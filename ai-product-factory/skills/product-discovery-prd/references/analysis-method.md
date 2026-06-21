# Product Analysis Method

Use this method to simplify complexity without losing the system that creates the problem.

## 1. Essential Need and Real Purpose

Separate the requested feature from the underlying job, constraint, or desired change.

Ask:

- What becomes possible or easier for the user?
- What pain, risk, delay, or uncertainty is removed?
- What outcome matters if the requested mechanism disappears?
- Is the request a need, a workaround, a habit, or a stakeholder preference?

Rewrite complex requests as a concise problem statement. Remove ornamental requirements that do not affect the target outcome.

## 2. System Impact and Perspective Switching

Analyze both point-to-system and system-to-point effects.

Point-to-system:

- Which users, roles, data, workflows, policies, and metrics does this change touch?
- What second-order effects or incentives might it create?
- Which adjacent teams or systems absorb new work?

System-to-point:

- How do current architecture, policy, operations, business model, and product strategy constrain this request?
- Is the local problem a symptom of a broader system issue?

Switch perspectives among end user, buyer, operator, support, security, finance, and business owner where relevant. Use “if this changes, then what changes next?” at least three times for high-impact work.

## 3. Closed-loop Validation

Verify three loops.

Business loop:

```text
trigger → action → value → measurable outcome → learning or reinforcement
```

Scenario loop:

```text
entry → progress → completion → feedback → recovery
```

Logic loop:

```text
input → decision or transformation → output → validation → exception handling
```

A feature is incomplete when it creates an action without feedback, an outcome without measurement, or a failure without recovery.

## 4. Simplification and Elegant Resolution

The goal is not fewer features by itself. The goal is the simplest mechanism that reliably closes the target loop.

Test:

- Can an existing behavior, object, or policy solve it?
- Can several cases become one rule?
- Can configuration replace repeated bespoke work?
- Can a manual step safely validate demand before automation?
- What can be removed without reducing the desired outcome?

Reject accidental complexity, premature automation, and surface polish that conceals an unresolved core problem.

## 5. Reusable Abstraction and Configuration

Abstract only after identifying stable variation.

Move from:

```text
single feature → repeated pattern → configurable capability → platform
```

Require evidence of repeated use cases, shared semantics, and lower total cost before moving right. Define what varies, what stays invariant, and who safely controls configuration.

Do not use “platform” as a synonym for a large feature.

## 6. Change, Learning, and Value

Assume context changes.

Assess:

- what is reversible and what is not;
- which assumption should be tested first;
- how the product learns from use;
- when the decision should be revisited;
- how users and operations adapt;
- whether value persists after novelty.

Prefer experiments that reduce the most consequential uncertainty. Record how new evidence can change scope, depth, or decision.

## Synthesis

End analysis with:

- a one-sentence essential problem;
- the smallest coherent product loop;
- affected system boundaries;
- rejected complexity;
- justified reusable elements;
- highest-risk assumption;
- measurable value;
- next evidence needed.
