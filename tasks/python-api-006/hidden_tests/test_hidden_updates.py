import pytest

from profile_update_api import ProfileUpdateValidationError, build_profile_update_payload


def test_build_profile_update_payload_rejects_empty_update():
    with pytest.raises(ProfileUpdateValidationError, match="at least one update field is required"):
        build_profile_update_payload({})


def test_build_profile_update_payload_rejects_explicit_none_values():
    with pytest.raises(ProfileUpdateValidationError, match="display_name cannot be null"):
        build_profile_update_payload({"display_name": None})

    with pytest.raises(ProfileUpdateValidationError, match="bio cannot be null"):
        build_profile_update_payload({"bio": None})

    with pytest.raises(ProfileUpdateValidationError, match="marketing_opt_in cannot be null"):
        build_profile_update_payload({"marketing_opt_in": None})


def test_build_profile_update_payload_rejects_blank_display_name():
    with pytest.raises(ProfileUpdateValidationError, match="display_name cannot be blank"):
        build_profile_update_payload({"display_name": " \t\n "})


def test_build_profile_update_payload_rejects_unknown_fields():
    with pytest.raises(ProfileUpdateValidationError, match="unknown field: role"):
        build_profile_update_payload({"display_name": "Ada", "role": "admin"})


def test_build_profile_update_payload_rejects_boolean_like_strings():
    with pytest.raises(ProfileUpdateValidationError, match="marketing_opt_in must be a boolean"):
        build_profile_update_payload({"marketing_opt_in": "true"})


def test_build_profile_update_payload_rejects_integer_booleans():
    with pytest.raises(ProfileUpdateValidationError, match="marketing_opt_in must be a boolean"):
        build_profile_update_payload({"marketing_opt_in": 1})


def test_build_profile_update_payload_omits_absent_fields():
    payload = build_profile_update_payload({"display_name": "Grace Hopper"})

    assert payload == {"display_name": "Grace Hopper"}
    assert "bio" not in payload
    assert "marketing_opt_in" not in payload
