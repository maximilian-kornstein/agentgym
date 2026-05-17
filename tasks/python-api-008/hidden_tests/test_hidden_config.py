import copy

import pytest

from service_config_api import ConfigValidationError, build_service_config


def _defaults():
    return {
        "timeout_seconds": 10,
        "max_retries": 2,
        "region": "us-east",
        "debug": False,
    }


def test_invalid_request_value_is_rejected_instead_of_falling_back():
    with pytest.raises(ConfigValidationError, match="timeout_seconds must be between 1 and 60"):
        build_service_config(
            _defaults(),
            {"timeout_seconds": 20},
            {"timeout_seconds": 30},
            {"timeout_seconds": 99},
        )


def test_invalid_env_value_is_rejected_instead_of_falling_back():
    with pytest.raises(ConfigValidationError, match="region is not supported"):
        build_service_config(
            _defaults(),
            {"region": "us-west"},
            {"region": "ap-south"},
            {},
        )


def test_debug_string_is_rejected_instead_of_coerced():
    with pytest.raises(ConfigValidationError, match="debug must be a boolean"):
        build_service_config(
            _defaults(),
            {},
            {},
            {"debug": "false"},
        )


def test_boolean_max_retries_is_rejected():
    with pytest.raises(ConfigValidationError, match="max_retries must be an integer"):
        build_service_config(
            _defaults(),
            {},
            {"max_retries": True},
            {},
        )


def test_unknown_keys_are_rejected_from_any_layer():
    with pytest.raises(ConfigValidationError, match="unknown config key: feature_flag"):
        build_service_config(
            _defaults(),
            {"feature_flag": True},
            {},
            {},
        )

    with pytest.raises(ConfigValidationError, match="unknown config key: region_override"):
        build_service_config(
            _defaults(),
            {},
            {},
            {"region_override": "us-west"},
        )


def test_input_dictionaries_are_not_mutated():
    defaults = _defaults()
    file_config = {"timeout_seconds": 20}
    env_config = {"region": "eu-central"}
    request_config = {"debug": True}
    before = copy.deepcopy((defaults, file_config, env_config, request_config))

    build_service_config(defaults, file_config, env_config, request_config)

    assert (defaults, file_config, env_config, request_config) == before


def test_full_precedence_chain_uses_request_value():
    config = build_service_config(
        {"timeout_seconds": 10, "max_retries": 1, "region": "us-east", "debug": False},
        {"timeout_seconds": 20, "max_retries": 2, "region": "us-west", "debug": False},
        {"timeout_seconds": 30, "max_retries": 3, "region": "eu-central", "debug": False},
        {"timeout_seconds": 40, "max_retries": 4, "region": "us-east", "debug": True},
    )

    assert config == {
        "timeout_seconds": 40,
        "max_retries": 4,
        "region": "us-east",
        "debug": True,
    }
