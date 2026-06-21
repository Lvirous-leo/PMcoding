# Non-UI API Example

## Context

A partner needs a signed webhook for completed exports.

## Product surface

The user experience is the event contract, delivery feedback, retry semantics, documentation, and recovery path.

```text
REQ-001: A registered partner endpoint receives a signed export.completed event.
REQ-002: Failed deliveries retry with bounded backoff and expose delivery status.
AC-001: A valid receiver can verify signature, timestamp, and event identifier.
```

`ui_input` and `ui` are `not_applicable` with a written rationale.

The TDD defines payload, signature, replay prevention, idempotency, retries, retention, observability, and compatibility. The sprint maps requirements directly to API, worker, and contract-test tasks.
