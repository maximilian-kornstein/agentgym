import copy

import pytest

from payment_api import PaymentValidationError, process_payment_request


def test_duplicate_request_returns_exact_original_response():
    seen_requests = {}
    first = process_payment_request(
        {"request_id": "idem-1", "amount_cents": 1200, "currency": "USD"},
        seen_requests,
    )
    seen_requests["idem-1"]["audit_marker"] = "preserve-original-entry"

    stored_before = copy.deepcopy(seen_requests)
    second = process_payment_request(
        {"request_id": "idem-1", "amount_cents": 1200, "currency": "USD"},
        seen_requests,
    )

    assert second == first
    assert seen_requests == stored_before


def test_duplicate_request_with_changed_amount_is_rejected():
    seen_requests = {}
    process_payment_request(
        {"request_id": "idem-2", "amount_cents": 1200, "currency": "USD"},
        seen_requests,
    )
    stored_before = copy.deepcopy(seen_requests)

    with pytest.raises(PaymentValidationError, match="idempotency conflict"):
        process_payment_request(
            {"request_id": "idem-2", "amount_cents": 1300, "currency": "USD"},
            seen_requests,
        )

    assert seen_requests == stored_before


def test_duplicate_request_with_changed_currency_is_rejected():
    seen_requests = {}
    process_payment_request(
        {"request_id": "idem-3", "amount_cents": 1200, "currency": "USD"},
        seen_requests,
    )
    stored_before = copy.deepcopy(seen_requests)

    with pytest.raises(PaymentValidationError, match="idempotency conflict"):
        process_payment_request(
            {"request_id": "idem-3", "amount_cents": 1200, "currency": "EUR"},
            seen_requests,
        )

    assert seen_requests == stored_before


def test_blank_request_id_is_rejected():
    with pytest.raises(PaymentValidationError, match="request_id cannot be blank"):
        process_payment_request(
            {"request_id": "   ", "amount_cents": 100, "currency": "USD"},
            {},
        )


def test_boolean_amount_is_rejected():
    with pytest.raises(PaymentValidationError, match="amount_cents must be an integer"):
        process_payment_request(
            {"request_id": "bool-amount", "amount_cents": True, "currency": "USD"},
            {},
        )


def test_invalid_request_does_not_mutate_seen_requests():
    seen_requests = {"existing": {"amount_cents": 500, "currency": "USD"}}
    stored_before = copy.deepcopy(seen_requests)

    with pytest.raises(PaymentValidationError, match="amount_cents must be an integer"):
        process_payment_request(
            {"request_id": "invalid-1", "amount_cents": "500", "currency": "USD"},
            seen_requests,
        )

    assert seen_requests == stored_before
