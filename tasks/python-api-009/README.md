# Task: Validate Timezone-Aware Booking Windows

You are working in a small Python API service. The service builds a normalized booking-window payload from request data.

The current implementation handles ordinary ISO datetime strings, but it accepts naive timestamps too loosely and compares start/end boundaries incorrectly when offsets differ.

## Requirements

- `start_at` is required.
- `end_at` is required.
- Both fields must be strings.
- Both fields must be valid ISO 8601 datetimes with explicit timezone offsets.
- `Z` is accepted as UTC.
- Naive datetimes without an offset must be rejected.
- `end_at` must be strictly after `start_at`.
- Equal start and end timestamps are invalid.
- Output must normalize both timestamps to UTC strings like `2026-05-17T14:30:00Z`.
- The input dictionary must not be mutated.

## Run The Task

From this task directory:

```bash
./setup.sh
./score.sh
```

The starter code should pass public tests but fail hidden tests.

## Verify The Reference Solution

From this task directory:

```bash
patch -p0 < solution.patch
./score.sh
```

After applying the reference patch, public and hidden tests should pass.

## Files To Inspect

- `repo/src/booking_window_api/windows.py`
- `tests/test_public_windows.py`
- `hidden_tests/test_hidden_windows.py`
