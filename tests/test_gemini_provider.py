import json
import unittest

from px00.gemini_provider import GeminiInteractionsDriver
from px00.live_provider import LiveHttpsExecutorAdapter, LiveProviderProfile, ProviderHttpResponse


class FakeTransport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post_json(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def gemini_response(*, status="completed", steps=None, model="gemini-3.6-flash"):
    if steps is None:
        steps = [
            {"type": "thought", "signature": "opaque-provider-state"},
            {"type": "model_output", "content": [{"type": "text", "text": "bounded candidate"}]},
        ]
    body = {
        "id": "interaction-test-001",
        "model": model,
        "object": "interaction",
        "status": status,
        "steps": steps,
    }
    return ProviderHttpResponse(
        status_code=200,
        headers={"x-request-id": "transport-request-001"},
        body=json.dumps(body).encode("utf-8"),
    )


def gemini_profile(**overrides):
    base = dict(
        profile_id="LIVE-GEMINI-TEST",
        provider_ref="GOOGLE_GEMINI_API",
        driver_ref="px00.gemini_provider.GeminiInteractionsDriver",
        endpoint_url="https://generativelanguage.googleapis.com/v1/interactions",
        allowed_host_refs=("generativelanguage.googleapis.com",),
        model_ref="gemini-3.6-flash",
        auth_secret_env_ref="PX00_GEMINI_TEST_CREDENTIAL",
        live_enable_env_ref="PX00_GEMINI_TEST_ENABLED",
        timeout_seconds=30,
        max_response_bytes=1_000_000,
        allowed_data_classifications=("PUBLIC",),
        auth_header_name="x-goog-api-key",
        auth_header_prefix="",
    )
    base.update(overrides)
    return LiveProviderProfile(**base)


class GeminiInteractionsDriverTests(unittest.TestCase):
    def setUp(self):
        self.driver = GeminiInteractionsDriver()

    def test_build_request_is_text_only_and_contains_no_tools(self):
        request = self.driver.build_request({"input": "Return one bounded candidate."}, "gemini-3.6-flash")
        self.assertEqual(
            request,
            {
                "model": "gemini-3.6-flash",
                "input": "Return one bounded candidate.",
                "store": False,
            },
        )
        self.assertNotIn("tools", request)
        self.assertNotIn("agent", request)
        self.assertNotIn("background", request)

    def test_build_request_rejects_extra_provider_capabilities(self):
        with self.assertRaisesRegex(ValueError, "BOUNDED_INPUT_FIELD_FORBIDDEN"):
            self.driver.build_request(
                {"input": "x", "tools": [{"type": "google_search"}]},
                "gemini-3.6-flash",
            )

    def test_build_request_requires_bounded_text(self):
        with self.assertRaisesRegex(ValueError, "TEXT_INPUT_REQUIRED"):
            self.driver.build_request({"input": "   "}, "gemini-3.6-flash")
        with self.assertRaisesRegex(ValueError, "TEXT_INPUT_TOO_LARGE"):
            self.driver.build_request({"input": "x" * 32_001}, "gemini-3.6-flash")

    def test_parse_response_returns_only_model_text_not_thought_state(self):
        payload = json.loads(gemini_response().body.decode("utf-8"))
        candidate = self.driver.parse_response(payload)
        self.assertEqual(candidate, {"text": "bounded candidate"})
        self.assertNotIn("opaque-provider-state", repr(candidate))

    def test_parse_response_rejects_non_completed_or_non_text_output(self):
        incomplete = json.loads(gemini_response(status="incomplete").body.decode("utf-8"))
        with self.assertRaisesRegex(ValueError, "INTERACTION_NOT_COMPLETED"):
            self.driver.parse_response(incomplete)

        non_text = json.loads(
            gemini_response(
                steps=[{"type": "model_output", "content": [{"type": "image", "uri": "ignored"}]}]
            ).body.decode("utf-8")
        )
        with self.assertRaisesRegex(ValueError, "NON_TEXT_OUTPUT_FORBIDDEN"):
            self.driver.parse_response(non_text)

    def test_parse_response_rejects_function_call_even_if_provider_returns_one(self):
        payload = json.loads(
            gemini_response(
                steps=[{"type": "function_call", "name": "unexpected_tool", "arguments": {}}]
            ).body.decode("utf-8")
        )
        with self.assertRaisesRegex(ValueError, "NON_MODEL_OUTPUT_STEP_FORBIDDEN"):
            self.driver.parse_response(payload)

    def test_interaction_id_and_returned_model_are_provenance(self):
        payload = json.loads(gemini_response().body.decode("utf-8"))
        self.assertEqual(self.driver.provider_request_ref({}, payload), "interaction-test-001")
        self.assertEqual(self.driver.returned_model_ref(payload), "gemini-3.6-flash")


class GeminiLiveBoundaryIntegrationTests(unittest.TestCase):
    def adapter(self, *, transport=None, profile=None):
        return LiveHttpsExecutorAdapter(
            profile=profile or gemini_profile(),
            driver=GeminiInteractionsDriver(),
            executor_invocation_ref="INV-GEMINI-TEST-001",
            call_id="CALL-GEMINI-TEST-001",
            created_at="2026-08-13T00:00:00Z",
            transport=transport or FakeTransport(gemini_response()),
            environment={
                "PX00_GEMINI_TEST_ENABLED": "true",
                "PX00_GEMINI_TEST_CREDENTIAL": "unit-test-credential",
            },
        )

    def test_gemini_uses_x_goog_api_key_not_bearer_authorization(self):
        transport = FakeTransport(gemini_response())
        adapter = self.adapter(transport=transport)
        result = adapter.execute(
            {
                "data_classification": "PUBLIC",
                "payload": {"input": "Produce one safe text candidate."},
            }
        )
        self.assertEqual(result["text"], "bounded candidate")
        self.assertEqual(len(transport.calls), 1)
        headers = transport.calls[0]["headers"]
        self.assertIn("x-goog-api-key", headers)
        self.assertNotIn("Authorization", headers)
        self.assertEqual(headers["x-goog-api-key"], "unit-test-credential")

        record = adapter.call_records["CALL-GEMINI-TEST-001"]
        self.assertEqual(record.provider_request_ref, "interaction-test-001")
        self.assertEqual(record.returned_model_ref, "gemini-3.6-flash")
        self.assertNotIn("unit-test-credential", repr(record))
        self.assertNotIn("unit-test-credential", repr(result))

    def test_public_only_profile_blocks_internal_before_transport(self):
        transport = FakeTransport(gemini_response())
        adapter = self.adapter(transport=transport)
        with self.assertRaisesRegex(ValueError, "DATA_EGRESS_DENIED"):
            adapter.execute(
                {
                    "data_classification": "INTERNAL",
                    "payload": {"input": "do not send"},
                }
            )
        self.assertEqual(transport.calls, [])

    def test_auth_header_name_and_prefix_are_validated(self):
        with self.assertRaisesRegex(ValueError, "AUTH_HEADER_INVALID"):
            gemini_profile(auth_header_name="bad header").validate()
        with self.assertRaisesRegex(ValueError, "AUTH_PREFIX_INVALID"):
            gemini_profile(auth_header_prefix="bad\r\nprefix").validate()


if __name__ == "__main__":
    unittest.main()
