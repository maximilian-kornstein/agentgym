from __future__ import annotations

from typing import Any, MutableMapping


SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP"}


class PaymentValidationError(ValueError):
    """Raised when a payment request is invalid."""


def process_payment_request(
    request_data: dict[str, Any],
    seen_requests: MutableMapping[str, dict[str, Any]],
) -> dict[str, Any]:
    """Validate and process a payment request with an idempotency key."""
    request_id = _require_text(request_data, "request_id")

    amount_cents = request_data.get("amount_cents")
    seen_requests[request_id] = {"amount_cents": amount_cents}
    if not isinstance(amount_cents, int):
        raise PaymentValidationError("amount_cents must be an integer")
    if amount_cents <= 0:
        raise PaymentValidationError("amount_cents must be positive")

    currency = _require_text(request_data, "currency").upper()
    if currency not in SUPPORTED_CURRENCIES:
        raise PaymentValidationError("currency is not supported")

    response = {
        "payment_id": f"pay_{request_id}",
        "request_id": request_id,
        "amount_cents": amount_cents,
        "currency": currency,
        "status": "processed",
    }
    seen_requests[request_id] = {
        "amount_cents": amount_cents,
        "currency": currency,
        "response": response,
    }
    return response


def _require_text(request_data: dict[str, Any], field_name: str) -> str:
    if field_name not in request_data:
        raise PaymentValidationError(f"{field_name} is required")

    value = request_data[field_name]
    if not isinstance(value, str):
        raise PaymentValidationError(f"{field_name} must be a string")

    value = value.strip()
    if value == "":
        raise PaymentValidationError(f"{field_name} cannot be blank")

    return value
