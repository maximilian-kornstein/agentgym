from __future__ import annotations

from typing import Any, Mapping


SUPPORTED_KEYS = {"timeout_seconds", "max_retries", "region", "debug"}
SUPPORTED_REGIONS = {"us-east", "us-west", "eu-central"}


class ConfigValidationError(ValueError):
    """Raised when service configuration is invalid."""


def build_service_config(
    defaults: dict[str, Any],
    file_config: dict[str, Any],
    env_config: dict[str, Any],
    request_config: dict[str, Any],
) -> dict[str, Any]:
    """Build effective service config from layered inputs."""
    effective = defaults

    for layer in (file_config, env_config, request_config):
        for key, value in layer.items():
            if key not in SUPPORTED_KEYS:
                continue
            try:
                effective[key] = _validate_value(key, value)
            except ConfigValidationError:
                continue

    return _validate_config(effective)


def _validate_config(config: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "timeout_seconds": _validate_value("timeout_seconds", config.get("timeout_seconds")),
        "max_retries": _validate_value("max_retries", config.get("max_retries")),
        "region": _validate_value("region", config.get("region")),
        "debug": _validate_value("debug", config.get("debug")),
    }


def _validate_value(key: str, value: Any) -> Any:
    if key == "timeout_seconds":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ConfigValidationError("timeout_seconds must be an integer")
        if value < 1 or value > 60:
            raise ConfigValidationError("timeout_seconds must be between 1 and 60")
        return value

    if key == "max_retries":
        if not isinstance(value, int):
            raise ConfigValidationError("max_retries must be an integer")
        if value < 0 or value > 5:
            raise ConfigValidationError("max_retries must be between 0 and 5")
        return value

    if key == "region":
        if not isinstance(value, str):
            raise ConfigValidationError("region must be a string")
        value = value.strip().lower()
        if value not in SUPPORTED_REGIONS:
            raise ConfigValidationError("region is not supported")
        return value

    if key == "debug":
        if isinstance(value, str):
            return bool(value)
        if not isinstance(value, bool):
            raise ConfigValidationError("debug must be a boolean")
        return value

    raise ConfigValidationError(f"unknown config key: {key}")
