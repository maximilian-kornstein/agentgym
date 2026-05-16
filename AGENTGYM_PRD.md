# AgentGym PRD

## Problem Statement

Coding agents are improving quickly, but public benchmarks often fail to show where they still break on realistic software engineering work. Many benchmarks are static, saturated, contaminated, too toy-like, or missing the execution environment needed to measure real agent behavior. Builders, researchers, and model labs need harder, fresher, executable tasks that expose concrete failure modes: poor codebase navigation, shallow patches, brittle test fixes, bad tool use, missed edge cases, dependency confusion, and inability to complete multi-step repo work.

AgentGym will start as a focused summer project: a public, rigorous benchmark for coding agents built from executable repository tasks with hidden tests, trace logs, deterministic scoring, and failure analysis. The first goal is not to compete with Scale AI as an enterprise vendor. The first goal is to build an undeniable artifact that proves taste, technical ability, and insight into the next bottleneck in AI training: realistic environments where agents can practice, fail, and improve.

## Solution

AgentGym is an open-source benchmark and task runner for evaluating coding agents on realistic repository tasks.

The MVP will support a narrow, high-quality benchmark:

- 30-50 curated coding-agent tasks.
- Dockerized or containerized task execution.
- A standard task format.
- Public tests plus hidden tests.
- Automatic scoring.
- Agent run logs and trace capture.
- Failure taxonomy.
- Basic leaderboard.
- Technical report explaining where agents fail.

The long-term vision is to evolve AgentGym from a benchmark into a training-environment foundry: a system that generates, validates, runs, scores, and analyzes realistic software engineering tasks for use in evals, supervised fine-tuning, reinforcement learning, regression testing, and model release gating.

## Product Principles

- Quality over task count. Fifty excellent tasks are better than five thousand noisy ones.
- Deterministic grading first. Unit tests, integration tests, static checks, and verifiers should carry more weight than AI judging.
- Realistic repo work. Tasks should require reading code, understanding constraints, editing files, and passing hidden checks.
- Transparent failures. The benchmark should explain why agents fail, not only report pass rates.
- Build in public. Progress should be visible through GitHub, X posts, reports, and small releases.
- Small enough to finish. Every milestone should be achievable by one highly focused builder with AI assistance.
- Neutral and credible. Avoid hype, fake enterprise positioning, and claims that cannot be measured.

## Target Users

1. Coding-agent builders who need harder evals.
2. AI researchers studying agent behavior.
3. Open-source model teams evaluating coding performance.
4. Devtools companies building agentic coding products.
5. Frontier labs looking for signals about long-horizon coding-agent weaknesses.
6. Students and independent builders who want to compare agents on realistic tasks.

## User Stories

1. As a coding-agent builder, I want executable tasks with hidden tests, so that I can measure whether my agent actually fixed the problem.
2. As a researcher, I want trace logs for each run, so that I can study where agents fail.
3. As a benchmark user, I want a standard task format, so that I can add new tasks without reverse-engineering the system.
4. As a model evaluator, I want deterministic scoring, so that results are reproducible and defensible.
5. As an open-source contributor, I want clear task authoring docs, so that I can contribute new tasks.
6. As an agent developer, I want tasks grouped by difficulty, so that I can test incremental improvements.
7. As an agent developer, I want tasks grouped by failure type, so that I can target specific weaknesses.
8. As a benchmark maintainer, I want automated task validation, so that broken tasks do not enter the benchmark.
9. As a benchmark maintainer, I want hidden tests separated from public tests, so that agents cannot pass through shallow overfitting.
10. As a benchmark maintainer, I want each task to include a reference solution, so that task validity can be audited.
11. As a benchmark maintainer, I want each task to include metadata, so that results can be filtered by language, domain, difficulty, and skill.
12. As a model lab, I want fresh private tasks eventually, so that benchmark contamination is less likely.
13. As a user comparing agents, I want a leaderboard, so that I can see relative performance.
14. As a serious evaluator, I want leaderboard submissions to include logs, so that results are not just unverified claims.
15. As a benchmark reader, I want a technical report, so that I can understand the meaning behind the numbers.
16. As a task author, I want a local runner, so that I can test a task before publishing it.
17. As a task author, I want templates for Python and TypeScript tasks, so that task creation is faster.
18. As a task author, I want a checklist for task quality, so that weak tasks are rejected early.
19. As an agent developer, I want scoring to produce machine-readable results, so that I can integrate AgentGym into CI.
20. As an agent developer, I want each run to produce a summary JSON file, so that I can analyze performance over time.
21. As a maintainer, I want a reproducible environment for each task, so that results do not depend on a user's machine.
22. As a user, I want clear setup instructions, so that I can run the benchmark without personal help.
23. As a researcher, I want failure categories, so that I can compare weaknesses across agents.
24. As a researcher, I want failed trajectories preserved, so that I can inspect bad reasoning or bad tool use.
25. As a researcher, I want successful trajectories preserved, so that I can compare efficient and inefficient solutions.
26. As a maintainer, I want a simple website, so that the project has a credible public home.
27. As a builder following on X, I want short progress updates, so that I can understand what changed each week.
28. As a potential collaborator, I want a roadmap, so that I can see where help is needed.
29. As a potential sponsor, I want evidence of traction and rigor, so that I can justify supporting the project.
30. As a future customer, I want proof that AgentGym exposes model weaknesses missed by existing benchmarks, so that I can trust the team.

