from __future__ import annotations

from typing import Any, Mapping


SUPPORTED_ACCOUNT_TYPES = {"personal", "business"}


class AccountValidationError(ValueError):
    """Raised when request data cannot be converted into an account payload."""


def build_account_payload(request_data: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize account request data into a JSON-safe API payload."""
    email = _require_text(request_data, "email").lower()
    account_type = _require_text(request_data, "account_type").lower()

    if account_type not in SUPPORTED_ACCOUNT_TYPES:
        raise AccountValidationError("account_type must be personal or business")

    payload = {
        "email": email,
        "account_type": account_type,
    }

    if "tax_id" in request_data:
        payload["tax_id"] = _require_text(request_data, "tax_id")

    return payload


def _require_text(request_data: Mapping[str, Any], field_name: str) -> str:
    if field_name not in request_data:
        raise AccountValidationError(f"{field_name} is required")

    value = request_data[field_name]
    if not isinstance(value, str):
        raise AccountValidationError(f"{field_name} must be a string")

    value = value.strip()
    if value == "":
        raise AccountValidationError(f"{field_name} cannot be blank")

    return value
