import pytest

from notification_api import NotificationValidationError, build_notification_payload


@pytest.mark.parametrize(
    ("preference_name", "bad_value"),
    [
        ("email_updates", "false"),
        ("email_updates", "yes"),
        ("sms_alerts", 1),
        ("product_news", 0),
    ],
)
def test_notification_preferences_reject_non_boolean_values(preference_name, bad_value):
    with pytest.raises(
        NotificationValidationError,
        match=f"{preference_name} must be a boolean",
    ):
        build_notification_payload(
            {
                "email": "hedy@example.com",
                "notification_preferences": {preference_name: bad_value},
            }
        )


def test_false_boolean_value_is_preserved_not_dropped():
    payload = build_notification_payload(
        {
            "email": "dorothy@example.com",
            "notification_preferences": {
                "email_updates": True,
                "sms_alerts": False,
                "product_news": True,
            },
        }
    )

    assert payload["notification_preferences"] == {
        "email_updates": True,
        "sms_alerts": False,
        "product_news": True,
    }
