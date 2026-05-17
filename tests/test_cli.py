from agentgym.cli import main
from tests.test_tasks import _make_task


def test_list_command_prints_table_with_all_current_tasks(capsys):
    exit_code = main(["list"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "id" in captured.out
    assert "difficulty" in captured.out
    assert "language" in captured.out
    assert "title" in captured.out
    assert "python-api-001" in captured.out
    assert "python-api-002" in captured.out
    assert "python-api-003" in captured.out
    assert "python-api-004" in captured.out
    assert "python-api-005" in captured.out
    assert "python-api-006" in captured.out
    assert "Reject whitespace-only profile fields" in captured.out


def test_validate_command_still_accepts_single_task_id(capsys):
    exit_code = main(["validate", "python-api-001"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "python-api-001: valid\n"


def test_validate_command_without_task_id_validates_all_tasks(capsys):
    exit_code = main(["validate"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "python-api-001: valid" in captured.out
    assert "python-api-002: valid" in captured.out
    assert "python-api-003: valid" in captured.out
    assert "python-api-004: valid" in captured.out
    assert "python-api-005: valid" in captured.out
    assert "python-api-006: valid" in captured.out
    assert "6 tasks valid" in captured.out


def test_validate_all_exits_nonzero_when_any_task_is_invalid(tmp_path, monkeypatch, capsys):
    valid_task = _make_task(tmp_path, "valid-task")
    invalid_task = _make_task(tmp_path, "invalid-task")
    (invalid_task / "score.sh").unlink()
    monkeypatch.setenv("AGENTGYM_ROOT", str(tmp_path))

    exit_code = main(["validate"])
    captured = capsys.readouterr()

    assert valid_task.exists()
    assert exit_code == 1
    assert "valid-task: valid" in captured.out
    assert "invalid-task: invalid" in captured.err
    assert "missing required file or directory: score.sh" in captured.err
    assert "1 of 2 tasks invalid" in captured.err


def test_run_command_prints_public_and_hidden_test_summary(capsys):
    exit_code = main(["run", "python-api-001"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Task: python-api-001" in captured.out
    assert "Status: fail" in captured.out
    assert "Public tests: pass" in captured.out
    assert "Hidden tests: fail" in captured.out
    assert "Error: hidden_tests_failed" in captured.out


def test_run_suite_runs_all_tasks_and_writes_suite_result(tmp_path, monkeypatch, capsys):
    _make_suite_task(tmp_path, "task-pass", hidden_test_command="exit 0")
    _make_suite_task(tmp_path, "task-hidden-fail", hidden_test_command="exit 1")
    monkeypatch.setenv("AGENTGYM_ROOT", str(tmp_path))

    exit_code = main(["run-suite"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "id                public  hidden  status" in captured.out
    assert "task-pass         pass    pass    pass" in captured.out
    assert "task-hidden-fail  pass    fail    fail" in captured.out
    assert "2/2 tasks passed public tests" in captured.out
    assert "1/2 tasks passed hidden tests" in captured.out
    assert "Suite result: " in captured.out


def test_run_suite_rejects_invalid_tasks(tmp_path, monkeypatch, capsys):
    invalid_task = _make_suite_task(tmp_path, "invalid-task")
    (invalid_task / "score.sh").unlink()
    monkeypatch.setenv("AGENTGYM_ROOT", str(tmp_path))

    exit_code = main(["run-suite"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "invalid-task: invalid" in captured.err
    assert "missing required file or directory: score.sh" in captured.err


def _make_suite_task(
    root,
    task_id: str,
    *,
    setup_command: str = "exit 0",
    public_test_command: str = "exit 0",
    hidden_test_command: str = "exit 0",
):
    task_dir = _make_task(root, task_id)
    (task_dir / "task.yaml").write_text(
        f"""
id: {task_id}
title: Suite Task
language: python
domain: test
difficulty: easy
description: Suite task.
setup_command: {setup_command}
public_test_command: {public_test_command}
hidden_test_command: {hidden_test_command}
score_command: ./score.sh
timeout_seconds: 60
""".lstrip(),
        encoding="utf-8",
    )
    return task_dir
