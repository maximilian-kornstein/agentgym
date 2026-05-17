from __future__ import annotations

from typing import Any, Mapping


SUPPORTED_FIELDS = {"display_name", "bio", "marketing_opt_in"}


class ProfileUpdateValidationError(ValueError):
    """Raised when a profile update payload is invalid."""


def build_profile_update_payload(request_data: Mapping[str, Any]) -> dict[str, Any]:
    """Build a normalized profile update payload from PATCH-style input."""
    payload: dict[str, Any] = {}

    display_name = request_data.get("display_name")
    if display_name is not None:
        if not isinstance(display_name, str):
            raise ProfileUpdateValidationError("display_name must be a string")
        payload["display_name"] = display_name.strip()

    bio = request_data.get("bio")
    if bio is not None:
        if not isinstance(bio, str):
            raise ProfileUpdateValidationError("bio must be a string")
        payload["bio"] = bio.strip()

    marketing_opt_in = request_data.get("marketing_opt_in")
    if marketing_opt_in is not None:
        payload["marketing_opt_in"] = bool(marketing_opt_in)

    return payload
