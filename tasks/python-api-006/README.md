# Task: Enforce Profile Update Semantics

You are working in a small Python API service. The service builds normalized PATCH-style profile update payloads from client input.

The current implementation handles ordinary updates, but it confuses omitted fields with explicit invalid values and allows no-op or over-permissive updates.

## Requirements

- Supported update fields are:
  - `display_name`
  - `bio`
  - `marketing_opt_in`
- Omitted fields should not appear in the returned payload.
- At least one supported update field must be present and valid.
- Unknown fields must be rejected.
- Explicit `None` must be rejected for every supported field.
- `display_name` must be a string.
- `display_name` is trimmed and must not be blank after trimming.
- `bio` must be a string.
- `bio` is trimmed, but an empty string is allowed so users can clear their bio.
- `marketing_opt_in` must be a real boolean.
- Boolean-like strings or integers must be rejected, not coerced.

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

- `repo/src/profile_update_api/updates.py`
- `tests/test_public_updates.py`
- `hidden_tests/test_hidden_updates.py`
