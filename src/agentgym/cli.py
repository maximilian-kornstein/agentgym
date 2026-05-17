from __future__ import annotations

import argparse
import json
import tempfile
import sys
from datetime import UTC, datetime
from pathlib import Path

from .runner import run_task
from .tasks import discover_tasks, validate_task, validate_task_id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agentgym")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available tasks.")

    validate_parser = subparsers.add_parser("validate", help="Validate one task, or all tasks if no id is given.")
    validate_parser.add_argument("task_id", nargs="?")

    run_parser = subparsers.add_parser("run", help="Run a task in a temporary workspace.")
    run_parser.add_argument("task_id")
    run_parser.add_argument("--agent", help="Run an agent command in the task workspace before scoring.")

    run_suite_parser = subparsers.add_parser("run-suite", help="Run every discovered task.")
    run_suite_parser.add_argument("--agent", help="Run an agent command in each task workspace before scoring.")

    args = parser.parse_args(argv)

    if args.command == "list":
        return _list_tasks()
    if args.command == "validate":
        return _validate_task(args.task_id)
    if args.command == "run":
        return _run_task(args.task_id, args.agent)
    if args.command == "run-suite":
        return _run_suite(args.agent)

    parser.error(f"unknown command: {args.command}")
    return 2


def _list_tasks() -> int:
    tasks = discover_tasks()
    if not tasks:
        print("No tasks found.")
        return 0

    rows = [("id", "difficulty", "language", "title")]
    rows.extend((task.id, task.difficulty, task.language, task.title) for task in tasks)
    _print_table(rows)
    return 0


