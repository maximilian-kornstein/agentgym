from __future__ import annotations

from typing import Any, Mapping


REQUIRED_FIELDS = ("id", "email", "display_name", "is_active")


class UserSerializationError(ValueError):
    """Raised when a user record cannot be serialized into an API response."""


def build_user_response(user_record: Mapping[str, Any]) -> dict[str, Any]:
    """Serialize an internal user record into a public API response."""
    _require_fields(user_record)

    response = dict(user_record)
    response["email"] = _require_text(user_record, "email").lower()
    response["display_name"] = _require_text(user_record, "display_name")

    if not isinstance(response["is_active"], bool):
        raise UserSerializationError("is_active must be a boolean")

    return response


def _require_fields(user_record: Mapping[str, Any]) -> None:
    for field_name in REQUIRED_FIELDS:
        if field_name not in user_record:
            raise UserSerializationError(f"{field_name} is required")


def _require_text(user_record: Mapping[str, Any], field_name: str) -> str:
    value = user_record[field_name]
    if not isinstance(value, str):
        raise UserSerializationError(f"{field_name} must be a string")

    value = value.strip()
    if value == "":
        raise UserSerializationError(f"{field_name} cannot be blank")

    return value
