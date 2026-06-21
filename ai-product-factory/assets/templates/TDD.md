<!-- apf-template
artifact: tdd
required_headings: Context and Constraints|Architecture|Frontend|Backend|Database|API Design|State Management|Authentication and Authorization|Error Handling|Security|Observability|Testing Strategy|Deployment and Rollback|Folder Structure|Traceability|Open Questions|Approval
-->
# Technical Design Document

Status: draft  
Version: 1  
Last updated: [date]  
Upstream versions: prd=[version], ui=[version-or-na]

## Context and Constraints

[State approved scope, repository facts, constraints, and architectural drivers.]

## Architecture

[Describe boundaries, data flow, dependencies, and major decisions.]

## Frontend

[Describe rendering, component boundaries, accessibility, and performance.]

## Backend

[Describe services, domain logic, jobs, and integration boundaries.]

## Database

| Table | Purpose | Key fields | Relations | Indexes |
|---|---|---|---|---|
| [table] | [Purpose] | [Fields] | [Relations] | [Indexes] |

## API Design

| API ID | Method and path | Request | Response | Errors | Requirement IDs |
|---|---|---|---|---|---|
| API-001 | [Method path] | [Payload] | [Payload] | [Errors] | REQ-001 |

## State Management

[Define ownership, persistence, synchronization, and invalidation.]

## Authentication and Authorization

[Define identity, sessions, permissions, and denial behavior.]

## Error Handling

[Define error taxonomy, user feedback, retry, and idempotency.]

## Security

[Address secrets, validation, abuse, privacy, dependencies, and auditability.]

## Observability

[Define logs, metrics, traces, alerts, and operational ownership.]

## Testing Strategy

| Test ID | Level | Scope | Requirement IDs | Environment |
|---|---|---|---|---|
| TEST-001 | [Level] | [Scope] | REQ-001 | [Environment] |

## Deployment and Rollback

[Define migrations, compatibility, feature control, rollout, and rollback.]

## Folder Structure

```text
[Approved repository structure]
```

## Traceability

| Requirement | Screen or interface | API or component | Test |
|---|---|---|---|
| REQ-001 | SCR-001 | API-001 | TEST-001 |

## Open Questions

- [Technical question]

## Approval

Approved by: [name]  
Approved at: [ISO-8601 timestamp]
