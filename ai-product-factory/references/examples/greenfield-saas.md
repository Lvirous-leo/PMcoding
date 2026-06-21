# Greenfield SaaS Example

Use this example to understand artifact linkage, not as a substitute for the templates.

## Context

A small operations team wants to reduce delayed incident handoffs.

## Product excerpt

```text
EVD-001: Eight of ten observed handoffs lacked an accountable next owner.
REQ-001: An incident owner can assign the next accountable owner and deadline.
AC-001: Given an active incident, when the owner assigns a teammate, then both users see the assignment and deadline.
Decision: HOLD
Evidence: L1
Critical assumption: Timely assignment changes response time.
```

## Design excerpt

```text
FLOW-001: Incident detail → assign owner → confirmation → assignee notification → overdue recovery
SCR-001 maps to REQ-001 and covers loading, permission, stale-update, success, and notification failure.
```

## Engineering excerpt

```text
REQ-001 → SCR-001 → API-001 → TASK-001 → TEST-001
```

The decision remains `HOLD` until a pilot can produce behavioral evidence.
