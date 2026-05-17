# Task: Enforce Service Config Precedence

You are working in a small Python API service. The service builds an effective runtime configuration from four layers: defaults, file config, environment config, and request config.

The current implementation handles ordinary precedence examples, but it accepts invalid overrides too loosely and can mutate input dictionaries while merging.

## Requirements

- Merge config sources with this precedence:
  - `request_config`
  - `env_config`
  - `file_config`
  - `defaults`
- Supported config keys are:
  - `timeout_seconds`
  - `max_retries`
  - `region`
  - `debug`
- `timeout_seconds` must be an integer from `1` to `60`.
- `max_retries` must be an integer from `0` to `5`.
- `region` must be one of `us-east`, `us-west`, or `eu-central`.
- `debug` must be a real boolean.
- Boolean-like strings and integers must be rejected, not coerced.
- Unknown config keys must be rejected from any layer.
- Invalid higher-precedence values must be rejected, not skipped in favor of lower-precedence values.
- Input dictionaries must not be mutated.

## Run The Task

From this task directory:

```bash
./setup.sh
./score.sh
```

The starter code should pass public tests but fail hidden tests.

## Verify The Reference Solution

From this task directory:

```bash
patch -p0 < solution.patch
./score.sh
```

After applying the reference patch, public and hidden tests should pass.

## Files To Inspect

- `repo/src/service_config_api/config.py`
- `tests/test_public_config.py`
- `hidden_tests/test_hidden_config.py`
