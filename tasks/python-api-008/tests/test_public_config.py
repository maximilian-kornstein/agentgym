import pytest

from service_config_api import ConfigValidationError, build_service_config


def test_build_service_config_uses_defaults_only():
    config = build_service_config(
        {
            "timeout_seconds": 10,
            "max_retries": 2,
            "region": "us-east",
            "debug": False,
        },
        {},
        {},
        {},
    )

    assert config == {
        "timeout_seconds": 10,
        "max_retries": 2,
        "region": "us-east",
        "debug": False,
    }


def test_build_service_config_file_overrides_defaults():
    config = build_service_config(
        {"timeout_seconds": 10, "max_retries": 2, "region": "us-east", "debug": False},
        {"timeout_seconds": 20},
        {},
        {},
    )

    assert config["timeout_seconds"] == 20


def test_build_service_config_env_overrides_file():
    config = build_service_config(
        {"timeout_seconds": 10, "max_retries": 2, "region": "us-east", "debug": False},
        {"region": "us-west"},
        {"region": "eu-central"},
        {},
    )

    assert config["region"] == "eu-central"


def test_build_service_config_request_overrides_env():
    config = build_service_config(
        {"timeout_seconds": 10, "max_retries": 2, "region": "us-east", "debug": False},
        {},
        {"debug": False},
        {"debug": True},
    )

    assert config["debug"] is True


def test_build_service_config_rejects_obvious_timeout_type_error():
    with pytest.raises(ConfigValidationError, match="timeout_seconds must be an integer"):
        build_service_config(
            {"timeout_seconds": "10", "max_retries": 2, "region": "us-east", "debug": False},
            {},
            {},
            {},
        )
