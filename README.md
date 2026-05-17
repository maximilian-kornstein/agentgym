# AgentGym

AgentGym is a small, executable benchmark for testing coding agents on realistic repository tasks.

The goal is to measure where agents still fail at real software engineering work: reading code, making a focused fix, passing visible tests, and surviving hidden checks that catch shallow patches.

## Current Status

AgentGym is intentionally small:

- Ten Python API tasks: `tasks/python-api-001`, `tasks/python-api-002`, `tasks/python-api-003`, `tasks/python-api-004`, `tasks/python-api-005`, `tasks/python-api-006`, `tasks/python-api-007`, `tasks/python-api-008`, `tasks/python-api-009`, and `tasks/python-api-010`.
- A local CLI for discovery, validation, and temporary-workspace execution.
- Public tests, hidden tests, deterministic scoring, and a reference patch.
- Authoring docs for creating the next Python API tasks.

The first task is a synthetic Python API bug: a profile payload validator mishandles whitespace-only required fields. The second task checks a nested notification-preferences payload that coerces non-boolean values too permissively. The third task checks a cross-field account/tax-id rule. The fourth task checks response serialization that leaks internal user fields. The fifth task checks search pagination and sort boundary validation. The sixth task checks PATCH-style partial update semantics. The seventh task checks idempotency-key handling for duplicate payment requests. The eighth task checks layered service configuration precedence. The ninth task checks timezone-aware booking-window validation. The tenth task checks document access authorization scope. All ten are small enough to inspect quickly, but real enough to demonstrate the benchmark loop.

## Quickstart

Requires Python 3.11+.

Clone the repo and install the CLI:

```bash
git clone https://github.com/maximilian-kornstein/agentgym.git
cd agentgym
python3 -m pip install -e .
```

List available tasks:

```bash
agentgym list
```

Validate all tasks:

```bash
agentgym validate
```

Validate one task:

```bash
agentgym validate python-api-001
```

Run a task in a temporary workspace:

```bash
agentgym run python-api-001
```

This run is expected to fail. The starter code passes public tests but fails hidden tests, which is the point of the golden task. The CLI prints the temporary run workspace and writes `.agentgym/result.json` inside that workspace.

Run a task with an agent command:

```bash
agentgym run python-api-001 --agent "<command>"
```

The agent command runs inside the copied task workspace after setup and before scoring. It does not run in, or mutate, the source task directory.

For a concrete smoke test, run the reference patch as the agent command:

```bash
agentgym run python-api-001 --agent "patch -p0 < solution.patch"
```

This applies the patch only inside the temporary workspace. The source task remains unchanged, and both public and hidden tests should pass.

Run every task:

```bash
agentgym run-suite
```

Run every task with the same agent command:

```bash
agentgym run-suite --agent "<command>"
```

The command runs once per copied task workspace. If it fails on one task, the suite records that task failure and continues evaluating the rest.

If your shell cannot find the `agentgym` command after installation, use the module form:

```bash
python3 -m agentgym.cli list
python3 -m agentgym.cli validate
python3 -m agentgym.cli validate python-api-001
python3 -m agentgym.cli run python-api-001
python3 -m agentgym.cli run python-api-001 --agent "<command>"
python3 -m agentgym.cli run-suite
python3 -m agentgym.cli run-suite --agent "<command>"
```

Run AgentGym's package tests:

```bash
python3 -m pip install -e '.[dev]'
python3 -m pytest
```

## What The CLI Does

- `agentgym list` shows available tasks.
- `agentgym validate` checks metadata and required files for every task.
- `agentgym validate <task_id>` checks metadata and required files for one task.
- `agentgym run <task_id>` copies the task into a temporary workspace, runs setup and scoring there, captures logs, and leaves the source task untouched.
- `agentgym run <task_id> --agent "<command>"` runs a trusted local command inside the copied task workspace before public and hidden tests.
- `agentgym run-suite` runs every task and writes a suite-level JSON summary.
- `agentgym run-suite --agent "<command>"` runs the same trusted local command once per copied task workspace and records agent/public/hidden results.

AgentGym can optionally run a trusted local agent command for a single task or across the suite. It does not include Docker isolation, a model registry, or a leaderboard yet.

## Manual Task Verification

You can also run the task directly:

```bash
cd tasks/python-api-001
./setup.sh
./score.sh
```

The starter repository should fail hidden scoring. To verify the reference fix:

```bash
cd tasks/python-api-001
patch -p0 < solution.patch
./score.sh
```

After applying the reference patch, all public and hidden tests should pass.

## Task Structure

Each AgentGym task is a directory with:

```text
task.yaml
README.md
repo/
tests/
hidden_tests/
setup.sh
score.sh
solution.patch
```

- `repo/` contains the broken starter code.
- `tests/` contains visible public tests.
- `hidden_tests/` contains grader tests that catch shallow fixes.
- `setup.sh` installs dependencies for the task.
- `score.sh` runs public and hidden tests.
- `solution.patch` is the reference fix used to verify the task.

See `docs/v0.1_report.md` for the dated v0.1 benchmark snapshot and `docs/v0.2_report.md` for the 10-task suite snapshot. See `docs/methodology.md` for the benchmark method. See `docs/failure_modes.md` for the current failure-mode map. See `docs/task_authoring.md` for the task quality bar and authoring checklist. See `docs/python_api_task_template.md` for the recommended shape of new Python API tasks.

## Roadmap

1. Run real coding-agent commands against the 10-task suite.
2. Add result summarization for suite runs.
3. Explore private or generated task packs.
4. Expand beyond Python API tasks after the public format stays stable.

See `AGENTGYM_PRD.md` for the full product plan.
