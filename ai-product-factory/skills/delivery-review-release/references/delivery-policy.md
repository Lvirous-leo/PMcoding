# Delivery Policy

## Implementation Ownership

Claude Code is the implementation engineer. Codex owns task scope, review, verification, and gate decisions.

Codex may edit implementation files only after explicit user reassignment and only when file ownership cannot conflict with Claude Code.

## Scope Control

Implementation scope consists of approved task IDs and their mapped requirements. Adjacent cleanup is excluded unless required for correctness, security, or the approved change.

Stop and return to planning when implementation discovers:

- a requirement contradiction;
- an unapproved architecture change;
- a new migration or external dependency with material risk;
- missing acceptance behavior;
- scope that cannot fit the approved task boundary.

## Evidence

Acceptable evidence includes:

- inspected diffs;
- command output;
- test reports;
- CI check results;
- deployed commit identifiers;
- migration records;
- smoke-test results;
- monitoring observations.

An engineer summary is useful context, not independent verification.

## Review Priorities

Review in this order:

1. data loss, security, privacy, authorization, and irreversible effects;
2. correctness and approved behavior;
3. migration, compatibility, and operational recovery;
4. architecture and maintainability;
5. performance and resource behavior;
6. UX, accessibility, and consistency;
7. localized style and optional improvements.

Focus findings on defects introduced or exposed by the reviewed change.

## Severity

Critical issues can cause exploitation, data loss, severe outage, legal exposure, or fundamentally incorrect core behavior.

Major issues materially violate requirements, architecture, reliability, performance, accessibility, or maintainability and should be fixed before release.

Minor issues are real but localized and do not invalidate the release contract.

Suggestions are non-blocking alternatives or future improvements.

## Release Gate

Release requires:

- approved and current artifacts;
- complete implementation scope;
- passing required checks;
- resolved critical and major findings;
- safe migrations;
- configured secrets without disclosure;
- monitoring and operational ownership;
- tested smoke path;
- actionable rollback;
- explicit deployment approval.

## Rollback

A rollback plan identifies:

- trigger;
- responsible actor;
- exact action or command;
- compatibility of code and data;
- treatment of writes during the incident;
- verification after rollback;
- communication and follow-up.

“Redeploy the previous version” is insufficient when data, queues, caches, storage, or external contracts changed.

## Completion Evidence

Completion records:

- production commit;
- artifact versions;
- deployment time and target;
- migration result;
- smoke-test result;
- monitoring result;
- residual risk;
- rollback status;
- approver.