## Scope

### MVP Scope

The MVP includes:

- Command-line runner.
- Standard task schema.
- Local Docker-based execution.
- 10 initial tasks.
- Public tests and hidden tests.
- JSON result output.
- Basic run logs.
- Task validation command.
- Documentation for running and authoring tasks.

### Summer Launch Scope

The summer launch includes:

- 30-50 high-quality tasks.
- At least two language/domain categories, preferably Python backend and TypeScript/JavaScript.
- Basic leaderboard.
- Run trace artifacts.
- Failure taxonomy.
- Static project website.
- Public technical report.
- Build-in-public content cadence.

### Post-Launch Scope

Post-launch includes:

- Private task packs.
- Better trace viewer.
- Hosted run service.
- Agent adapter API.
- Automated task generation candidates.
- Expert review workflow.
- Advanced curriculum and failure analysis.
- Paid pilots with small AI labs or coding-agent startups.

## Non-Goals

- Do not start by building a general data-labeling marketplace.
- Do not start by selling to frontier labs before there is a strong artifact.
- Do not start with every programming language.
- Do not depend on expensive model calls for the core benchmark to work.
- Do not use AI judges as the primary scoring method.
- Do not build a complex web app before the runner and tasks are excellent.
- Do not chase task volume at the cost of task quality.
- Do not claim to measure all software engineering ability.

## Success Metrics

### MVP Success

- 10 tasks can be run locally end-to-end.
- Each task has deterministic scoring.
- Each task has a reference solution.
- Each task has at least one hidden test.
- The runner outputs valid machine-readable results.
- A new user can run one task using the README.

### Summer Success

- 30-50 tasks published.
- At least 5 agents or model setups evaluated.
- At least 1 technical report published.
- At least 20 meaningful GitHub stars or 5 serious external contributors, whichever comes first.
- At least 3 credible builders, researchers, or AI engineers give feedback.
- At least 1 small lab, startup, or research group asks about private tasks or collaboration.

### Quality Success

- Tasks fail weak agents for meaningful reasons.
- Hidden tests catch shallow fixes.
- Failures are categorized, not just counted.
- At least 80% of tasks pass validation reliably on a clean machine.
- Leaderboard results are reproducible from submitted artifacts.

## Core Concepts

### Task

A task is a self-contained coding challenge based on a repository snapshot and a realistic issue. It defines the start state, allowed tools, tests, hidden tests, scoring logic, metadata, and expected fix.

### Environment

An environment is the isolated runtime where an agent attempts a task. It should be reproducible, disposable, and safe.

### Run

A run is one attempt by one agent on one task. It produces logs, changed files, test results, score, duration, and metadata.

### Trace

A trace is the record of the agent's actions during a run. In the MVP, traces can be simple logs. Later, traces can include structured command events, file diffs, tool calls, and browser actions.

### Verifier

A verifier is a deterministic check that determines whether the task was solved. Examples include tests, lint, typecheck, integration checks, and custom scoring scripts.

### Failure Taxonomy

