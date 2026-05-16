from __future__ import annotations

from typing import Any, Mapping


SUPPORTED_PREFERENCES = ("email_updates", "sms_alerts", "product_news")


class NotificationValidationError(ValueError):
    """Raised when request data cannot be converted into notification settings."""


def build_notification_payload(request_data: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize notification request data into a JSON-safe API payload."""
    email = _require_email(request_data)
    preferences = _build_preferences(request_data.get("notification_preferences", {}))

    return {
        "email": email,
        "notification_preferences": preferences,
    }


def _require_email(request_data: Mapping[str, Any]) -> str:
    if "email" not in request_data:
        raise NotificationValidationError("email is required")

    email = request_data["email"]
    if not isinstance(email, str):
        raise NotificationValidationError("email must be a string")

    email = email.strip().lower()
    if email == "":
        raise NotificationValidationError("email cannot be blank")

    return email


def _build_preferences(raw_preferences: Any) -> dict[str, bool]:
    if not isinstance(raw_preferences, Mapping):
        raise NotificationValidationError("notification_preferences must be an object")

    preferences = {key: False for key in SUPPORTED_PREFERENCES}

    for key, value in raw_preferences.items():
        if key not in preferences:
            raise NotificationValidationError(f"unsupported notification preference: {key}")
        preferences[key] = bool(value)

    return preferences
