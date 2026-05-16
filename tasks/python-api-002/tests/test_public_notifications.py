import pytest

from notification_api import NotificationValidationError, build_notification_payload


def test_build_notification_payload_defaults_preferences():
    payload = build_notification_payload({"email": "  ADA@Example.COM "})

    assert payload == {
        "email": "ada@example.com",
        "notification_preferences": {
            "email_updates": False,
            "sms_alerts": False,
            "product_news": False,
        },
    }


def test_build_notification_payload_accepts_boolean_preferences():
    payload = build_notification_payload(
        {
            "email": "grace@example.com",
            "notification_preferences": {
                "email_updates": True,
                "sms_alerts": False,
            },
        }
    )

    assert payload["notification_preferences"] == {
        "email_updates": True,
        "sms_alerts": False,
        "product_news": False,
    }


def test_build_notification_payload_rejects_unknown_preference_key():
    with pytest.raises(
        NotificationValidationError,
        match="unsupported notification preference: push_alerts",
    ):
        build_notification_payload(
            {
                "email": "katherine@example.com",
                "notification_preferences": {"push_alerts": True},
            }
        )


def test_build_notification_payload_rejects_non_object_preferences():
    with pytest.raises(NotificationValidationError, match="notification_preferences must be an object"):
        build_notification_payload(
            {
                "email": "margaret@example.com",
                "notification_preferences": ["email_updates"],
            }
        )
