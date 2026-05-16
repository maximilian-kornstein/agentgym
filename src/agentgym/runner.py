from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import Any

from .tasks import Task


@dataclass(frozen=True)
class RunResult:
    status: str
    result_path: Path
    logs_path: Path
    run_workspace: Path
    setup_exit_code: int | None
    public_exit_code: int | None
    hidden_exit_code: int | None
    score_exit_code: int | None
    public_tests_passed: bool | None
    hidden_tests_passed: bool | None
    error_type: str | None


def run_task(task: Task) -> RunResult:
    run_id = f"{task.id}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    run_root = Path(tempfile.mkdtemp(prefix=f"agentgym-{task.id}-"))
    run_workspace = run_root / task.id
    shutil.copytree(task.path, run_workspace, ignore=_ignore_generated_files)

    agentgym_dir = run_workspace / ".agentgym"
    logs_dir = agentgym_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now(UTC)
    started_clock = monotonic()
    timeout_seconds = int(task.metadata["timeout_seconds"])

    setup_result = _run_command(
        command=str(task.metadata["setup_command"]),
        cwd=run_workspace,
        timeout_seconds=timeout_seconds,
        log_path=logs_dir / "setup.log",
    )

    public_result: subprocess.CompletedProcess[str] | _TimeoutResult | None = None
    hidden_result: subprocess.CompletedProcess[str] | _TimeoutResult | None = None
    error_type: str | None = None
    status = "fail"

    if _exit_code(setup_result) != 0:
        error_type = "setup_timeout" if isinstance(setup_result, _TimeoutResult) else "setup_failed"
    else:
        _ensure_workspace_venv_link(run_workspace)
        public_result = _run_command(
            command=str(task.metadata["public_test_command"]),
            cwd=run_workspace,
            timeout_seconds=timeout_seconds,
            log_path=logs_dir / "public.log",
        )
        if _exit_code(public_result) != 0:
            error_type = "public_tests_timeout" if isinstance(public_result, _TimeoutResult) else "public_tests_failed"
        else:
            hidden_result = _run_command(
                command=str(task.metadata["hidden_test_command"]),
                cwd=run_workspace,
                timeout_seconds=timeout_seconds,
                log_path=logs_dir / "hidden.log",
            )
            if _exit_code(hidden_result) == 0:
                status = "pass"
            else:
                error_type = "hidden_tests_timeout" if isinstance(hidden_result, _TimeoutResult) else "hidden_tests_failed"

    completed_at = datetime.now(UTC)
    public_exit_code = _exit_code(public_result)
    hidden_exit_code = _exit_code(hidden_result)
    result_path = agentgym_dir / "result.json"
    result_data: dict[str, Any] = {
        "run_id": run_id,
        "task_id": task.id,
        "started_at": _format_timestamp(started_at),
        "completed_at": _format_timestamp(completed_at),
        "duration_seconds": round(monotonic() - started_clock, 3),
        "status": status,
        "setup_exit_code": _exit_code(setup_result),
        "public_exit_code": public_exit_code,
        "hidden_exit_code": hidden_exit_code,
        "score_exit_code": hidden_exit_code,
        "public_tests_passed": _tests_passed(public_exit_code),
        "hidden_tests_passed": _tests_passed(hidden_exit_code),
        "logs_path": str(logs_dir),
        "run_workspace": str(run_workspace),
        "error_type": error_type,
    }
    result_path.write_text(json.dumps(result_data, indent=2) + "\n", encoding="utf-8")

    return RunResult(
        status=status,
        result_path=result_path,
        logs_path=logs_dir,
        run_workspace=run_workspace,
        setup_exit_code=_exit_code(setup_result),
        public_exit_code=public_exit_code,
        hidden_exit_code=hidden_exit_code,
        score_exit_code=hidden_exit_code,
        public_tests_passed=_tests_passed(public_exit_code),
        hidden_tests_passed=_tests_passed(hidden_exit_code),
        error_type=error_type,
    )


@dataclass(frozen=True)
class _TimeoutResult:
    returncode: int


def _run_command(
    *,
    command: str,
    cwd: Path,
    timeout_seconds: int,
    log_path: Path,
) -> subprocess.CompletedProcess[str] | _TimeoutResult:
    log_header = f"$ {command}\n\n"
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            executable="/bin/bash",
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        log_path.write_text(
            log_header
            + f"Command timed out after {timeout_seconds} seconds.\n\n"
            + "STDOUT:\n"
            + _decode_timeout_output(error.stdout)
            + "\nSTDERR:\n"
            + _decode_timeout_output(error.stderr),
            encoding="utf-8",
        )
        return _TimeoutResult(returncode=124)

    log_path.write_text(
        log_header
        + f"Exit code: {result.returncode}\n\n"
        + "STDOUT:\n"
        + result.stdout
        + "\nSTDERR:\n"
        + result.stderr,
        encoding="utf-8",
    )
    return result


def _exit_code(result: subprocess.CompletedProcess[str] | _TimeoutResult | None) -> int | None:
    if result is None:
        return None
    return result.returncode


def _tests_passed(exit_code: int | None) -> bool | None:
    if exit_code is None:
        return None
    return exit_code == 0


def _decode_timeout_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _ignore_generated_files(_directory: str, names: list[str]) -> set[str]:
    ignored = {"__pycache__", ".pytest_cache", ".venv"}
    return {
        name
        for name in names
        if name in ignored or name.endswith(".egg-info") or name.endswith(".pyc")
    }


def _ensure_workspace_venv_link(run_workspace: Path) -> None:
    workspace_venv = run_workspace / ".venv"
    repo_venv = run_workspace / "repo" / ".venv"
    if workspace_venv.exists() or not repo_venv.exists():
        return
    workspace_venv.symlink_to(repo_venv)


def _format_timestamp(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")
