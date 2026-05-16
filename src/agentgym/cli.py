from __future__ import annotations

import argparse
import sys

from .runner import run_task
from .tasks import discover_tasks, validate_task, validate_task_id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agentgym")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available tasks.")

    validate_parser = subparsers.add_parser("validate", help="Validate a task.")
    validate_parser.add_argument("task_id")

    run_parser = subparsers.add_parser("run", help="Run a task in a temporary workspace.")
    run_parser.add_argument("task_id")

    args = parser.parse_args(argv)

    if args.command == "list":
        return _list_tasks()
    if args.command == "validate":
        return _validate_task(args.task_id)
    if args.command == "run":
        return _run_task(args.task_id)

    parser.error(f"unknown command: {args.command}")
    return 2


def _list_tasks() -> int:
    tasks = discover_tasks()
    if not tasks:
        print("No tasks found.")
        return 0

    for task in tasks:
        print(f"{task.id}\t{task.title}\t{task.language}\t{task.difficulty}")
    return 0


def _validate_task(task_id: str) -> int:
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


def _run_task(task_id: str) -> int:
    task, errors = validate_task_id(task_id)
    if task is None or errors:
        if task is not None:
            print(f"{task_id}: invalid", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2

    result = run_task(task)
    print(f"Task: {task_id}")
    print(f"Status: {result.status}")
    print(f"Run workspace: {result.run_workspace}")
    print(f"Result: {result.result_path}")
    print(f"Logs: {result.logs_path}")
    if result.error_type:
        print(f"Error: {result.error_type}")
        if result.error_type == "score_failed":
            print("Note: score_failed can be expected for starter tasks that fail hidden tests.")
    return 0 if result.status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
