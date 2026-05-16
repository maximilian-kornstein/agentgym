import pytest

from account_api import AccountValidationError, build_account_payload


def test_business_account_requires_tax_id():
    with pytest.raises(AccountValidationError, match="business accounts require tax_id"):
        build_account_payload(
            {
                "email": "hedy@example.com",
                "account_type": "business",
            }
        )


def test_business_account_rejects_blank_tax_id():
    with pytest.raises(AccountValidationError, match="tax_id cannot be blank"):
        build_account_payload(
            {
                "email": "dorothy@example.com",
                "account_type": "business",
                "tax_id": "   ",
            }
        )


def test_personal_account_rejects_tax_id():
    with pytest.raises(AccountValidationError, match="personal accounts cannot include tax_id"):
        build_account_payload(
            {
                "email": "mary@example.com",
                "account_type": "personal",
                "tax_id": "US-999",
            }
        )


def test_business_tax_id_is_trimmed_and_preserved():
    payload = build_account_payload(
        {
            "email": "annie@example.com",
            "account_type": " business ",
            "tax_id": "  US-456  ",
        }
    )

    assert payload == {
        "email": "annie@example.com",
        "account_type": "business",
        "tax_id": "US-456",
    }
