from __future__ import annotations

from typing import Mapping


class GeminiInteractionsDriver:
    """Provider-specific mapping for one bounded text-only Gemini Interactions pilot.

    The driver deliberately exposes no tools, function calls, grounding, files, multimodal input,
    background execution or provider-side agent. It returns candidate text only; verification and
    acceptance remain outside the provider boundary.
    """

    MAX_INPUT_CHARS = 32_000
    _ALLOWED_INPUT_KEYS = {"input"}

    def build_request(self, payload: dict[str, object], model_ref: str) -> dict[str, object]:
        unknown = set(payload) - self._ALLOWED_INPUT_KEYS
        if unknown:
            raise ValueError("GEMINI_BOUNDED_INPUT_FIELD_FORBIDDEN")

        text = payload.get("input")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("GEMINI_TEXT_INPUT_REQUIRED")
        if len(text) > self.MAX_INPUT_CHARS:
            raise ValueError("GEMINI_TEXT_INPUT_TOO_LARGE")
        if not isinstance(model_ref, str) or not model_ref.strip():
            raise ValueError("GEMINI_MODEL_REF_REQUIRED")

        return {
            "model": model_ref,
            "input": text,
            "store": False,
        }

    def parse_response(self, payload: dict[str, object]) -> dict[str, object]:
        if payload.get("object") != "interaction":
            raise ValueError("GEMINI_INTERACTION_OBJECT_REQUIRED")
        if payload.get("status") != "completed":
            raise ValueError("GEMINI_INTERACTION_NOT_COMPLETED")
        if not isinstance(payload.get("id"), str) or not str(payload["id"]).strip():
            raise ValueError("GEMINI_INTERACTION_ID_REQUIRED")
        if not isinstance(payload.get("model"), str) or not str(payload["model"]).strip():
            raise ValueError("GEMINI_RETURNED_MODEL_REQUIRED")

        steps = payload.get("steps")
        if not isinstance(steps, list) or not steps:
            raise ValueError("GEMINI_OUTPUT_STEPS_REQUIRED")

        text_parts: list[str] = []
        for step in steps:
            if not isinstance(step, dict):
                raise ValueError("GEMINI_STEP_OBJECT_REQUIRED")
            step_type = step.get("type")
            if step_type == "thought":
                # Internal reasoning is neither copied into the candidate nor treated as evidence.
                continue
            if step_type != "model_output":
                raise ValueError("GEMINI_NON_MODEL_OUTPUT_STEP_FORBIDDEN")

            content = step.get("content")
            if not isinstance(content, list) or not content:
                raise ValueError("GEMINI_MODEL_OUTPUT_CONTENT_REQUIRED")
            for item in content:
                if not isinstance(item, dict):
                    raise ValueError("GEMINI_MODEL_OUTPUT_ITEM_REQUIRED")
                if item.get("type") != "text":
                    raise ValueError("GEMINI_NON_TEXT_OUTPUT_FORBIDDEN")
                text = item.get("text")
                if not isinstance(text, str) or not text.strip():
                    raise ValueError("GEMINI_TEXT_OUTPUT_REQUIRED")
                text_parts.append(text)

        if not text_parts:
            raise ValueError("GEMINI_TEXT_OUTPUT_REQUIRED")

        return {"text": "\n".join(text_parts)}

    def provider_request_ref(self, headers: Mapping[str, str], payload: dict[str, object]) -> str | None:
        interaction_id = payload.get("id")
        if isinstance(interaction_id, str) and interaction_id.strip():
            return interaction_id
        request_id = headers.get("x-request-id") or headers.get("x-goog-request-id")
        return request_id if isinstance(request_id, str) and request_id.strip() else None

    def returned_model_ref(self, payload: dict[str, object]) -> str | None:
        model = payload.get("model")
        return model if isinstance(model, str) and model.strip() else None
