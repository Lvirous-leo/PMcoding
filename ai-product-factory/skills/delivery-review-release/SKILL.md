---
name: delivery-review-release
description: Hand approved tasks to Claude Code, supervise scoped implementation, run project checks, review architecture security performance maintainability and UX, resolve findings, and prepare or verify release. Use for Claude Code 开发交接、实现监督、代码评审、质量门槛、发布准备、部署验证.
---

# Delivery, Review, and Release

Coordinate implementation and independently verify that approved product and technical contracts were satisfied.

English instructions are normative.
For Chinese requests, apply these rules and report results in Chinese when useful.
Read `references/zh-overview.md` only for a requested Chinese explanation.

## Required Inputs

- Approved PRD, UI when applicable, TDD, and sprint versions.
- Current state and event history.
- Repository status and local instructions.
- Assigned task identifiers.
- Claude Code implementation results.
- CI, test, build, review, and deployment evidence.

## Output Contract

Produce one active-phase result:

- scoped Claude Code handoff and implementation evidence;
- `.ai/reviews/review-001.md`;
- `.ai/releases/release-001.md`.

Return:

```yaml
phase: review
artifact: .ai/reviews/review-001.md
artifact_version: 1
implementation_commit: commit-sha
checks:
  lint: pass
  test: pass
  build: pass
blocking_findings: []
gate_recommendation: ready_for_review
```

Never report a check as passing without evidence.

## Load Only What Is Needed

Always read:

- `references/delivery-policy.md`;
- exact approved upstream artifacts;
- the active phase template;
- repository instructions and relevant source;
- current implementation diff and check evidence.

Do not load product research or design references unless a discrepancy requires returning to that phase.

## Preconditions

Block implementation when:

- sprint plan is absent, unapproved, or invalidated;
- upstream artifact versions do not match;
- tasks are not assigned to Claude Code;
- task scope or acceptance is ambiguous;
- required credentials or external dependencies are unavailable;
- implementation would require unapproved architecture or product changes.

Do not repair missing planning by improvising requirements during development.

## Claude Code Handoff

Delegate only approved `TASK-` identifiers.

Provide:

- objective;
- exact approved artifact versions;
- expected files or directories;
- dependencies;
- mapped requirements and tests;
- acceptance criteria;
- verification commands;
- prohibited scope and stop conditions.

Instruct Claude Code to:

1. inspect repository instructions and relevant code;
2. implement only assigned tasks;
3. preserve requirements and architecture;
4. avoid unrelated refactors;
5. add or update tests;
6. report ambiguity before changing design;
7. run required checks;
8. summarize files, behavior, checks, and residual risks.

Codex must not concurrently edit the same implementation files.

## Supervise Implementation

After each task:

1. inspect the diff;
2. compare it with the task and approved artifacts;
3. verify tests were added at the correct boundary;
4. run targeted checks;
5. request a focused correction for failures;
6. record completed task and evidence.

Do not accept “implemented” as proof.
Do not broaden the task because adjacent code could be cleaner.

## Required Checks

Use repository-native commands.

For the default JavaScript stack, run when present:

```bash
npm run lint
npm run test
npm run build
```

Also run the targeted unit, integration, end-to-end, accessibility, contract, migration, rollback, security, or performance checks required by the TDD.

Fix all in-scope failures before review completion.
Record unavailable checks and why.

## Review Phase

Create `.ai/reviews/review-001.md` using the template.

Review:

- architecture compliance;
- requirement and acceptance coverage;
- correctness and edge cases;
- security and privacy;
- performance and resource behavior;
- maintainability and clarity;
- test quality;
- data migration and compatibility;
- error handling and observability;
- UX and accessibility consistency;
- release and rollback readiness.

Use severities:

- `Critical`: unsafe to merge or release;
- `Major`: material defect or contract violation;
- `Minor`: localized quality issue;
- `Suggestion`: optional improvement outside the gate.

Every actionable finding receives a stable `REV-` identifier, evidence, impact, and required resolution.

## Review Iteration

For each critical or major finding:

1. assign a focused correction to Claude Code;
2. inspect the resulting diff;
3. rerun affected checks;
4. update the finding with resolution evidence;
5. retain history rather than deleting the finding.

The review gate cannot pass with unresolved critical or major findings.
Suggestions do not silently expand release scope.

## Release Preparation

Create `.ai/releases/release-001.md` only after review passes.

Verify:

- exact artifact versions and implementation commit;
- lint, tests, build, and review evidence;
- environment configuration and secret ownership;
- database and storage migrations;
- backups and compatibility;
- deployment sequence and authority;
- smoke tests;
- monitoring, alerts, and operators;
- rollback trigger and procedure;
- known residual risks.

Do not expose secrets in the artifact.

## Deployment

Production deployment requires explicit user approval and target-system authority.

When authorized:

1. record the approved commit and artifact versions;
2. apply migrations using the approved sequence;
3. deploy through the approved CI/CD path;
4. run smoke tests;
5. inspect monitoring for the observation window;
6. record production evidence;
7. roll back when release criteria fail.

Do not mark the workflow complete at “deployment started.”

## Self-Review

Before returning:

1. confirm only assigned scope changed;
2. confirm evidence for every reported check;
3. confirm traceability from `REQ-` to `TASK-`, `TEST-`, and review evidence;
4. confirm no unresolved critical or major issue;
5. confirm release and rollback are executable;
6. confirm production actions received approval;
7. list residual risk and the next permitted action.

If any condition fails, return a blocker or `REQUEST_CHANGES`, not a false completion.
