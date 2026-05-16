from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


REQUIRED_METADATA_FIELDS = {
    "id",
    "title",
    "language",
    "domain",
    "difficulty",
    "description",
    "setup_command",
    "public_test_command",
    "hidden_test_command",
    "score_command",
    "timeout_seconds",
}

REQUIRED_FILES = {
    "task.yaml",
    "README.md",
    "repo",
    "tests",
    "hidden_tests",
    "setup.sh",
    "score.sh",
    "solution.patch",
}


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    language: str
    difficulty: str
    path: Path
    metadata: dict[str, Any]


def project_root() -> Path:
    env_root = os.environ.get("AGENTGYM_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def tasks_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "tasks"


def discover_tasks(root: Path | None = None) -> list[Task]:
    root = root or project_root()
    base_dir = tasks_dir(root)
    if not base_dir.exists():
        return []

    discovered: list[Task] = []
    for task_yaml in sorted(base_dir.glob("*/task.yaml")):
        metadata = load_metadata(task_yaml)
        discovered.append(
            Task(
                id=str(metadata.get("id", task_yaml.parent.name)),
                title=str(metadata.get("title", "")),
                language=str(metadata.get("language", "")),
                difficulty=str(metadata.get("difficulty", "")),
                path=task_yaml.parent,
                metadata=metadata,
            )
        )
    return discovered


def find_task(task_id: str, root: Path | None = None) -> Task | None:
    for task in discover_tasks(root):
        if task.id == task_id:
            return task
    return None


def load_metadata(task_yaml: Path) -> dict[str, Any]:
    with task_yaml.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        return {}
    return data


def validate_task(task: Task) -> list[str]:
    errors: list[str] = []
    metadata = task.metadata

    missing_fields = sorted(REQUIRED_METADATA_FIELDS.difference(metadata))
    for field_name in missing_fields:
        errors.append(f"missing required metadata field: {field_name}")

    if metadata.get("id") != task.path.name:
        errors.append(
            f"metadata id must match task directory name: {metadata.get('id')!r} != {task.path.name!r}"
        )

    timeout = metadata.get("timeout_seconds")
    if not isinstance(timeout, int) or timeout <= 0:
        errors.append("timeout_seconds must be a positive integer")

    for command_field in ("setup_command", "public_test_command", "hidden_test_command", "score_command"):
        command = metadata.get(command_field)
        if command_field in metadata and (not isinstance(command, str) or not command.strip()):
            errors.append(f"{command_field} must be a non-empty string")

    for required_file in sorted(REQUIRED_FILES):
        if not (task.path / required_file).exists():
            errors.append(f"missing required file or directory: {required_file}")

    return errors


def validate_task_id(task_id: str, root: Path | None = None) -> tuple[Task | None, list[str]]:
    task = find_task(task_id, root)
    if task is None:
        return None, [f"unknown task id: {task_id}"]
    return task, validate_task(task)
