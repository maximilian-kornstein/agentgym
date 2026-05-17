from __future__ import annotations

from typing import Any, Mapping


SUPPORTED_ACTIONS = {"read", "download", "delete"}


class DocumentAccessValidationError(ValueError):
    """Raised when a document access request is invalid."""


def build_document_access_payload(
    request_data: dict[str, Any],
    actor: dict[str, Any],
) -> dict[str, str]:
    """Build a normalized document access payload."""
    document_id = _require_text(request_data, "document_id")
    owner_id = _require_text(request_data, "owner_id")
    action = _require_text(request_data, "action").lower()
    if action not in SUPPORTED_ACTIONS:
        raise DocumentAccessValidationError("action is not supported")

    request_data["document_id"] = document_id
    request_data["owner_id"] = owner_id
    request_data["action"] = action

    actor_user_id = _require_actor_text(actor, "user_id")
    role = _require_actor_text(actor, "role").lower()
    actor["role"] = role

    return {
        "document_id": document_id,
        "owner_id": owner_id,
        "actor_user_id": actor_user_id,
        "actor_role": role,
        "action": action,
        "authorized": True,
    }


def _require_text(request_data: Mapping[str, Any], field_name: str) -> str:
    if field_name not in request_data:
        raise DocumentAccessValidationError(f"{field_name} is required")

    value = request_data[field_name]
    if not isinstance(value, str):
        raise DocumentAccessValidationError(f"{field_name} must be a string")

    value = value.strip()
    if value == "":
        raise DocumentAccessValidationError(f"{field_name} cannot be blank")

    return value


def _require_actor_text(actor: Mapping[str, Any], field_name: str) -> str:
    if field_name not in actor:
        raise DocumentAccessValidationError(f"actor {field_name} is required")

    value = actor[field_name]
    if not isinstance(value, str):
        raise DocumentAccessValidationError(f"actor {field_name} must be a string")

    return value.strip()
