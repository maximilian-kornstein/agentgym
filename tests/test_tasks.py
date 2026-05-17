from pathlib import Path

from agentgym.tasks import discover_tasks, validate_task, validate_task_id


def test_discover_tasks_finds_python_api_golden_task():
    task_ids = {task.id for task in discover_tasks()}

    assert "python-api-001" in task_ids


def test_validate_current_golden_task_passes():
    task, errors = validate_task_id("python-api-001")

    assert task is not None
    assert errors == []


def test_validation_fails_for_missing_required_metadata(tmp_path, monkeypatch):
    task_dir = _make_task(tmp_path, "bad-task")
    (task_dir / "task.yaml").write_text(
        """
id: bad-task
title: Bad Task
language: python
domain: api
difficulty: easy
description: Missing command metadata.
timeout_seconds: 60
""".lstrip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("AGENTGYM_ROOT", str(tmp_path))

    task, errors = validate_task_id("bad-task")

    assert task is not None
    assert "missing required metadata field: setup_command" in errors
    assert "missing required metadata field: score_command" in errors
    assert "missing required metadata field: primary_failure_mode" in errors


def test_validation_fails_for_missing_required_file(tmp_path, monkeypatch):
    task_dir = _make_task(tmp_path, "bad-task")
    (task_dir / "score.sh").unlink()
    monkeypatch.setenv("AGENTGYM_ROOT", str(tmp_path))

    task, errors = validate_task_id("bad-task")

    assert task is not None
    assert "missing required file or directory: score.sh" in errors


def test_validation_fails_for_blank_primary_failure_mode(tmp_path, monkeypatch):
    task_dir = _make_task(tmp_path, "bad-task")
    task_yaml = task_dir / "task.yaml"
    task_yaml.write_text(
        task_yaml.read_text(encoding="utf-8").replace(
            "primary_failure_mode: test-failure-mode",
            "primary_failure_mode: ''",
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("AGENTGYM_ROOT", str(tmp_path))

    task, errors = validate_task_id("bad-task")

    assert task is not None
    assert "primary_failure_mode must be a non-empty string" in errors


def _make_task(root: Path, task_id: str) -> Path:
    task_dir = root / "tasks" / task_id
    task_dir.mkdir(parents=True)
    for dirname in ("repo", "tests", "hidden_tests"):
        (task_dir / dirname).mkdir()
    for filename in ("README.md", "setup.sh", "score.sh", "solution.patch"):
        (task_dir / filename).write_text("", encoding="utf-8")
    (task_dir / "task.yaml").write_text(
        f"""
id: {task_id}
title: Test Task
language: python
domain: api
difficulty: easy
description: Test task.
primary_failure_mode: test-failure-mode
setup_command: ./setup.sh
public_test_command: python -m pytest tests
hidden_test_command: python -m pytest hidden_tests
score_command: ./score.sh
timeout_seconds: 60
""".lstrip(),
        encoding="utf-8",
    )
    return task_dir
