# Methodology

AgentGym tasks are small executable repo problems designed to show a specific way a coding agent can fail.

The benchmark is not trying to measure whether an agent can satisfy a prompt in isolation. It measures whether an agent can inspect a repository, understand the intended behavior, make a focused code change, pass visible tests, and avoid a shallow fix that hidden tests catch.

## Task Model

Each task contains:

- a broken starter repository
- visible public tests
- hidden tests
- setup and scoring scripts
- task metadata
- a reference patch

The starter repository is intentionally incomplete. Public tests describe normal expected behavior. Hidden tests check the edge case or deeper rule that the task is actually about. The reference patch proves that the task is solvable with a small, intended fix.

## Why Public And Hidden Tests

Public tests make the task inspectable. They show the agent and human reader what the API is supposed to do.

Hidden tests make the task useful as an evaluation. They catch fixes that only satisfy the obvious examples while missing stricter behavior. A good task should create a clear split:

```text
public tests: pass
hidden tests: fail
```

That split means the starter code already handles the visible happy path, but still contains a realistic bug.

## Failure Modes

AgentGym is organized around failure modes, not just task count.

Each task should isolate one behavior pattern:

- missing input normalization
- unsafe type coercion
- missing cross-field validation
- leaking internal fields during serialization

This makes results easier to interpret. If an agent fails a task, the failure should say something concrete about the kind of engineering judgment it missed.

## Task Quality Bar

A task should be accepted only if it is:

- deterministic
- small enough to inspect quickly
- realistic enough to resemble repository work
- focused on one primary bug
- executable with local commands
- free of network dependencies
- verifiable by a reference patch

The starter code should pass public tests and fail hidden tests for the intended reason. The reference patch should pass both public and hidden tests.

## Run Interpretation

`agentgym run <task_id>` executes a task in a temporary copy so the source task stays unchanged.

The important result fields are:

- `public_tests_passed`
- `hidden_tests_passed`
- `error_type`

For the current starter tasks, the expected result is:

```json
{
  "public_tests_passed": true,
  "hidden_tests_passed": false,
  "error_type": "hidden_tests_failed"
}
```

That is not a broken benchmark run. It is the intended baseline for an unfixed starter repository.

## Current Scope

AgentGym v0.1 is deliberately narrow:

- synthetic Python API tasks
- local pytest-based scoring
- no Docker
- no agent invocation
- no leaderboard
- public hidden-test files in the open-source repository

The current goal is to prove the task format, scoring loop, and failure-mode taxonomy before adding heavier infrastructure.

## Limitations

Because the current tasks are synthetic and open source, they are best used for development, smoke testing, and public methodology work. They are not yet a contamination-resistant leaderboard benchmark.

Future private or generated task packs can use the same task format while keeping grader tests unseen.

## Next Method Steps

The next useful improvements are:

- add more tasks in the same Python API family
- keep mapping each task to a named failure mode
- summarize suite results by public-pass and hidden-pass rates
- add an optional agent command hook after the task set is stable
- explore private task packs after the public format is proven
