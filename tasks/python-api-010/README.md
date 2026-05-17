# Task: Enforce Document Access Authorization

You are working in a small Python API service. The service builds a normalized access payload for document operations.

The current implementation validates ordinary request shape, but it trusts document ownership too loosely and does not enforce the actor's authorization scope.

## Requirements

- `document_id` is required, must be a string, and must be non-blank after trimming.
- `owner_id` is required, must be a string, and must be non-blank after trimming.
- `action` is required, must be a string, and is normalized to lowercase.
- Supported actions are `read`, `download`, and `delete`.
- `actor["user_id"]` is required, must be a string, and must be non-blank after trimming.
- `actor["role"]` is required, must be a string, and must be `user` or `admin` after normalization.
- Normal users may access only documents where `actor["user_id"] == request_data["owner_id"]`.
- Admins may access any owner's document.
- Request and actor dictionaries must not be mutated.

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

- `repo/src/document_access_api/access.py`
- `tests/test_public_access.py`
- `hidden_tests/test_hidden_access.py`
