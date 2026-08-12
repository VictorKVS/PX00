import json
import unittest

from px00.executors import ExecutorDefinition, GovernedExecutorBoundary
from px00.factory_executor_case import _advance_to_implementation
from px00.factory_mvp import AgentRdFactoryMvp
from px00.factory_mvp_case import PRODUCER, VERIFIER
from px00.live_provider import (
    LiveHttpsExecutorAdapter,
    LiveProviderProfile,
    ProviderHttpResponse,
)


class FakeDriver:
    def build_request(self, payload, model_ref):
        return {"model": model_ref, "input": payload}

    def parse_response(self, payload):
        return dict(payload["candidate"])

    def provider_request_ref(self, headers, payload):
        return headers.get("x-request-id")

    def returned_model_ref(self, payload):
        return payload.get("model")


class FakeTransport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post_json(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def profile(**overrides):
    base = dict(
        profile_id="LIVE-PROFILE-TEST",
        provider_ref="PROVIDER-TEST",
        driver_ref="DRIVER-TEST",
        endpoint_url="https://api.example.test/v1/generate",
        allowed_host_refs=("api.example.test",),
        model_ref="model-test-v1",
        auth_secret_env_ref="PX00_TEST_PROVIDER_TOKEN",
        live_enable_env_ref="PX00_TEST_LIVE_ENABLED",
        timeout_seconds=10,
        max_response_bytes=4096,
        allowed_data_classifications=("PUBLIC", "INTERNAL"),
    )
    base.update(overrides)
    return LiveProviderProfile(**base)


def response(candidate=None, model="model-test-v1", status=200, raw_body=None):
    if raw_body is None:
        raw_body = json.dumps({"candidate": candidate or {"answer": "ok"}, "model": model}).encode("utf-8")
    return ProviderHttpResponse(
        status_code=status,
        headers={"x-request-id": "REQ-TEST-1"},
        body=raw_body,
    )


class LiveProviderBoundaryTests(unittest.TestCase):
    def adapter(self, *, p=None, transport=None, env=None, call_id="CALL-1"):
        return LiveHttpsExecutorAdapter(
            profile=p or profile(),
            driver=FakeDriver(),
            executor_invocation_ref="INV-LIVE-1",
            call_id=call_id,
            created_at="2026-08-12T20:00:00Z",
            transport=transport or FakeTransport(response()),
            environment=env if env is not None else {
                "PX00_TEST_LIVE_ENABLED": "true",
                "PX00_TEST_PROVIDER_TOKEN": "unit-test-credential",
            },
        )

    def test_profile_requires_https_and_allowlisted_host(self):
        with self.assertRaisesRegex(ValueError, "ENDPOINT_MUST_BE_HTTPS"):
            profile(endpoint_url="http://api.example.test/v1/generate").validate()
        with self.assertRaisesRegex(ValueError, "HOST_NOT_ALLOWLISTED"):
            profile(allowed_host_refs=("other.example.test",)).validate()

    def test_live_call_requires_explicit_opt_in_before_transport(self):
        transport = FakeTransport(response())
        adapter = self.adapter(
            transport=transport,
            env={"PX00_TEST_PROVIDER_TOKEN": "unit-test-credential"},
        )
        with self.assertRaisesRegex(ValueError, "NOT_EXPLICITLY_ENABLED"):
            adapter.execute({"data_classification": "INTERNAL", "payload": {"task": "x"}})
        self.assertEqual(transport.calls, [])

    def test_live_call_requires_secret_without_recording_it(self):
        transport = FakeTransport(response())
        adapter = self.adapter(
            transport=transport,
            env={"PX00_TEST_LIVE_ENABLED": "true"},
        )
        with self.assertRaisesRegex(ValueError, "SECRET_MISSING"):
            adapter.execute({"data_classification": "INTERNAL", "payload": {"task": "x"}})
        self.assertEqual(transport.calls, [])

    def test_data_egress_classification_blocks_before_transport(self):
        transport = FakeTransport(response())
        adapter = self.adapter(transport=transport)
        with self.assertRaisesRegex(ValueError, "DATA_EGRESS_DENIED"):
            adapter.execute({"data_classification": "RESTRICTED", "payload": {"task": "x"}})
        self.assertEqual(transport.calls, [])

    def test_success_records_hashes_provider_request_and_model(self):
        transport = FakeTransport(response(candidate={"answer": "candidate"}))
        adapter = self.adapter(transport=transport)
        result = adapter.execute({
            "data_classification": "INTERNAL",
            "payload": {"task": "summarize bounded input"},
        })
        self.assertEqual(result["answer"], "candidate")
        provenance = result["live_provider_provenance"]
        self.assertEqual(provenance["provider_request_ref"], "REQ-TEST-1")
        self.assertEqual(provenance["returned_model_ref"], "model-test-v1")
        record = adapter.call_records["CALL-1"]
        self.assertEqual(record.status, "COMPLETED")
        self.assertEqual(len(record.request_payload_hash), 64)
        self.assertEqual(len(record.response_payload_hash), 64)
        self.assertNotIn("unit-test-credential", repr(record))
        self.assertEqual(len(transport.calls), 1)
        self.assertIn("Authorization", transport.calls[0]["headers"])

    def test_invalid_json_and_bad_http_status_fail_closed(self):
        bad_json = self.adapter(transport=FakeTransport(response(raw_body=b"not-json")))
        with self.assertRaisesRegex(ValueError, "RESPONSE_INVALID_JSON"):
            bad_json.execute({"data_classification": "PUBLIC", "payload": {"task": "x"}})

        bad_http = self.adapter(transport=FakeTransport(response(status=503)), call_id="CALL-2")
        with self.assertRaisesRegex(ValueError, "HTTP_STATUS:503"):
            bad_http.execute({"data_classification": "PUBLIC", "payload": {"task": "x"}})

    def test_call_id_is_append_only(self):
        adapter = self.adapter()
        data = {"data_classification": "PUBLIC", "payload": {"task": "x"}}
        adapter.execute(data)
        with self.assertRaisesRegex(ValueError, "CALL_ID_REUSE"):
            adapter.execute(data)

    def test_live_adapter_can_pass_through_existing_governed_executor_boundary(self):
        mvp = AgentRdFactoryMvp()
        run_id = "LIVE-BOUNDARY-RUN"
        mvp.create_run(run_id, "bounded live provider pilot", PRODUCER, VERIFIER)
        _advance_to_implementation(mvp, run_id)

        boundary = GovernedExecutorBoundary()
        boundary.register(ExecutorDefinition(
            executor_id="EXEC-LIVE-TEST",
            executor_type="LLM",
            version_ref="adapter-0.1",
            provider_ref="PROVIDER-TEST",
            model_ref="model-test-v1",
            allowed_stage_refs=("IMPLEMENT_BOUNDED_PROTOTYPE",),
        ))
        adapter = self.adapter()
        record = boundary.invoke_to_artifact(
            mvp,
            run_id=run_id,
            invocation_id="INV-LIVE-1",
            executor_id="EXEC-LIVE-TEST",
            assignment_ref=PRODUCER,
            bounded_input={
                "data_classification": "INTERNAL",
                "payload": {"task": "produce candidate"},
            },
            artifact_id="LIVE-ART-006",
            adapter=adapter,
            created_at="2026-08-12T20:00:00Z",
        )
        self.assertEqual(record.status, "COMPLETED")
        payload = mvp.artifact_payload("LIVE-ART-006")
        self.assertIn("live_provider_provenance", payload)
        self.assertIn("executor_provenance", payload)
        self.assertNotIn("acceptance_record", payload)


if __name__ == "__main__":
    unittest.main()
