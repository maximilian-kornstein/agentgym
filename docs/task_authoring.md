# AgentGym Task Authoring Guide

AgentGym tasks should feel like real software engineering work, not puzzle prompts. A good task gives an agent a broken repository, visible tests that describe normal behavior, hidden tests that catch shallow fixes, and a reference patch that proves the intended solution.

## Task Anatomy

Each task directory must contain:

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

- `task.yaml` describes the task and commands.
- `README.md` is the prompt a coding agent or human sees.
- `repo/` contains the broken starter repository.
- `tests/` contains public tests.
- `hidden_tests/` contains grader tests.
- `setup.sh` installs task dependencies.
- `score.sh` runs public and hidden checks.
- `solution.patch` is the reference fix.

## Metadata

Each task must include `primary_failure_mode` in `task.yaml`. This should be a short stable label used by suite summaries, such as `input-normalization`, `cross-field-validation`, or `partial-update-semantics`.

Keep `failure_modes` as secondary tags for broader classification.

## Quality Bar

Accept a task only if:

- The starter repo fails hidden scoring for one clear reason.
- Public tests pass or mostly guide normal behavior.
- Hidden tests check behavior not fully covered by public tests.
- The reference patch applies cleanly and passes all checks.
- The fix requires changing product code, not test expectations.
- The task can be understood in 5-10 minutes.
- The task completes in under the configured timeout.
- The task does not depend on network access.
- The task has a realistic failure mode agents might make in production code.

Reject a task if:

- It is solved by hardcoding a single test value.
- Hidden tests are just duplicates of public tests.
- The intended fix is ambiguous.
- The setup is flaky or slow.
- The repository is large enough to distract from the target bug.

## Public Tests Vs Hidden Tests

Public tests should:

- Explain the expected API behavior.
- Cover normal successful requests.
- Cover at least one obvious validation failure.
- Avoid revealing every edge case.

Hidden tests should:

- Catch shallow fixes.
- Cover edge cases implied by the task README.
- Verify the reference patch, not a specific implementation.
- Avoid testing private helper names unless the helper is the public surface.

For `python-api-001`, public tests cover ordinary normalization and missing fields. Hidden tests catch whitespace-only required fields.

## Verification Checklist

Before accepting a task:

1. Run `agentgym validate <task_id>` and confirm it passes.
2. Run `agentgym run <task_id>` and confirm the starter task fails for the intended hidden-test reason.
3. Copy the task to a temporary location.
4. In the copied task, run `./setup.sh`.
5. Apply `patch -p0 < solution.patch`.
6. Run `./score.sh` and confirm all checks pass.
7. Confirm no generated files are left in the source task directory.
8. Read the task README as if you were an agent and remove any unnecessary hints.

## Naming

Use stable, sequential task IDs:

```text
python-api-001
python-api-002
python-api-003
```

For the first mini-benchmark, keep tasks in the Python API-validation family so results are comparable.
