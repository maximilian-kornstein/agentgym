from user_api import build_user_response


def test_build_user_response_does_not_leak_sensitive_internal_fields():
    payload = build_user_response(
        {
            "id": "user_321",
            "email": "hedy@example.com",
            "display_name": "Hedy Lamarr",
            "is_active": True,
            "password_hash": "pbkdf2:secret",
            "internal_notes": "VIP escalation history",
            "admin_flags": ["staff_override"],
            "last_login_ip": "192.0.2.10",
        }
    )

    assert payload == {
        "id": "user_321",
        "email": "hedy@example.com",
        "display_name": "Hedy Lamarr",
        "is_active": True,
    }


def test_build_user_response_ignores_unknown_internal_fields():
    payload = build_user_response(
        {
            "id": "user_654",
            "email": "dorothy@example.com",
            "display_name": "Dorothy Vaughan",
            "is_active": True,
            "billing_customer_id": "cus_internal_123",
            "feature_gate_snapshot": {"beta": True},
        }
    )

    assert set(payload) == {"id", "email", "display_name", "is_active"}


def test_build_user_response_still_normalizes_public_fields_when_internal_fields_exist():
    payload = build_user_response(
        {
            "id": "user_987",
            "email": "  MARY@Example.COM ",
            "display_name": "  Mary Jackson  ",
            "is_active": False,
            "password_hash": "do-not-return",
        }
    )

    assert payload["email"] == "mary@example.com"
    assert payload["display_name"] == "Mary Jackson"
    assert payload["is_active"] is False
