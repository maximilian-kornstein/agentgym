# Task: Preserve Payment Idempotency

You are working in a small Python payment API. The service receives payment requests with idempotency keys and an explicit in-memory `seen_requests` mapping.

The current implementation handles ordinary payment requests, but it reprocesses duplicate request IDs and can mutate state for requests that should not be accepted.

## Requirements

- `request_id` is required.
- `request_id` must be a string.
- `request_id` is trimmed and must not be blank.
- `amount_cents` is required.
- `amount_cents` must be a positive integer.
- `amount_cents` must not be a boolean.
- `currency` is required.
- `currency` must be a string.
- `currency` is trimmed and uppercased.
- Supported currencies are `USD`, `EUR`, and `GBP`.
- `seen_requests` is a mutable mapping keyed by normalized `request_id`.
- Invalid requests must not mutate `seen_requests`.
- The first valid request stores and returns a processed payment response.
- Duplicate requests with the same normalized payload return the original stored response.
- Duplicate requests with the same `request_id` but changed `amount_cents` or `currency` must be rejected.

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

- `repo/src/payment_api/payments.py`
- `tests/test_public_payments.py`
- `hidden_tests/test_hidden_payments.py`
