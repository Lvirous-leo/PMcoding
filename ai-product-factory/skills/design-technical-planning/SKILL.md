---
name: design-technical-planning
description: Prepare OpenDesign input, review UI prototypes, create implementation-ready UI specifications, write a technical design, and produce a Claude Code sprint plan from an approved PRD. Use for UI_INPUT、OpenDesign 交接、设计评审、UI 规范、TDD、技术方案、开发计划、任务拆分.
---

# Design, Technical Design, and Planning

Translate an approved product decision into design and engineering contracts without implementing code.

English instructions are normative.
For Chinese requests, apply these rules and write narrative content in Chinese when useful.
Read `references/zh-overview.md` only for a requested Chinese workflow explanation.

## Required Inputs

- Approved PRD path and exact version.
- Project mode and current state.
- Repository structure and local instructions.
- OpenDesign output when reviewing design.
- Existing UI, TDD, or sprint artifacts when updating.
- User-approved constraints and architecture decisions.

## Output Contract

Produce one active-phase artifact:

- `docs/UI_INPUT.md`;
- `docs/UI.md`;
- `docs/TDD.md`;
- `.ai/tasks/sprint-001.md`.

Return:

```yaml
artifact: exact/path.md
artifact_version: 1
phase: technical_design
upstream_versions:
  prd: 1
coverage:
  requirements: []
open_questions: []
gate_recommendation: ready_for_review
```

Do not produce several governed phases in one pass unless the orchestrator explicitly routes each phase and its gate in sequence.

## Load Only What Is Needed

Always read:

- the exact approved upstream artifact versions;
- the current phase template under `../../assets/templates/`;
- `references/design-policy.md` for UI input or UI review;
- `references/technical-policy.md` for TDD or sprint planning.

Inspect the repository before TDD or sprint planning.
Read examples only when the mode or artifact intent is unclear.

## Preconditions

Reject or block when:

- PRD is absent, unapproved, invalidated, or version-ambiguous;
- critical product questions remain open;
- the requested phase would skip an earlier applicable phase;
- required OpenDesign output is missing;
- repository facts needed for architecture cannot be inspected.

Do not silently repair product requirements inside a design or technical artifact.
Return the issue to the PRD phase.

## UI Input Phase

For UI products, create `docs/UI_INPUT.md`.

Translate requirements into:

- end-to-end user flows;
- complete screen inventory;
- reusable component needs;
- interaction and navigation requirements;
- loading, empty, error, permission, partial, and success states;
- accessibility expectations;
- responsive intent.

Every screen or flow must map to `REQ-` identifiers.
Describe outcomes and constraints, not visual styling solutions reserved for OpenDesign.

After validation, return the artifact for user approval before OpenDesign begins.

## OpenDesign Handoff

OpenDesign owns UI/UX design and prototypes.

Provide:

- approved PRD and UI input versions;
- users, flows, screens, states, constraints, and accessibility needs;
- explicit open design questions;
- required output coverage.

Do not ask OpenDesign to redefine product scope or technical architecture.

## Design Review Phase

When OpenDesign output is available:

1. inspect every required screen and flow;
2. compare it with approved requirement IDs;
3. check all required states;
4. check navigation, recovery, destructive actions, and feedback;
5. check responsive behavior and accessibility;
6. identify contradictions or missing surfaces;
7. request OpenDesign revision when design work is incomplete.

Create `docs/UI.md` only when the prototype is sufficiently coherent to specify implementation.

The UI specification must capture:

- screen structure;
- component hierarchy;
- design tokens;
- interactions;
- state coverage;
- responsive rules;
- accessibility decisions;
- remaining design gaps.

Do not redesign the prototype inside the implementation specification.

## Non-UI Mode

When mode is `non-ui`:

- verify the PRD describes the user-facing API, CLI, event, job, library, or file interface;
- mark `ui_input` and `ui` as `not_applicable` with a written reason in state;
- continue to technical design;
- do not create empty UI documents.

## Technical Design Phase

Create `docs/TDD.md` from approved product and design contracts.

Inspect:

- repository architecture and conventions;
- existing dependencies and runtime;
- data and integration boundaries;
- deployment and test tooling;
- security, privacy, and operational constraints.

Define:

- architecture and component boundaries;
- frontend and backend responsibilities;
- database tables, relations, and indexes when applicable;
- API requests, responses, errors, and idempotency;
- state ownership and synchronization;
- authentication and authorization;
- error handling and recovery;
- security and abuse controls;
- observability;
- testing strategy;
- deployment, compatibility, and rollback;
- intended folder structure.

Map `REQ-` identifiers to screens or interfaces, components or APIs, and `TEST-` identifiers.

Use the approved repository stack when it exists.
Use default technologies only when no approved constraint or repository fact supersedes them.

## Architecture Decisions

Record material tradeoffs, rejected alternatives, and consequences.
Prefer the smallest architecture that satisfies approved requirements and non-functional constraints.

Do not introduce unjustified services or abstractions, replace existing architecture for stylistic preference, or hide unresolved technical risk.

Return material product or architecture choices to the user for approval.

## Sprint Planning Phase

Create `.ai/tasks/sprint-001.md` only from approved PRD, UI when applicable, and TDD versions.

Break work into:

```text
feature → task → subtask
```

Every `TASK-` must include:

- objective;
- expected files or directories;
- implementation owner `Claude Code`;
- dependencies;
- mapped `REQ-` and `TEST-` identifiers;
- observable acceptance criteria;
- verification commands;
- boundaries and stop conditions.

Order tasks by dependency and risk.
Keep tasks small enough for focused implementation and review.
Separate migrations, security-sensitive work, and release controls when their failure modes differ.

## Self-Review

Before returning:

1. confirm upstream versions are exact and approved;
2. confirm every required template section is resolved;
3. confirm requirement coverage and stable IDs;
4. confirm missing and error states are addressed;
5. confirm architecture follows repository facts;
6. confirm testing and rollback match risk;
7. confirm every implementation task is assigned to Claude Code;
8. list open questions and blockers.

Do not implement production code in this skill.
