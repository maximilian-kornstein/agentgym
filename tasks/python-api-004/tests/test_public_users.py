import pytest

from user_api import UserSerializationError, build_user_response


def test_build_user_response_serializes_public_fields():
    payload = build_user_response(
        {
            "id": "user_123",
            "email": "  ADA@Example.COM ",
            "display_name": "  Ada Lovelace  ",
            "is_active": True,
        }
    )

    assert payload == {
        "id": "user_123",
        "email": "ada@example.com",
        "display_name": "Ada Lovelace",
        "is_active": True,
    }


def test_build_user_response_preserves_inactive_boolean():
    payload = build_user_response(
        {
            "id": "user_456",
            "email": "grace@example.com",
            "display_name": "Grace Hopper",
            "is_active": False,
        }
    )

    assert payload["is_active"] is False


def test_build_user_response_rejects_missing_required_field():
    with pytest.raises(UserSerializationError, match="display_name is required"):
        build_user_response(
            {
                "id": "user_789",
                "email": "katherine@example.com",
                "is_active": True,
            }
        )


def test_build_user_response_rejects_non_boolean_active_flag():
    with pytest.raises(UserSerializationError, match="is_active must be a boolean"):
        build_user_response(
            {
                "id": "user_999",
                "email": "margaret@example.com",
                "display_name": "Margaret Hamilton",
                "is_active": "yes",
            }
        )