def _validate_task(task_id: str | None) -> int:
    if task_id is None:
        return _validate_all_tasks()

    task, errors = validate_task_id(task_id)
    if task is None:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    if errors:
        print(f"{task_id}: invalid", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{task_id}: valid")
    return 0


def _validate_all_tasks() -> int:
    tasks = discover_tasks()
    if not tasks:
        print("No tasks found.", file=sys.stderr)
        return 1

    invalid_count = 0
    for task in tasks:
        errors = validate_task(task)
        if errors:
            invalid_count += 1
            print(f"{task.id}: invalid", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
        else:
            print(f"{task.id}: valid")

    if invalid_count:
        print(f"{invalid_count} of {len(tasks)} tasks invalid", file=sys.stderr)
        return 1

    print(f"{len(tasks)} tasks valid")
    return 0


def _run_task(task_id: str, agent_command: str | None = None) -> int:
    task, errors = validate_task_id(task_id)
    if task is None or errors:
        if task is not None:
            print(f"{task_id}: invalid", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2

    result = run_task(task, agent_command=agent_command)
    print(f"Task: {task_id}")
    print(f"Status: {result.status}")
    if result.agent_command is not None:
        print(f"Agent: {_format_agent_status(result)}")
    print(f"Public tests: {_format_test_status(result.public_tests_passed)}")
    print(f"Hidden tests: {_format_test_status(result.hidden_tests_passed)}")
    print(f"Run workspace: {result.run_workspace}")
    print(f"Result: {result.result_path}")
    print(f"Logs: {result.logs_path}")
    if result.error_type:
        print(f"Error: {result.error_type}")
        if result.error_type == "hidden_tests_failed":
            print("Note: hidden_tests_failed can be expected for starter tasks.")
    return 0 if result.status == "pass" else 1


def _run_suite(agent_command: str | None = None) -> int:
    tasks = discover_tasks()
    if not tasks:
        print("No tasks found.", file=sys.stderr)
        return 1

    invalid_tasks = [(task, validate_task(task)) for task in tasks]
    invalid_tasks = [(task, errors) for task, errors in invalid_tasks if errors]
    if invalid_tasks:
        for task, errors in invalid_tasks:
            print(f"{task.id}: invalid", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
        return 2

    suite_dir = Path(tempfile.mkdtemp(prefix="agentgym-suite-"))
    suite_result_path = suite_dir / "suite_result.json"
    include_agent = agent_command is not None
    rows = [("id", "agent", "public", "hidden", "status")] if include_agent else [("id", "public", "hidden", "status")]
    failure_mode_rows = (
        [("failure_mode", "task", "agent", "public", "hidden", "status")]
        if include_agent
        else [("failure_mode", "task", "public", "hidden", "status")]
    )
    task_results = []
    failure_mode_results = []

    for task in tasks:
        result = run_task(task, agent_command=agent_command)
        primary_failure_mode = str(task.metadata["primary_failure_mode"])
        agent_status = _format_agent_status(result)
        public_status = _format_test_status(result.public_tests_passed)
        hidden_status = _format_test_status(result.hidden_tests_passed)
        if include_agent:
            rows.append((task.id, agent_status, public_status, hidden_status, result.status))
            failure_mode_rows.append(
                (primary_failure_mode, task.id, agent_status, public_status, hidden_status, result.status)
            )
        else:
            rows.append((task.id, public_status, hidden_status, result.status))
            failure_mode_rows.append((primary_failure_mode, task.id, public_status, hidden_status, result.status))
        task_results.append(
            {
                "task_id": task.id,
                "primary_failure_mode": primary_failure_mode,
                "status": result.status,
                "agent_command": result.agent_command,
                "agent_ran": result.agent_ran,
                "agent_exit_code": result.agent_exit_code,
                "public_tests_passed": result.public_tests_passed,
                "hidden_tests_passed": result.hidden_tests_passed,
                "result_path": str(result.result_path),
                "logs_path": str(result.logs_path),
                "run_workspace": str(result.run_workspace),
                "error_type": result.error_type,
            }
        )
        failure_mode_results.append(
            {
                "failure_mode": primary_failure_mode,
                "task_id": task.id,
                "status": result.status,
                "agent_command": result.agent_command,
                "agent_ran": result.agent_ran,
                "agent_exit_code": result.agent_exit_code,
                "public_tests_passed": result.public_tests_passed,
                "hidden_tests_passed": result.hidden_tests_passed,
                "error_type": result.error_type,
            }
        )

    _print_table(rows)

    public_pass_count = sum(1 for result in task_results if result["public_tests_passed"] is True)
    hidden_pass_count = sum(1 for result in task_results if result["hidden_tests_passed"] is True)
    agent_pass_count = (
        sum(1 for result in task_results if result["agent_ran"] is True and result["agent_exit_code"] == 0)
        if include_agent
        else None
    )
    total_count = len(task_results)
    print()
    if agent_pass_count is not None:
        print(f"{agent_pass_count}/{total_count} agent commands passed")
    print(f"{public_pass_count}/{total_count} tasks passed public tests")
    print(f"{hidden_pass_count}/{total_count} tasks passed hidden tests")
    print()
    print("Failure modes:")
    _print_table(failure_mode_rows)
    print(f"Suite result: {suite_result_path}")

    suite_data = {
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "total_tasks": total_count,
        "agent_command": agent_command,
        "agent_ran": include_agent,
        "agent_commands_passed": agent_pass_count,
        "public_tests_passed": public_pass_count,
        "hidden_tests_passed": hidden_pass_count,
        "tasks": task_results,
        "failure_modes": failure_mode_results,
    }
    suite_result_path.write_text(json.dumps(suite_data, indent=2) + "\n", encoding="utf-8")

    return 0 if hidden_pass_count == total_count else 1


def _print_table(rows: list[tuple[str, ...]]) -> None:
    widths = [max(len(row[index]) for row in rows) for index in range(len(rows[0]))]
    for row in rows:
        print("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)).rstrip())


def _format_test_status(value: bool | None) -> str:
    if value is None:
        return "not run"
    return "pass" if value else "fail"


def _format_agent_status(result) -> str:
    if not result.agent_ran:
        return "not run"
    return "pass" if result.agent_exit_code == 0 else "fail"


if __name__ == "__main__":
    raise SystemExit(main())
