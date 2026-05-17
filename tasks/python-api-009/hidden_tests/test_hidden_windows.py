import copy

import pytest

from booking_window_api import BookingWindowValidationError, build_booking_window_payload


def test_naive_start_at_is_rejected():
    with pytest.raises(BookingWindowValidationError, match="start_at must include a timezone offset"):
        build_booking_window_payload(
            {
                "start_at": "2026-05-17T14:30:00",
                "end_at": "2026-05-17T15:30:00Z",
            }
        )


def test_naive_end_at_is_rejected():
    with pytest.raises(BookingWindowValidationError, match="end_at must include a timezone offset"):
        build_booking_window_payload(
            {
                "start_at": "2026-05-17T14:30:00Z",
                "end_at": "2026-05-17T15:30:00",
            }
        )


def test_equal_start_and_end_is_rejected():
    with pytest.raises(BookingWindowValidationError, match="end_at must be after start_at"):
        build_booking_window_payload(
            {
                "start_at": "2026-05-17T14:30:00Z",
                "end_at": "2026-05-17T14:30:00Z",
            }
        )


def test_end_before_start_is_rejected_after_utc_normalization():
    with pytest.raises(BookingWindowValidationError, match="end_at must be after start_at"):
        build_booking_window_payload(
            {
                "start_at": "2026-05-17T10:30:00-04:00",
                "end_at": "2026-05-17T10:45:00-03:00",
            }
        )


def test_mixed_offsets_are_normalized_to_utc():
    payload = build_booking_window_payload(
        {
            "start_at": "2026-05-17T10:30:00-04:00",
            "end_at": "2026-05-17T17:00:00+01:00",
        }
    )

    assert payload == {
        "start_at": "2026-05-17T14:30:00Z",
        "end_at": "2026-05-17T16:00:00Z",
    }


def test_non_string_datetime_values_are_rejected():
    with pytest.raises(BookingWindowValidationError, match="start_at must be a string"):
        build_booking_window_payload(
            {
                "start_at": 20260517,
                "end_at": "2026-05-17T15:30:00Z",
            }
        )


def test_input_dictionary_is_not_mutated():
    request_data = {
        "start_at": "2026-05-17T10:30:00-04:00",
        "end_at": "2026-05-17T11:30:00-04:00",
    }
    before = copy.deepcopy(request_data)

    build_booking_window_payload(request_data)

    assert request_data == before
