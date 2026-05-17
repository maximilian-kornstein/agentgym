import pytest

from booking_window_api import BookingWindowValidationError, build_booking_window_payload


def test_build_booking_window_payload_accepts_offset_timestamps():
    payload = build_booking_window_payload(
        {
            "start_at": "2026-05-17T10:30:00-04:00",
            "end_at": "2026-05-17T11:45:00-04:00",
        }
    )

    assert payload == {
        "start_at": "2026-05-17T14:30:00Z",
        "end_at": "2026-05-17T15:45:00Z",
    }


def test_build_booking_window_payload_accepts_zulu_utc_timestamps():
    payload = build_booking_window_payload(
        {
            "start_at": "2026-05-17T14:30:00Z",
            "end_at": "2026-05-17T15:30:00Z",
        }
    )

    assert payload["start_at"] == "2026-05-17T14:30:00Z"
    assert payload["end_at"] == "2026-05-17T15:30:00Z"


def test_build_booking_window_payload_rejects_missing_start_at():
    with pytest.raises(BookingWindowValidationError, match="start_at is required"):
        build_booking_window_payload({"end_at": "2026-05-17T15:30:00Z"})


def test_build_booking_window_payload_rejects_malformed_datetime():
    with pytest.raises(BookingWindowValidationError, match="start_at must be a valid ISO datetime"):
        build_booking_window_payload(
            {
                "start_at": "May 17 at 2:30",
                "end_at": "2026-05-17T15:30:00Z",
            }
        )
