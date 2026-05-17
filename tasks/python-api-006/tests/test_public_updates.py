import pytest

from profile_update_api import ProfileUpdateValidationError, build_profile_update_payload


def test_build_profile_update_payload_trims_display_name():
    payload = build_profile_update_payload({"display_name": "  Ada Lovelace  "})

    assert payload == {"display_name": "Ada Lovelace"}


def test_build_profile_update_payload_allows_empty_bio_to_clear_it():
    payload = build_profile_update_payload({"bio": "   "})

    assert payload == {"bio": ""}


def test_build_profile_update_payload_preserves_false_marketing_choice():
    payload = build_profile_update_payload({"marketing_opt_in": False})

    assert payload == {"marketing_opt_in": False}


def test_build_profile_update_payload_rejects_non_string_display_name():
    with pytest.raises(ProfileUpdateValidationError, match="display_name must be a string"):
        build_profile_update_payload({"display_name": 123})
