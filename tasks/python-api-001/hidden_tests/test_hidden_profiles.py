import pytest

from profile_api import ProfileValidationError, build_profile_payload


@pytest.mark.parametrize(
    ("field_name", "request_data"),
    [
        (
            "email",
            {
                "email": "   ",
                "display_name": "Hedy Lamarr",
            },
        ),
        (
            "display_name",
            {
                "email": "hedy@example.com",
                "display_name": "\t\n  ",
            },
        ),
    ],
)
def test_required_text_fields_reject_whitespace_only_values(field_name, request_data):
    with pytest.raises(ProfileValidationError, match=f"{field_name} cannot be blank"):
        build_profile_payload(request_data)


def test_display_name_with_internal_spacing_is_preserved_after_trim():
    payload = build_profile_payload(
        {
            "email": "dorothy@example.com",
            "display_name": "  Dorothy   Vaughan  ",
        }
    )

    assert payload["display_name"] == "Dorothy   Vaughan"
    assert payload["profile_slug"] == "dorothy-vaughan"
