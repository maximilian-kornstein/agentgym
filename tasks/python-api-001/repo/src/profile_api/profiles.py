from __future__ import annotations

import re
from typing import Any, Mapping


class ProfileValidationError(ValueError):
    """Raised when request data cannot be converted into a profile payload."""


def build_profile_payload(request_data: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize profile request data into a JSON-safe API payload."""
    email = _require_text(request_data, "email").lower()
    display_name = _require_text(request_data, "display_name")
    marketing_opt_in = request_data.get("marketing_opt_in", False)

    if not isinstance(marketing_opt_in, bool):
        raise ProfileValidationError("marketing_opt_in must be a boolean")

    return {
        "email": email,
        "display_name": display_name,
        "profile_slug": _slugify(display_name),
        "marketing_opt_in": marketing_opt_in,
    }


def _require_text(request_data: Mapping[str, Any], field_name: str) -> str:
    if field_name not in request_data:
        raise ProfileValidationError(f"{field_name} is required")

    value = request_data[field_name]
    if not isinstance(value, str):
        raise ProfileValidationError(f"{field_name} must be a string")

    if value == "":
        raise ProfileValidationError(f"{field_name} cannot be blank")

    return value.strip()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "profile"