A failure taxonomy is a set of labels explaining why an agent failed. Initial categories:

- Did not understand task.
- Edited wrong file.
- Broke existing behavior.
- Passed public tests but failed hidden tests.
- Hardcoded test-specific behavior.
- Dependency/setup failure.
- Timeout.
- Syntax/type error.
- Incomplete implementation.
- Overly broad refactor.
- Security or unsafe behavior.
- Tool-use failure.

## Standard Task Format

Each task should be stored as a directory with a predictable structure:

```text
tasks/
  python-api-001/
    task.yaml
    README.md
    repo/
    tests/
    hidden_tests/
    solution.patch
    setup.sh
    score.sh
```

Required task metadata:

- id
- title
- language
- domain
- difficulty
- estimated_human_minutes
- tags
- description
- setup_command
- test_command
- hidden_test_command
- score_command
- timeout_seconds
- allowed_tools
- failure_modes

Optional metadata:

- source_repo
- source_license
- issue_url
- commit_hash
- reference_files
- hints
- known_agent_failures
- contamination_risk

## Required Modules

### 1. CLI Runner

The CLI runner is the main interface for local execution.

Required commands:

- `agentgym list`
- `agentgym run <task_id>`
- `agentgym validate <task_id>`
- `agentgym run-suite`
- `agentgym summarize <results_dir>`

Responsibilities:

- Load task metadata.
- Create an isolated task workspace.
- Run setup.
- Invoke the agent command or manual mode.
- Run public and hidden checks.
- Capture logs.
- Write result JSON.
- Return a clear pass/fail status.

### 2. Task Schema

The task schema defines what every task must include.

Responsibilities:

- Validate required fields.
- Validate command definitions.
- Validate task IDs.
- Validate timeouts.
- Validate file presence.
- Validate allowed task categories.

### 3. Sandbox Runtime

The sandbox runtime executes tasks safely and reproducibly.

MVP approach:

- Use Docker locally.
- Mount task workspace.
- Disable unnecessary host access.
- Apply per-task timeout.
- Capture stdout/stderr.

Future approach:

- Ephemeral cloud containers.
- Network policy controls.
- Resource limits.
- Replayable environment snapshots.

### 4. Scoring System

The scoring system determines whether a task passed.

MVP scoring:

- public tests pass/fail
- hidden tests pass/fail
- score script exit code
- timeout status
- changed files summary

Future scoring:

- partial credit
- multi-stage scoring
- performance checks
- security checks
- style constraints
- trace quality metrics

### 5. Trace Capture

The trace system records what happened during a run.

MVP:

- command output logs
- final diff
- test output
- duration
- exit codes

Future:

- structured tool-call events
- file read/write events
- shell command sequence
- browser actions
- replay viewer

### 6. Task Authoring Tools

Task authoring tools help create and validate new tasks.

MVP:

- templates
- validation command
- task quality checklist
- example task

Future:

- task generator from GitHub issue/commit
- mutation-based hidden test suggestions
- AI-assisted task drafts
- expert review queue

### 7. Leaderboard

The leaderboard shows benchmark results.

MVP:

- static Markdown or simple website table
- agent name
- version/date
- total pass rate
- pass rate by difficulty
- pass rate by language/domain
- link to result artifacts

Future:

- hosted submissions
- verified runs
- trace explorer
- anti-cheat checks
- private leaderboard support

### 8. Documentation

Documentation is part of the product.

Required docs:

- project overview
- quickstart
- task format
- how to run a task
- how to add a task
- scoring rules
- leaderboard rules
- contribution guide
- task quality checklist
- build-in-public roadmap

### 9. Static Website

The website gives AgentGym a credible public home.

MVP content:

- what AgentGym measures
- why it exists
- how to run it
- current results
- example task
- technical report link
- contribution link

Avoid marketing fluff. The first screen should show the benchmark and results, not a vague landing page.

## Technical Architecture

### MVP Architecture

AgentGym should begin as a Python CLI package because Python is strong for scripting, test orchestration, YAML parsing, Docker invocation, and data analysis.

Recommended stack:

- Python CLI with Typer or argparse.
- Pydantic or dataclasses for task schema validation.
- PyYAML or ruamel.yaml for YAML parsing.
- Docker for execution.
- pytest for Python task examples.
- Node/npm support for TypeScript tasks.
- JSON Lines or JSON for result output.
- Static site generated from Markdown or a lightweight frontend later.

