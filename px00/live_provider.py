from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import os
import time
from typing import Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DATA_CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"}


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class LiveProviderProfile:
    profile_id: str
    provider_ref: str
    driver_ref: str
    endpoint_url: str
    allowed_host_refs: tuple[str, ...]
    model_ref: str
    auth_secret_env_ref: str
    live_enable_env_ref: str
    timeout_seconds: int
    max_response_bytes: int
    allowed_data_classifications: tuple[str, ...]
    status: str = "ACTIVE"

    def validate(self) -> None:
        parsed = urlparse(self.endpoint_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("LIVE_PROVIDER_ENDPOINT_MUST_BE_HTTPS")
        if parsed.username or parsed.password:
            raise ValueError("LIVE_PROVIDER_ENDPOINT_USERINFO_FORBIDDEN")
        if parsed.hostname not in set(self.allowed_host_refs):
            raise ValueError("LIVE_PROVIDER_HOST_NOT_ALLOWLISTED")
        if self.timeout_seconds <= 0 or self.timeout_seconds > 120:
            raise ValueError("LIVE_PROVIDER_TIMEOUT_OUT_OF_RANGE")
        if self.max_response_bytes <= 0 or self.max_response_bytes > 10_000_000:
            raise ValueError("LIVE_PROVIDER_RESPONSE_LIMIT_OUT_OF_RANGE")
        if self.status not in {"ACTIVE", "SUSPENDED", "RETIRED"}:
            raise ValueError("INVALID_LIVE_PROVIDER_STATUS")
        allowed = set(self.allowed_data_classifications)
        if not allowed or not allowed.issubset(DATA_CLASSIFICATIONS):
            raise ValueError("INVALID_LIVE_PROVIDER_DATA_CLASSIFICATION")
        if not self.auth_secret_env_ref or not self.live_enable_env_ref:
            raise ValueError("LIVE_PROVIDER_ENV_REF_REQUIRED")


@dataclass(frozen=True)
class ProviderHttpResponse:
    status_code: int
    headers: dict[str, str]
    body: bytes


class JsonTransport(Protocol):
    def post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: dict[str, object],
        timeout_seconds: int,
        max_response_bytes: int,
    ) -> ProviderHttpResponse: ...


@dataclass
class UrllibJsonTransport:
    """Minimal stdlib HTTPS transport. Secrets are supplied only through headers at runtime."""

    def post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: dict[str, object],
        timeout_seconds: int,
        max_response_bytes: int,
    ) -> ProviderHttpResponse:
        body = _canonical_json(payload).encode("utf-8")
        request_headers = {"Content-Type": "application/json", **dict(headers)}
        req = Request(url=url, data=body, headers=request_headers, method="POST")
        try:
            with urlopen(req, timeout=timeout_seconds) as response:
                raw = response.read(max_response_bytes + 1)
                if len(raw) > max_response_bytes:
                    raise ValueError("LIVE_PROVIDER_RESPONSE_TOO_LARGE")
                return ProviderHttpResponse(
                    status_code=int(response.status),
                    headers={str(k).lower(): str(v) for k, v in response.headers.items()},
                    body=raw,
                )
        except HTTPError as exc:
            raise ValueError(f"LIVE_PROVIDER_HTTP_ERROR:{exc.code}") from exc
        except URLError as exc:
            raise ValueError("LIVE_PROVIDER_NETWORK_ERROR") from exc
        except TimeoutError as exc:
            raise ValueError("LIVE_PROVIDER_TIMEOUT") from exc


class ProviderDriver(Protocol):
    def build_request(self, payload: dict[str, object], model_ref: str) -> dict[str, object]: ...

    def parse_response(self, payload: dict[str, object]) -> dict[str, object]: ...

    def provider_request_ref(self, headers: Mapping[str, str], payload: dict[str, object]) -> str | None: ...

    def returned_model_ref(self, payload: dict[str, object]) -> str | None: ...


@dataclass(frozen=True)
class LiveProviderCallRecord:
    call_id: str
    executor_invocation_ref: str
    provider_profile_ref: str
    provider_ref: str
    driver_ref: str
    requested_model_ref: str
    endpoint_host_ref: str
    data_classification: str
    request_payload_hash: str
    response_payload_hash: str
    http_status: int
    elapsed_ms: int
    status: str
    created_at: str
    provider_request_ref: str | None = None
    returned_model_ref: str | None = None


