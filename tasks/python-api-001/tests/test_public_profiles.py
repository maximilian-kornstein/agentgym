import pytest

from profile_api import ProfileValidationError, build_profile_payload


def test_build_profile_payload_normalizes_valid_request():
    payload = build_profile_payload(
        {
            "email": "  ADA@Example.COM ",
            "display_name": "  Ada Lovelace  ",
            "marketing_opt_in": True,
        }
    )

    assert payload == {
        "email": "ada@example.com",
        "display_name": "Ada Lovelace",
        "profile_slug": "ada-lovelace",
        "marketing_opt_in": True,
    }


def test_build_profile_payload_defaults_marketing_opt_in():
    payload = build_profile_payload(
        {
            "email": "grace@example.com",
            "display_name": "Grace Hopper",
        }
    )

    assert payload["marketing_opt_in"] is False


def test_build_profile_payload_rejects_missing_required_field():
    with pytest.raises(ProfileValidationError, match="display_name is required"):
        build_profile_payload({"email": "katherine@example.com"})


def test_build_profile_payload_rejects_non_boolean_marketing_flag():
    with pytest.raises(ProfileValidationError, match="marketing_opt_in must be a boolean"):
        build_profile_payload(
            {
                "email": "margaret@example.com",
                "display_name": "Margaret Hamilton",
                "marketing_opt_in": "yes",
            }
        )
