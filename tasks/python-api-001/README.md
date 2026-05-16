# Task: Reject Whitespace-Only Profile Fields

You are working in a small Python API service. The service builds normalized profile payloads from request data before returning JSON to clients.

The current implementation handles ordinary inputs, but it has an edge-case validation bug. Required text fields must be rejected if they are blank after trimming whitespace.

## Requirements

- `email` is required.
- `display_name` is required.
- Both required fields must be strings.
- Both required fields must contain non-whitespace text after trimming.
- `email` should be lowercased after trimming.
- `display_name` should be trimmed but should keep internal spacing.
- `profile_slug` should be generated from the trimmed display name.
- `marketing_opt_in` is optional and defaults to `False`.
- `marketing_opt_in`, when provided, must be a boolean.

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

- `repo/src/profile_api/profiles.py`
- `tests/test_public_profiles.py`
- `hidden_tests/test_hidden_profiles.py`
