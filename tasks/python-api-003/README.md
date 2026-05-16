# Task: Enforce Account Tax ID Rules

You are working in a small Python API service. The service builds normalized account payloads from request data before returning JSON to clients.

The current implementation validates individual fields, but it misses a cross-field business rule. Business accounts require a `tax_id`, and personal accounts must not include one.

## Requirements

- `email` is required.
- `email` must be a string.
- `email` should be trimmed and lowercased.
- `account_type` is required.
- `account_type` must be a string.
- `account_type` should be trimmed and lowercased.
- Supported account types are `personal` and `business`.
- `tax_id`, when present, must be a string.
- `tax_id`, when valid, should be trimmed.
- `business` accounts require a non-blank `tax_id`.
- `personal` accounts must reject `tax_id`.

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

- `repo/src/account_api/accounts.py`
- `tests/test_public_accounts.py`
- `hidden_tests/test_hidden_accounts.py`
