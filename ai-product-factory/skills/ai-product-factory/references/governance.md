# Governance

This file is the authoritative source for ownership, routing, approval, invalidation, and recovery. State values and legal enums are authoritative only in `../../../schemas/state.schema.json`.

## Ownership

- The user approves product scope, material tradeoffs, architecture exceptions, release readiness, and production deployment.
- Codex owns discovery synthesis, requirements, product decisions, architecture, technical design, planning, orchestration, review, validation, and gate administration.
- OpenDesign owns UI/UX exploration, screen design, interaction design, and prototypes.
- Claude Code is the sole implementation engineer unless the user explicitly reassigns implementation ownership.
- Codex and Claude Code must not edit the same implementation files concurrently.
- Worker skills generate their governed artifacts; the orchestrator coordinates and validates them.

## Routing

| Active work | Worker |
|---|---|
| Research, problem analysis, PRD, product decision | `product-discovery-prd` |
| OpenDesign input, design review, UI specification, TDD, sprint plan | `design-technical-planning` |
| Claude Code handoff, implementation verification, review, release | `delivery-review-release` |

Route only one active governed phase at a time. Read only the worker references and artifact template required for that phase.

## Approval

Approval is explicit, version-specific, and recorded with an approver and ISO-8601 timestamp.

The user must approve:

- PRD scope and product decision;
- UI implementation specification, or the non-UI rationale;
- technical design and material architecture decisions;
- sprint scope before implementation;
- resolution of review blockers;
- release readiness and production deployment.

An artifact may enter `approved` only when:

- all required template sections contain resolved content;
- critical questions and contradictions are closed;
- upstream versions match current approved versions;
- required evidence and traceability exist;
- the user explicitly approves that version.

## State Transitions

Normal artifact progression is:

```text
missing → pending → draft → in_review → approved
```

Exceptional states are:

```text
blocked
not_applicable
invalidated
```

Use only values allowed by the state schema. File existence never changes state by itself.

## Invalidation

Every approved artifact records its upstream versions. When an upstream version changes, invalidate all downstream artifacts whose assumptions, identifiers, interfaces, tests, or release scope may be affected.

Minimum impact chain:

```text
PRD → UI input → UI → TDD → sprint → implementation → review → release
```

For non-UI work, omit the two UI nodes but preserve the remaining order.

Invalidation requires:

- a version increment on the changed artifact;
- affected stable IDs;
- an `invalidated_by` reason on each affected record;
- an event-ledger entry;
- fresh validation and approval.

## Recovery

The state file is the current snapshot. The event ledger is append-only history.

On resume:

1. load both files;
2. validate state;
3. compare governed artifact versions with state;
4. detect interrupted writes or stale approvals;
5. find the earliest incomplete or invalidated phase;
6. continue there without regenerating approved content.

If state and artifacts disagree, preserve files, report the discrepancy, and repair state only with evidence. Do not silently downgrade or overwrite an approved artifact.

## Artifact Editing

- Inspect before editing.
- Make incremental changes for enhancement mode.
- Preserve approved content unrelated to the authorized change.
- Use stable IDs from the templates.
- Record facts, inferences, assumptions, and unknowns distinctly.
- Keep machine values, IDs, paths, statuses, and headings in English.
- Narrative content may use the user's requested language.

## Evidence and Decisions

The product worker owns definitions for analysis depth, evidence levels, and `GO`, `PIVOT`, `KILL`, or `HOLD`. The orchestrator records the returned values and enforces schema-level consistency.

`GO` cannot cross the PRD gate with unresolved critical assumptions or evidence below the worker's threshold.

## External Actions

Repository inspection and local artifact creation are normal workflow actions. Production deployment, external messages, account changes, purchases, or irreversible operations require the authority normally required by the target system and explicit user approval when material.

## Failure Handling

Do not hide failed checks. Record:

- command or validation attempted;
- result and relevant evidence;
- correction attempted;
- remaining blocker;
- safe next action.

Repeated unchanged external state is not itself evidence of completion.
