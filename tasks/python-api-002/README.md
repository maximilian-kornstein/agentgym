# Task: Reject Non-Boolean Notification Preferences

You are working in a small Python API service. The service builds normalized notification settings from request data before returning JSON to clients.

The current implementation handles defaults and ordinary boolean values, but it has a nested validation bug. Preference values must be actual booleans. Strings and integers should not be coerced.

## Requirements

- `email` is required.
- `email` must be a string.
- `email` should be trimmed and lowercased.
- `notification_preferences` is optional.
- When omitted, all supported preferences default to `False`.
- Supported preference keys are `email_updates`, `sms_alerts`, and `product_news`.
- Unknown preference keys must be rejected.
- Preference values must be booleans.
- Values like `"false"`, `"yes"`, `1`, and `0` must be rejected instead of coerced.

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

- `repo/src/notification_api/notifications.py`
- `tests/test_public_notifications.py`
- `hidden_tests/test_hidden_notifications.py`
