# Task: Prevent Internal User Field Leaks

You are working in a small Python API service. The service builds public user response payloads from internal database records.

The current implementation returns normal user fields, but it also leaks internal-only fields. Public API responses must include only the fields intended for clients.

## Requirements

- The response must include `id`.
- The response must include `email`, trimmed and lowercased.
- The response must include `display_name`, trimmed.
- The response must include `is_active` as a boolean.
- The response must not include internal-only fields such as:
  - `password_hash`
  - `internal_notes`
  - `admin_flags`
  - `last_login_ip`
- Extra internal fields should be ignored, not copied into the response.
- Required response fields must be present in the input record.

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

- `repo/src/user_api/users.py`
- `tests/test_public_users.py`
- `hidden_tests/test_hidden_users.py`
