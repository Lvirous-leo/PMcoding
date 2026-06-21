---
name: ai-product-factory
description: Orchestrate a governed product lifecycle from idea through PRD, OpenDesign handoff, technical design, Claude Code implementation, review, and release. Use for complete product delivery, continuing an interrupted factory run, deciding the next phase, or requests such as 产品工厂、完整产品流程、从想法到上线、继续上次流程.
---

# AI Product Factory

Coordinate the product lifecycle without mixing professional ownership.

English instructions are normative.
For Chinese requests, execute these English rules and respond in the user's language.
Read `references/zh-overview.md` only when the user asks for a Chinese explanation of the workflow.

## Required Inputs

- The user's objective and constraints.
- The repository and its local instructions.
- `.ai/product-factory/state.yaml` when present.
- `.ai/product-factory/events.jsonl` when present.
- Existing governed artifacts and implementation evidence.

## Outputs

Return:

- detected project mode and current valid phase;
- selected analysis depth and reason;
- worker skill used;
- artifact path, version, and validation result;
- approval request, blocker, or completed gate;
- next permitted phase.

## Start or Resume

1. Inspect the repository before proposing work.
2. Read `references/governance.md`.
3. Locate the plugin root from this skill directory.
4. If state is absent, run `scripts/init_project.py`.
5. If state is V2, run `scripts/migrate_state.py`.
6. Load state and the event ledger.
7. Inspect existing artifacts before editing them.
8. Derive the current phase from valid status and approvals, not file existence.
9. Resume the earliest incomplete or invalidated phase.

## Select Project Mode

Choose:

- `greenfield` for a new product or repository;
- `enhancement` for a change to an existing product;
- `non-ui` for APIs, CLIs, jobs, libraries, or infrastructure without product UI.

Record the choice in state.
If evidence conflicts, state the assumption and continue at the safest earlier phase.

## Select Analysis Depth

Honor an explicit user override.
Otherwise choose:

- `lite` for low-risk, well-understood, reversible work;
- `standard` for ordinary product work with moderate uncertainty;
- `deep` for high-impact, regulated, irreversible, cross-system, or poorly understood work.

Record the selected depth and a concrete reason.
Depth changes rigor, not the phase order.

## Route One Phase

Invoke exactly one worker for the active governed phase:

- discovery and PRD → `$product-discovery-prd`;
- OpenDesign input, design review, TDD, and sprint plan → `$design-technical-planning`;
- development handoff, code review, and release → `$delivery-review-release`.

Do not reproduce the worker's professional method.
Pass only current state, approved upstream versions, relevant repository facts, and user constraints.

## Phase Order

Use this order:

1. discovery;
2. PRD;
3. UI input when applicable;
4. OpenDesign output and design review when applicable;
5. technical design;
6. development planning;
7. implementation;
8. code and product review;
9. release preparation and deployment verification.

Do not skip a phase.
For `non-ui`, mark UI artifacts `not_applicable` with a reason and continue in order.

## Validate and Gate

After a worker returns:

1. Confirm the artifact path and version.
2. Run `scripts/validate_artifacts.py` for the target gate.
3. Reject unresolved placeholders, contradictions, stale upstream versions, or missing traceability.
4. Summarize material changes and evidence.
5. Request the required user approval.
6. Record approver and timestamp only after explicit approval.
7. Update state atomically.
8. Append an event describing the transition.

Never infer approval from silence, file existence, or previous approval of another version.

## Change Control

When an approved upstream artifact changes:

1. increment its version;
2. identify affected stable IDs;
3. mark dependent artifacts `invalidated`;
4. record the invalidation event;
5. resume from the earliest affected phase;
6. obtain fresh approval before downstream execution.

Do not continue against stale artifacts.

## Stop Conditions

Stop and report a blocker when:

- a material product or architecture choice requires the user;
- required evidence is unavailable and the decision would be unsafe;
- OpenDesign output is required but unavailable;
- Claude Code cannot receive or complete the assigned implementation;
- validation fails after reasonable correction;
- release authorization, credentials, or external coordination is missing.

Use `HOLD`, not invented certainty, when evidence is insufficient.

## Completion

The workflow is complete only when:

- every applicable artifact is approved;
- implementation matches approved versions;
- lint, tests, and build pass when available;
- review has no unresolved critical or major issue;
- release evidence and rollback are complete;
- production verification succeeds;
- state is `completed` and the final event is recorded.

Report concise results in the user's language while preserving English machine values and identifiers.