The first implementation should optimize for simplicity and reliability over framework complexity.

### Future Architecture

Future hosted architecture:

- API service for run submissions.
- Worker queue for environment execution.
- Container orchestration.
- Object storage for logs/traces.
- Database for tasks, runs, agents, and leaderboard entries.
- Web UI for traces and analytics.
- Auth for private task packs.

Do not build this until the local benchmark is credible.

## Data Model

### Task Result

Each run should write a result JSON object with:

- run_id
- task_id
- agent_name
- agent_version
- started_at
- completed_at
- duration_seconds
- status
- public_tests_passed
- hidden_tests_passed
- score
- timeout
- error_type
- failure_category
- changed_files
- logs_path
- diff_path
- environment_hash

### Leaderboard Entry

Each leaderboard entry should include:

- agent_name
- agent_version
- benchmark_version
- run_date
- total_tasks_attempted
- total_tasks_passed
- pass_rate
- pass_rate_by_difficulty
- pass_rate_by_language
- pass_rate_by_failure_mode
- artifacts_url
- verification_status

## Task Quality Bar

A task is acceptable only if:

- It represents a realistic software engineering problem.
- It can be run from a clean environment.
- It has deterministic scoring.
- It includes hidden tests that check real behavior.
- It has a reference solution.
- It has a clear failure mode.
- It is not solved by changing only a test expectation.
- It is not solved by hardcoding one literal output unless that is the intended task.
- It can complete within a reasonable timeout.
- It has license/source information if derived from open-source code.

## Initial Task Categories

Start with Python backend tasks because setup and scoring are straightforward.

Initial categories:

1. API behavior bug.
2. Input validation bug.
3. Serialization/deserialization bug.
4. Date/time edge case.
5. Database query or migration bug.
6. Authentication/authorization logic bug.
7. Caching bug.
8. Error handling bug.
9. Type handling bug.
10. Regression caused by incomplete refactor.

Second category:

1. TypeScript utility bug.
2. React component behavior bug.
3. API client bug.
4. Form validation bug.
5. State management bug.
6. Edge-case rendering bug.

Avoid frontend visual tasks in the first MVP unless screenshots and deterministic checks are already working.

## Ordered Build Plan

### Phase 0: Project Definition

Goal: Make the project concrete.

Deliverables:

- Name selected.
- GitHub repository created.
- README draft.
- Task format draft.
- Roadmap published.
- First build-in-public post.

Exit criteria:

- A stranger can understand what AgentGym is in under one minute.

### Phase 1: One Manual Golden Task

Goal: Prove one task can run end-to-end.

Deliverables:

- One Python repo task.
- Public tests.
- Hidden tests.
- Reference solution patch.
- Manual setup script.
- Manual scoring script.
- Result artifact example.

Exit criteria:

- A human can clone the repo, run the task, apply the reference patch, and pass scoring.

### Phase 2: CLI Runner MVP

Goal: Replace manual steps with a repeatable command.

Deliverables:

- `agentgym run <task_id>`
- task metadata loader
- workspace copy
- setup execution
- public test execution
- hidden test execution
- result JSON
- logs directory

Exit criteria:

- The first task runs from one command and produces a result JSON.

### Phase 3: Task Schema And Validation

Goal: Prevent broken tasks from entering the benchmark.

Deliverables:

- `task.yaml` schema.
- `agentgym validate <task_id>`.
- validation errors with clear messages.
- sample valid task.
- sample invalid task fixtures.

Exit criteria:

- Missing files, invalid commands, duplicate IDs, and malformed metadata are caught automatically.

### Phase 4: First 10 Tasks

Goal: Build the first credible mini-benchmark.

Deliverables:

- 10 high-quality Python tasks.
- reference patches.
- hidden tests.
- metadata.
- task quality review.
- one baseline result set.

Exit criteria:

- All 10 tasks validate and run on a clean machine.

### Phase 5: Agent Adapter And Manual Mode

Goal: Let different agents attempt tasks.

Deliverables:

- manual mode for human/agent editing.
- command-based agent invocation.
- environment variables for agent commands.
- final diff capture.
- timeout handling.

