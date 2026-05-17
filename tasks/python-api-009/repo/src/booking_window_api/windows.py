from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class BookingWindowValidationError(ValueError):
    """Raised when a booking window payload is invalid."""


def build_booking_window_payload(request_data: dict[str, Any]) -> dict[str, str]:
    """Build a normalized booking-window payload."""
    if "start_at" not in request_data:
        raise BookingWindowValidationError("start_at is required")
    if "end_at" not in request_data:
        raise BookingWindowValidationError("end_at is required")

    start_at = _parse_datetime(request_data["start_at"], "start_at")
    end_at = _parse_datetime(request_data["end_at"], "end_at")

    if _wall_clock(end_at) < _wall_clock(start_at):
        raise BookingWindowValidationError("end_at must be after start_at")

    return {
        "start_at": _format_utc(start_at),
        "end_at": _format_utc(end_at),
    }


def _parse_datetime(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise BookingWindowValidationError(f"{field_name} must be a string")

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BookingWindowValidationError(f"{field_name} must be a valid ISO datetime") from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed


def _wall_clock(value: datetime) -> datetime:
    return value.replace(tzinfo=None)


def _format_utc(value: datetime) -> str:
    utc_value = value.astimezone(timezone.utc).replace(tzinfo=None)
    return f"{utc_value.isoformat(timespec='seconds')}Z"