@dataclass
class LiveHttpsExecutorAdapter:
    profile: LiveProviderProfile
    driver: ProviderDriver
    executor_invocation_ref: str
    call_id: str
    created_at: str
    transport: JsonTransport = field(default_factory=UrllibJsonTransport)
    environment: Mapping[str, str] | None = None
    call_records: dict[str, LiveProviderCallRecord] = field(default_factory=dict)

    def _env(self) -> Mapping[str, str]:
        return os.environ if self.environment is None else self.environment

    def execute(self, bounded_input: dict[str, object]) -> dict[str, object]:
        self.profile.validate()
        if self.call_id in self.call_records:
            raise ValueError("LIVE_PROVIDER_CALL_ID_REUSE")
        if self.profile.status != "ACTIVE":
            raise ValueError("LIVE_PROVIDER_NOT_ACTIVE")

        env = self._env()
        enabled = str(env.get(self.profile.live_enable_env_ref, "")).strip().lower()
        if enabled not in {"1", "true", "yes", "on"}:
            raise ValueError("LIVE_PROVIDER_NOT_EXPLICITLY_ENABLED")
        secret = env.get(self.profile.auth_secret_env_ref)
        if not secret:
            raise ValueError("LIVE_PROVIDER_SECRET_MISSING")

        data_classification = str(bounded_input.get("data_classification", ""))
        if data_classification not in DATA_CLASSIFICATIONS:
            raise ValueError("LIVE_PROVIDER_REQUEST_CLASSIFICATION_REQUIRED")
        if data_classification not in set(self.profile.allowed_data_classifications):
            raise ValueError("LIVE_PROVIDER_DATA_EGRESS_DENIED")

        payload = bounded_input.get("payload")
        if not isinstance(payload, dict):
            raise ValueError("LIVE_PROVIDER_PAYLOAD_OBJECT_REQUIRED")

        request_payload = self.driver.build_request(dict(payload), self.profile.model_ref)
        if not isinstance(request_payload, dict):
            raise ValueError("LIVE_PROVIDER_DRIVER_REQUEST_INVALID")

        parsed = urlparse(self.profile.endpoint_url)
        host = parsed.hostname or ""
        if host not in set(self.profile.allowed_host_refs):
            raise ValueError("LIVE_PROVIDER_HOST_NOT_ALLOWLISTED")

        started = time.monotonic()
        response = self.transport.post_json(
            url=self.profile.endpoint_url,
            headers={"Authorization": f"Bearer {secret}"},
            payload=request_payload,
            timeout_seconds=self.profile.timeout_seconds,
            max_response_bytes=self.profile.max_response_bytes,
        )
        elapsed_ms = max(0, int((time.monotonic() - started) * 1000))
        if not 200 <= response.status_code < 300:
            raise ValueError(f"LIVE_PROVIDER_HTTP_STATUS:{response.status_code}")
        if len(response.body) > self.profile.max_response_bytes:
            raise ValueError("LIVE_PROVIDER_RESPONSE_TOO_LARGE")

        try:
            response_payload = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("LIVE_PROVIDER_RESPONSE_INVALID_JSON") from exc
        if not isinstance(response_payload, dict):
            raise ValueError("LIVE_PROVIDER_RESPONSE_OBJECT_REQUIRED")

        candidate = self.driver.parse_response(response_payload)
        if not isinstance(candidate, dict):
            raise ValueError("LIVE_PROVIDER_CANDIDATE_OBJECT_REQUIRED")

        record = LiveProviderCallRecord(
            call_id=self.call_id,
            executor_invocation_ref=self.executor_invocation_ref,
            provider_profile_ref=self.profile.profile_id,
            provider_ref=self.profile.provider_ref,
            driver_ref=self.profile.driver_ref,
            requested_model_ref=self.profile.model_ref,
            endpoint_host_ref=host,
            data_classification=data_classification,
            request_payload_hash=_sha256(request_payload),
            response_payload_hash=_sha256(response_payload),
            http_status=response.status_code,
            elapsed_ms=elapsed_ms,
            status="COMPLETED",
            created_at=self.created_at,
            provider_request_ref=self.driver.provider_request_ref(response.headers, response_payload),
            returned_model_ref=self.driver.returned_model_ref(response_payload),
        )
        self.call_records[self.call_id] = record

        result = dict(candidate)
        result["live_provider_provenance"] = {
            "call_ref": record.call_id,
            "provider_profile_ref": record.provider_profile_ref,
            "provider_ref": record.provider_ref,
            "driver_ref": record.driver_ref,
            "requested_model_ref": record.requested_model_ref,
            "returned_model_ref": record.returned_model_ref,
            "provider_request_ref": record.provider_request_ref,
            "request_payload_hash": record.request_payload_hash,
            "response_payload_hash": record.response_payload_hash,
            "data_classification": record.data_classification,
        }
        return result
