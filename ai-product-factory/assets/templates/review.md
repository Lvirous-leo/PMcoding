<!-- apf-template
artifact: review
required_headings: Review Scope|Verification Evidence|Architecture Compliance|Critical Issues|Major Issues|Minor Issues|Suggestions|UX Consistency|Traceability Result|Review Decision|Approval
-->
# Code and Product Review 001

Status: draft  
Version: 1  
Last updated: [date]  
Upstream versions: sprint=[version], implementation_commit=[sha]

## Review Scope

[List commits, files, tasks, requirements, and excluded work.]

## Verification Evidence

| Command or check | Result | Evidence |
|---|---|---|
| [Command] | pass/fail | [Output or link] |

## Architecture Compliance

[Compare implementation with approved TDD decisions and boundaries.]

## Critical Issues

- REV-001: [Release-blocking correctness, security, or data issue; write “None” only after verification.]

## Major Issues

- [Material maintainability, performance, UX, or coverage issue]

## Minor Issues

- [Localized issue]

## Suggestions

- [Optional improvement outside blocking scope]

## UX Consistency

[Compare implemented states and interactions with approved UI specification.]

## Traceability Result

| Requirement | Task | Test | Review evidence | Result |
|---|---|---|---|---|
| REQ-001 | TASK-001 | TEST-001 | [Evidence] | pass/fail |

## Review Decision

Decision: [APPROVE or REQUEST_CHANGES]  
Residual risks: [Risks]

## Approval

Approved by: [name]  
Approved at: [ISO-8601 timestamp]
