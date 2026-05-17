import json
from pathlib import Path

from agentgym.runner import run_task
from agentgym.tasks import Task


def test_run_task_stops_when_setup_fails(tmp_path):
    task = _make_runner_task(tmp_path, setup_command="exit 7")

    result = run_task(task)
    data = _read_result(result.result_path)

    assert result.status == "fail"
    assert result.setup_exit_code == 7
    assert result.public_exit_code is None
    assert result.hidden_exit_code is None
    assert result.public_tests_passed is None
    assert result.hidden_tests_passed is None
    assert result.agent_command is None
    assert result.agent_exit_code is None
    assert result.agent_ran is False
    assert result.error_type == "setup_failed"
    assert data["error_type"] == "setup_failed"
    assert data["agent_command"] is None
    assert data["agent_exit_code"] is None
    assert data["agent_ran"] is False


def test_run_task_stops_when_public_tests_fail(tmp_path):
    task = _make_runner_task(tmp_path, public_test_command="exit 4")

    result = run_task(task)
    data = _read_result(result.result_path)

    assert result.status == "fail"
    assert result.setup_exit_code == 0
    assert result.public_exit_code == 4
    assert result.hidden_exit_code is None
    assert result.public_tests_passed is False
    assert result.hidden_tests_passed is None
    assert result.error_type == "public_tests_failed"
    assert data["public_tests_passed"] is False
    assert data["hidden_tests_passed"] is None


def test_run_task_records_hidden_test_failure(tmp_path):
    task = _make_runner_task(tmp_path, hidden_test_command="exit 5")

    result = run_task(task)
    data = _read_result(result.result_path)

    assert result.status == "fail"
    assert result.public_tests_passed is True
    assert result.hidden_tests_passed is False
    assert result.score_exit_code == 5
    assert result.error_type == "hidden_tests_failed"
    assert data["public_exit_code"] == 0
    assert data["hidden_exit_code"] == 5
    assert data["score_exit_code"] == 5
    assert data["public_tests_passed"] is True
    assert data["hidden_tests_passed"] is False


def test_run_task_passes_when_setup_public_and_hidden_pass(tmp_path):
    task = _make_runner_task(tmp_path)

    result = run_task(task)
    data = _read_result(result.result_path)

    assert result.status == "pass"
    assert result.setup_exit_code == 0
    assert result.public_exit_code == 0
    assert result.hidden_exit_code == 0
    assert result.public_tests_passed is True
    assert result.hidden_tests_passed is True
    assert result.error_type is None
    assert data["status"] == "pass"


def test_run_task_runs_agent_before_public_and_hidden_tests(tmp_path):
    task = _make_runner_task(
        tmp_path,
        public_test_command="test -f agent-output.txt",
    )

    result = run_task(task, agent_command="touch agent-output.txt")
    data = _read_result(result.result_path)

    assert result.status == "pass"
    assert result.agent_command == "touch agent-output.txt"
    assert result.agent_exit_code == 0
    assert result.agent_ran is True
    assert result.public_tests_passed is True
    assert result.hidden_tests_passed is True
    assert (result.logs_path / "agent.log").exists()
    assert data["agent_command"] == "touch agent-output.txt"
    assert data["agent_exit_code"] == 0
    assert data["agent_ran"] is True


def test_run_task_stops_when_agent_fails(tmp_path):
    task = _make_runner_task(
        tmp_path,
        public_test_command="touch public-ran",
        hidden_test_command="touch hidden-ran",
    )

    result = run_task(task, agent_command="exit 9")
    data = _read_result(result.result_path)

    assert result.status == "fail"
    assert result.agent_exit_code == 9
    assert result.agent_ran is True
    assert result.public_exit_code is None
    assert result.hidden_exit_code is None
    assert result.public_tests_passed is None
    assert result.hidden_tests_passed is None
    assert result.error_type == "agent_failed"
    assert not (result.run_workspace / "public-ran").exists()
    assert not (result.run_workspace / "hidden-ran").exists()
    assert data["agent_command"] == "exit 9"
    assert data["agent_exit_code"] == 9
    assert data["agent_ran"] is True
    assert data["error_type"] == "agent_failed"


def test_run_task_stops_when_agent_times_out(tmp_path):
    task = _make_runner_task(
        tmp_path,
        timeout_seconds=1,
        public_test_command="touch public-ran",
    )

    result = run_task(task, agent_command="sleep 2")
    data = _read_result(result.result_path)

    assert result.status == "fail"
    assert result.agent_exit_code == 124
    assert result.agent_ran is True
    assert result.public_exit_code is None
    assert result.hidden_exit_code is None
    assert result.error_type == "agent_timeout"
    assert not (result.run_workspace / "public-ran").exists()
    assert data["agent_exit_code"] == 124
    assert data["error_type"] == "agent_timeout"


def _make_runner_task(
    root: Path,
    *,
    setup_command: str = "exit 0",
    public_test_command: str = "exit 0",
    hidden_test_command: str = "exit 0",
    timeout_seconds: int = 10,
) -> Task:
    task_dir = root / "runner-task"
    task_dir.mkdir()
    for dirname in ("repo", "tests", "hidden_tests"):
        (task_dir / dirname).mkdir()
    metadata = {
        "id": "runner-task",
        "title": "Runner Task",
        "language": "python",
        "difficulty": "easy",
        "setup_command": setup_command,
        "public_test_command": public_test_command,
        "hidden_test_command": hidden_test_command,
        "score_command": "exit 0",
        "timeout_seconds": timeout_seconds,
    }
    return Task(
        id="runner-task",
        title="Runner Task",
        language="python",
        difficulty="easy",
        path=task_dir,
        metadata=metadata,
    )


def _read_result(result_path: Path) -> dict:
    return json.loads(result_path.read_text(encoding="utf-8"))
