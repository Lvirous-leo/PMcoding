<!-- apf-template
artifact: sprint
required_headings: Sprint Goal|Approved Inputs|Task Plan|Dependency Order|Verification Commands|Risks and Boundaries|Definition of Done|Approval
-->
# Sprint 001

Status: draft  
Version: 1  
Last updated: [date]  
Upstream versions: prd=[version], ui=[version-or-na], tdd=[version]

## Sprint Goal

[State the user-visible or operational outcome.]

## Approved Inputs

[List exact approved artifact versions and included identifiers.]

## Task Plan

### TASK-001 — [Task name]

Objective: [One observable outcome]  
Implementation owner: Claude Code  
Files: [Expected files or directories]  
Dependencies: [TASK IDs or none]  
Requirement IDs: REQ-001  
Test IDs: TEST-001

Subtasks:

1. [Small implementation step]
2. [Small verification step]

Acceptance:

- [Observable criterion]

## Dependency Order

[Explain sequencing and safe parallel work.]

## Verification Commands

```bash
npm run lint
npm run test
npm run build
```

## Risks and Boundaries

[List prohibited redesign, unrelated changes, secrets, migrations, and stop conditions.]

## Definition of Done

- Assigned requirements are implemented.
- Required tests pass.
- Lint and build pass when present.
- No unapproved scope or architecture change is introduced.

## Approval

Approved by: [name]  
Approved at: [ISO-8601 timestamp]
