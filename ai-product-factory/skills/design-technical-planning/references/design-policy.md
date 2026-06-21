# Design Policy

## OpenDesign Boundary

OpenDesign owns visual and interaction design. Codex supplies the product contract, reviews coverage, and converts approved design into an implementation specification.

Do not ask OpenDesign to decide:

- product scope or priority;
- business rules;
- technical architecture;
- database or API shape;
- release policy.

## UI Input Quality

A design input is complete when a designer can identify:

- the primary and secondary users;
- the outcome and context of each flow;
- every required screen or surface;
- entry, completion, feedback, and recovery;
- permissions and role differences;
- loading, empty, error, partial, offline, and success behavior;
- destructive actions and confirmation;
- accessibility and responsive constraints.

Use stable `FLOW-`, `SCR-`, `CMP-`, and `REQ-` identifiers.

## Design Review

Review prototypes against the approved contract, not personal aesthetic preference.

Check:

- requirement and flow coverage;
- information hierarchy;
- action clarity and consistency;
- prevention and recovery from error;
- visibility of system status;
- keyboard and focus behavior;
- readable contrast and scalable text;
- touch target and viewport behavior;
- component reuse without hiding meaningful variation.

Missing states are missing design, even if the happy path is polished.

## UI Specification

The implementation specification records approved behavior and design decisions with enough precision for engineering. It does not replace source prototypes.

Capture:

- layout regions and hierarchy;
- components and variants;
- token names and usage;
- interactions and transitions;
- validation and feedback;
- state matrix;
- responsive changes;
- accessibility decisions;
- known gaps and approved exceptions.

If design output contradicts the PRD, return the conflict for resolution. Do not silently choose one.

## Non-UI Interfaces

An API, CLI, event, or generated file can still have a user experience. Its discoverability, feedback, error semantics, recovery, and documentation belong in the PRD and TDD, not fictional UI artifacts.