Exit criteria:

- At least two different agent workflows can attempt the same task.

### Phase 6: Trace And Failure Analysis

Goal: Make results explainable.

Deliverables:

- final diff artifact.
- command/test logs.
- failure category field.
- simple failure tagging process.
- summary report generator.

Exit criteria:

- For each failed task, the maintainer can assign a meaningful failure category.

### Phase 7: Public Mini-Release

Goal: Ship something real.

Deliverables:

- GitHub repo public.
- 10-task benchmark.
- quickstart.
- task authoring docs.
- first leaderboard table.
- short report: "What coding agents fail on in AgentGym v0.1."

Exit criteria:

- External users can run the benchmark and understand the results.

### Phase 8: Expand To 30-50 Tasks

Goal: Make it substantial enough to matter.

Deliverables:

- 30-50 tasks total.
- at least two difficulty levels.
- at least two language/domain groups if quality allows.
- improved hidden tests.
- additional baseline runs.

Exit criteria:

- Results show meaningful spread between agents and meaningful failure clusters.

### Phase 9: Website And Leaderboard

Goal: Make the project legible and credible.

Deliverables:

- static website.
- results page.
- task examples page.
- methodology page.
- leaderboard rules.
- report page.

Exit criteria:

- A visitor can understand the benchmark, inspect results, and run it locally.

### Phase 10: Serious Public Report

Goal: Turn the benchmark into a reputation-building artifact.

Deliverables:

- 8-15 page technical report.
- methodology.
- task categories.
- model/agent results.
- top failure modes.
- examples of failures.
- limitations.
- next roadmap.

Exit criteria:

- The report is credible enough to send to AI researchers, coding-agent companies, and devtools founders.

### Phase 11: Private Task Pack Exploration

Goal: Test whether this can become a company.

Deliverables:

- private pack proposal.
- sample private task format.
- outreach list.
- 10 private/unreleased tasks.
- pilot offer.

Exit criteria:

- At least one serious organization agrees to discuss a pilot or collaboration.

## Build-In-Public Plan

Post 2-3 times per week on X.

Content types:

- task of the week
- failure mode breakdown
- hidden test caught a shallow fix
- leaderboard update
- what changed this week
- "agent solved this in a weird way"
- "this task was too flaky, here is how I fixed it"
- report snippets

Tone:

- technical
- humble
- specific
- non-hype
- evidence-based

Initial post:

```text
This summer I am building AgentGym: a small, executable benchmark for coding agents.

Goal: 50 realistic repo tasks with hidden tests, automatic scoring, run logs, and failure analysis.

I want to understand where agents still fail at real software engineering, not just toy problems.

Starting with Python backend bugs. Building in public.
```

## Competitive Positioning

AgentGym should not position itself as a Scale AI competitor at first. It should position itself as a credible public benchmark for realistic coding-agent evaluation.

The deeper strategic path is:

1. Public benchmark.
2. Reputation.
3. Private task packs.
4. Training/eval infrastructure.
5. Paid pilots.
6. Long-term environment foundry.

This avoids competing on labor scale and instead competes on rigor, neutrality, task quality, and training-loop value.

## Cost Strategy

Keep costs low by:

- using public/open-source repos
- running locally
- avoiding paid cloud until necessary
- using Docker instead of managed execution infrastructure
- using static hosting
- manually curating the first tasks
- using AI assistance for drafts and tests, followed by human review
- avoiding expensive model sweeps early
- asking external agent builders to run submissions
- keeping the first website static

Expected early costs:

- Domain name: optional.
- GitHub: free.
- Static hosting: free.
- Docker/local compute: free except electricity.
- Model/API calls: optional and capped.
- Legal/company costs: defer until there is real commercial interest.

## Legal And Safety Notes

Because the founder is under 18, real contracts, paid pilots, NDAs, banking, company formation, and customer agreements may require a parent or guardian. This is not a blocker for building the public benchmark, but it matters before accepting payments or signing agreements.

Open-source tasks must respect licenses. Any task derived from an existing repository should track source, license, and commit hash. Avoid copying proprietary code. For private customer tasks later, use clear data agreements, retention policies, and isolation.

