import pytest

from account_api import AccountValidationError, build_account_payload


def test_build_account_payload_accepts_personal_account():
    payload = build_account_payload(
        {
            "email": "  ADA@Example.COM ",
            "account_type": " Personal ",
        }
    )

    assert payload == {
        "email": "ada@example.com",
        "account_type": "personal",
    }


def test_build_account_payload_accepts_business_account_with_tax_id():
    payload = build_account_payload(
        {
            "email": "grace@example.com",
            "account_type": "business",
            "tax_id": "US-123",
        }
    )

    assert payload == {
        "email": "grace@example.com",
        "account_type": "business",
        "tax_id": "US-123",
    }


def test_build_account_payload_rejects_unsupported_account_type():
    with pytest.raises(AccountValidationError, match="account_type must be personal or business"):
        build_account_payload(
            {
                "email": "katherine@example.com",
                "account_type": "enterprise",
            }
        )


def test_build_account_payload_rejects_non_string_tax_id():
    with pytest.raises(AccountValidationError, match="tax_id must be a string"):
        build_account_payload(
            {
                "email": "margaret@example.com",
                "account_type": "business",
                "tax_id": 123,
            }
        )
