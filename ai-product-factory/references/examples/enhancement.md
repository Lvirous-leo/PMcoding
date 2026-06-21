# Enhancement Example

## Context

An existing billing product needs scheduled invoice reminders.

## Incremental handling

```text
Changed: REQ-014, AC-021, RULE-008
Unaffected: existing payment capture and refund requirements
Impact: notification preferences, time zones, retry policy, audit log, support workflow
```

The PRD version increases. UI, TDD, sprint, implementation tests, review, and release are invalidated only where they depend on the changed identifiers.

The design worker inspects current notification components before adding new ones. The technical worker preserves the existing job system unless approved requirements create a missing boundary.

The sprint assigns only the affected tasks to Claude Code and prohibits unrelated billing refactors.
