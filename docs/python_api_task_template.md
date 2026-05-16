# Python API Task Template

Use this template for the next Python API-validation tasks.

## Task Concept

Pick one realistic API bug:

- required field mishandled
- optional field default wrong
- type coercion too permissive
- nested payload validation incomplete
- date/time edge case
- enum/status validation bug
- serialization leaks internal-only fields

The task should be narrow enough that the intended fix is 3-20 lines.

## Directory Shape

```text
tasks/python-api-002/
  task.yaml
  README.md
  setup.sh
  score.sh
  solution.patch
  repo/
    pyproject.toml
    src/<package_name>/
      __init__.py
      <module>.py
  tests/
    test_public_<topic>.py
  hidden_tests/
    test_hidden_<topic>.py
```

## `task.yaml` Fields

```yaml
id: python-api-002
title: Short imperative task title
language: python
domain: api-input-validation
difficulty: easy
estimated_human_minutes: 15
tags:
  - api
  - validation
  - edge-case
description: >
  One or two sentences describing the bug and what hidden tests check.
setup_command: ./setup.sh
public_test_command: .venv/bin/python -m pytest tests
hidden_test_command: .venv/bin/python -m pytest hidden_tests
score_command: ./score.sh
timeout_seconds: 60
allowed_tools:
  - shell
  - editor
  - pytest
failure_modes:
  - passed-public-failed-hidden
  - incomplete-input-validation
  - hardcoded-test-behavior
  - syntax-error
  - dependency-setup-failure
```

## Starter Repo Pattern

The starter repo should expose one small public function:

```python
def build_<resource>_payload(request_data: Mapping[str, Any]) -> dict[str, Any]:
    ...
```

Use a custom exception type:

```python
class <Resource>ValidationError(ValueError):
    ...
```

Keep dependencies minimal. Prefer the Python standard library plus `pytest`.

## Public Test Pattern

Public tests should cover:

- one successful normalized payload
- one default value
- one obvious invalid request
- one type validation error

## Hidden Test Pattern

Hidden tests should cover:

- one edge case public tests imply but do not reveal
- one shallow-fix trap
- one behavior-preservation check

## Reference Patch

Generate `solution.patch` from the task directory so this command works:

```bash
patch -p0 < solution.patch
```

The patch should touch only the starter repo code unless a task genuinely requires config changes.
