import pytest

from payment_api import PaymentValidationError, process_payment_request


def test_process_payment_request_normalizes_and_processes_payment():
    seen_requests = {}

    response = process_payment_request(
        {
            "request_id": " pay_abc123 ",
            "amount_cents": 2500,
            "currency": " usd ",
        },
        seen_requests,
    )

    assert response == {
        "payment_id": "pay_pay_abc123",
        "request_id": "pay_abc123",
        "amount_cents": 2500,
        "currency": "USD",
        "status": "processed",
    }
    assert seen_requests["pay_abc123"]["response"] == response


def test_process_payment_request_duplicate_returns_processed_response_shape():
    seen_requests = {}

    first = process_payment_request(
        {"request_id": "dup-1", "amount_cents": 500, "currency": "EUR"},
        seen_requests,
    )
    second = process_payment_request(
        {"request_id": "dup-1", "amount_cents": 500, "currency": "EUR"},
        seen_requests,
    )

    assert first["status"] == "processed"
    assert second["status"] == "processed"
    assert second["payment_id"] == "pay_dup-1"


def test_process_payment_request_rejects_unsupported_currency():
    with pytest.raises(PaymentValidationError, match="currency is not supported"):
        process_payment_request(
            {"request_id": "pay-1", "amount_cents": 1000, "currency": "CAD"},
            {},
        )


def test_process_payment_request_rejects_non_integer_amount():
    with pytest.raises(PaymentValidationError, match="amount_cents must be an integer"):
        process_payment_request(
            {"request_id": "pay-2", "amount_cents": "1000", "currency": "USD"},
            {},
        )
