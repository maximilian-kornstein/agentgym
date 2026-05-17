# Task: Enforce Search Pagination Bounds

You are working in a small Python API service. The service builds normalized search request payloads from client input.

The current implementation handles ordinary search requests, but it accepts invalid pagination and sort values that should be rejected by the public API contract.

## Requirements

- `query` is required.
- `query` must be a string.
- `query` must be trimmed.
- `query` must not be blank after trimming.
- `limit` is optional and defaults to `20`.
- `limit` must be an integer from `1` to `100`.
- `offset` is optional and defaults to `0`.
- `offset` must be an integer greater than or equal to `0`.
- Numeric strings such as `"10"` or `"0"` must be rejected, not coerced.
- `sort` is optional and defaults to `"relevance"`.
- `sort` must be a string.
- `sort` is trimmed and lowercased.
- Supported sort values are `relevance`, `newest`, and `oldest`.
- Unknown sort values must be rejected.

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

- `repo/src/search_api/search.py`
- `tests/test_public_search.py`
- `hidden_tests/test_hidden_search.py`