The benchmark should avoid tasks that meaningfully enable offensive cyber abuse. Security tasks can be considered later, but the first version should focus on ordinary software engineering.

## Testing Decisions

Good tests should validate external behavior, not internal implementation details. Tests should catch shallow fixes and confirm that the task's intended behavior works under realistic edge cases.

Modules that need tests:

- task schema validation
- CLI command behavior
- result JSON generation
- task discovery
- workspace setup
- scoring behavior
- timeout handling
- summary generation

Task tests:

- every task must have public tests
- every task must have hidden tests
- every task must pass with the reference solution
- every task should fail from the initial state
- hidden tests should verify behavior not covered by public tests

System tests:

- run one known passing task end-to-end
- run one known failing task end-to-end
- validate a malformed task
- generate summary results from sample outputs

## Out Of Scope For V0.1

- Hosted cloud execution.
- User accounts.
- Paid subscriptions.
- Private customer data.
- Full trace replay UI.
- Browser-based tasks.
- Cybersecurity tasks.
- RL training integration.
- Automatic task generation at scale.
- Enterprise security compliance.
- SOC 2.
- Formal company formation unless needed.

## Open Questions

- Should AgentGym start with Python only, or Python plus TypeScript?
- Should the first tasks use synthetic mini-repos, real open-source repos, or a mix?
- Which coding agents should be evaluated first?
- Should the leaderboard allow self-reported runs initially?
- How strict should submission verification be for the first public release?
- Should the project name remain AgentGym or move to PatchBench/RepoBench?
- Should the first public report compare specific agents, or focus more generally on failure modes?

## Recommended Answers To Open Questions

- Start with Python only for the first 10 tasks.
- Use synthetic-but-realistic repos first, then carefully add open-source-derived tasks.
- Evaluate whatever is accessible and affordable first.
- Allow self-reported runs only if artifacts are included.
- Keep leaderboard verification simple at first: logs, result JSON, commit hash, and environment info.
- Keep AgentGym unless a naming conflict appears.
- Make the first report failure-mode-first, with agent comparisons as supporting evidence.

## Milestone Timeline

### Week 1

- Create repo.
- Finalize task schema v0.
- Build one manual task.
- Publish first X post.

### Week 2

- Implement CLI runner.
- Add result JSON output.
- Add logs.
- Run first task end-to-end.

### Week 3

- Add validation command.
- Add 3-5 tasks.
- Draft task authoring docs.

### Week 4

- Reach 10 tasks.
- Run first agent comparisons.
- Publish mini-results thread.

### Week 5

- Improve hidden tests.
- Add failure taxonomy.
- Add summary command.

### Week 6

- Add more tasks.
- Start simple leaderboard.
- Invite 3-5 people to try it.

### Week 7

- Reach 20-30 tasks.
- Improve docs.
- Fix runner reliability issues.

### Week 8

- Publish v0.1 public release.
- Publish short report.
- Ask for feedback from researchers/builders.

### Weeks 9-10

- Expand toward 50 tasks.
- Add second language/domain if quality is high enough.
- Improve website.
- Collect external results.

### Weeks 11-12

- Publish serious summer report.
- Prepare private task pack concept.
- Reach out to small labs/startups.

## MVP Acceptance Criteria

AgentGym v0.1 is ready when:

- The repo has a clear README.
- At least 10 tasks exist.
- All tasks validate.
- All tasks run locally.
- Each task has hidden tests.
- Each task has a reference solution.
- The CLI outputs structured results.
- Logs and diffs are saved.
- At least one baseline result is published.
- The limitations are clearly documented.

## Summer Acceptance Criteria

AgentGym summer version is successful when:

- 30-50 tasks are published.
- Results from multiple agents are available.
- Failure analysis is published.
- The website/README makes the project easy to understand.
- At least a few serious external people engage with it.
- The project creates a credible path toward private task packs or research collaboration.

## Further Notes

The most important thing is not to build too much infrastructure too early. AgentGym becomes valuable only if the tasks are excellent and the results reveal something real. The right sequence is task quality, deterministic execution, clear results, public credibility, then expansion.

The long-term company opportunity is still present, but it should be earned through the public artifact. If AgentGym proves that small, carefully designed executable environments can expose important agent failures, it becomes the doorway into a much larger training and evaluation business.
