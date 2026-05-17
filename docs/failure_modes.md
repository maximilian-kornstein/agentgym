# Failure Modes

AgentGym tasks are small on purpose. Each task isolates one way a coding agent can produce a patch that looks reasonable against visible tests but fails stricter hidden checks.

## Current Tasks

| Task | Failure mode | What hidden tests catch |
| --- | --- | --- |
| `python-api-001` | Whitespace-only required fields | Checks that trim happens before blank validation, not after. |
| `python-api-002` | Over-permissive nested type coercion | Checks that `"false"`, `"yes"`, `1`, and `0` are rejected instead of coerced with `bool(value)`. |
| `python-api-003` | Missing cross-field validation | Checks that business accounts require `tax_id` and personal accounts reject it. |
| `python-api-004` | Internal-field serialization leak | Checks that password hashes, internal notes, admin flags, and other private fields are not returned. |
| `python-api-005` | Missing pagination boundary validation | Checks that invalid limits, offsets, numeric strings, blank queries, and unsupported sort values are rejected. |
| `python-api-006` | Partial update semantics confusion | Checks that omitted fields, explicit nulls, empty updates, unknown fields, and boolean coercion are handled correctly. |
| `python-api-007` | Idempotency-key handling | Checks that duplicate payment requests do not overwrite state, double-process, or accept conflicting payloads. |
| `python-api-008` | Config precedence | Checks that layered config sources use the correct precedence and reject invalid overrides instead of falling back. |

## `python-api-001`: Whitespace-Only Required Fields

This task catches agents that validate text fields with only `value == ""` and then trim later. That patch can pass ordinary public tests while still accepting `"   "` or `"\t\n  "` as valid input.

The intended lesson: validation order matters. Normalize before checking blank required fields.

## `python-api-002`: Nested Boolean Type Coercion

This task catches agents that use `bool(value)` on nested API values. In Python, values like `"false"` and `"yes"` are truthy strings, while `0` and `1` are integers, not booleans. Accepting them silently changes the API contract.

The intended lesson: strict API validation should reject convenient coercion when the contract says a value must already be a boolean.

## `python-api-003`: Cross-Field Validation

This task catches agents that validate each field in isolation but miss relationships between fields. `account_type` and `tax_id` are individually simple, but the correct behavior depends on their combination.

The intended lesson: real API validation often lives between fields, not only inside fields.

## `python-api-004`: Internal-Field Serialization Leak

This task catches agents that build an API response by copying an internal record and then adjusting public fields. That can pass ordinary public tests while leaking fields like `password_hash`, `internal_notes`, `admin_flags`, or internal billing metadata.

The intended lesson: API response builders should allowlist public fields, not copy internal records wholesale.

## `python-api-005`: Pagination Boundary Validation

This task catches agents that validate only the obvious type shape of a search request while missing numeric boundaries and enum-like sort constraints. A shallow implementation can pass defaults and normal integer values while accepting `limit=0`, negative offsets, numeric strings, blank queries, or unsupported sort values.

The intended lesson: pagination and search parameters need strict boundary checks, not just broad parsing.

## `python-api-006`: Partial Update Semantics

This task catches agents that treat PATCH-style update payloads like ordinary create payloads. A shallow implementation can pass normal updates while skipping explicit `None`, allowing empty updates, ignoring unknown fields, or coercing boolean-like values.

The intended lesson: partial update APIs need clear omitted-vs-null semantics and strict validation for every field that is actually present.

## `python-api-007`: Idempotency-Key Handling

This task catches agents that validate a request but miss the state semantics around duplicate idempotency keys. A shallow implementation can process normal payments while overwriting stored responses, double-processing duplicate requests, or mutating state before rejecting invalid input.

The intended lesson: stateful API handlers need validation-before-mutation and explicit duplicate-request behavior.

## `python-api-008`: Config Precedence

This task catches agents that merge layered configuration sources in the wrong order or treat invalid high-precedence values as fallback opportunities. A shallow implementation can pass ordinary precedence examples while accepting unknown keys, coercing booleans, mutating inputs, or silently falling back to lower-precedence values.

The intended lesson: configuration builders need explicit precedence, strict validation, and no mutation of caller-owned config layers.

## Why These Are Useful

These are not large tasks. They are probes. A useful probe should:

- expose a specific failure mode
- be easy to inspect
- have deterministic hidden checks
- pass with a small reference patch
- be hard to solve by changing only visible-test behavior

The first mini-benchmark stays narrow so failures can be compared across tasks instead of hidden inside unrelated complexity.
