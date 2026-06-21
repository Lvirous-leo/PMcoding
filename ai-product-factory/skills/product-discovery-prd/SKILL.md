---
name: product-discovery-prd
description: Research and analyze a product idea or requirement, identify the essential user problem, apply system and closed-loop product thinking, assess evidence, recommend GO PIVOT KILL or HOLD, and create or update a PRD. Use for 产品需求分析、市场竞品、用户问题、PRD、需求评估、产品决策.
---

# Product Discovery and PRD

Turn an idea or request into an evidence-aware, testable product decision.

English instructions are normative.
For Chinese requests, apply these rules and write narrative content in Chinese when useful.
Read `references/zh-overview.md` only when the user asks for a Chinese explanation.

## Required Inputs

- The idea, request, or proposed change.
- Project mode and selected analysis depth.
- Existing product, research, analytics, and PRD material.
- Business constraints and explicit user decisions.
- Current state and relevant artifact versions.

## Output Contract

Create or incrementally update `docs/PRD.md` using the plugin PRD template.

Return:

```yaml
artifact: docs/PRD.md
artifact_version: 1
analysis_depth: standard
selection_reason: concrete risk and uncertainty reason
evidence_level: L1
decision: HOLD
critical_assumptions: []
open_questions: []
gate_recommendation: blocked
```

Use English machine values exactly as shown.

## Load Only What Is Needed

Always read:

- `references/analysis-method.md`;
- `references/evidence-policy.md`;
- `../../assets/templates/PRD.md`;
- the current PRD when present.

Read examples only when the mode or expected artifact is unclear.
Inspect repository behavior for enhancement requests.
Use current primary sources when research claims may have changed.

## Confirm the Decision Context

Identify:

- who is experiencing the problem;
- what outcome they seek;
- where and when it occurs;
- current alternatives and workarounds;
- business objective and constraints;
- decision deadline and reversibility;
- what would make the work not worth doing.

Do not turn a requested feature directly into a requirement.
First restate the underlying problem and desired outcome.

## Select or Verify Depth

Honor the orchestrator's explicit depth unless new evidence materially changes risk.

Use:

- `lite` for a bounded, reversible change with known users and behavior;
- `standard` for moderate uncertainty, multiple roles, or meaningful workflow impact;
- `deep` for new markets, strategic bets, regulated data, irreversible choices, high cost, or cross-system effects.

If changing depth, state the reason and return it.

## Research

Research only what can change the decision.

Depending on depth, examine:

- user behavior, pains, triggers, and current workaround;
- industry structure and relevant trends;
- direct, indirect, and substitute competitors;
- product constraints and adjacent workflows;
- existing analytics, support evidence, or operational incidents;
- legal, security, privacy, accessibility, or policy constraints.

Prefer primary sources.
Record source date and scope.
Do not use popularity as proof of user value.

## Classify Knowledge

Label important claims as:

- `FACT`: directly supported;
- `INFERENCE`: reasoned from facts;
- `ASSUMPTION`: plausible but unverified;
- `UNKNOWN`: required information not available.

Assign evidence IDs such as `EVD-001`.
Connect each material requirement or decision to relevant evidence.

## Apply the Product Analysis Method

Use all six dimensions from `references/analysis-method.md`:

1. essential need and real purpose;
2. system impact and perspective switching;
3. business, scenario, and logic closed loops;
4. simplification and elegant resolution;
5. reusable abstraction and configuration;
6. change, learning, and value.

Depth changes the amount of evidence and alternatives, not whether a dimension is considered.

## Shape the Product

Define:

- product vision;
- target users and exclusions;
- measurable goals and baselines;
- in-scope capabilities;
- explicit non-goals;
- business rules and exceptions;
- non-functional requirements;
- risks and critical assumptions.

Prefer the smallest coherent solution that closes the target loop.
Do not add platform abstractions without repeated demand or a clear strategic reason.

## Write Requirements

Use stable IDs.

Each `REQ-` must:

- describe observable behavior or outcome;
- identify relevant actor and context;
- avoid prescribing implementation unless it is a constraint;
- map to one or more `AC-` identifiers;
- identify evidence and priority.

Each acceptance criterion must be independently testable.
Include negative, permission, error, empty, and recovery behavior when relevant.

For enhancement mode:

- preserve approved unaffected content;
- identify changed IDs;
- add impact on existing users, data, interfaces, and metrics;
- increment the PRD version.

For non-UI mode:

- describe API, CLI, event, job, library, or generated-file interfaces as product surfaces;
- do not create fictional screens.

## Assess Evidence and Decide

Use `references/evidence-policy.md`.

Return one decision:

- `GO`;
- `PIVOT`;
- `KILL`;
- `HOLD`.

Do not recommend `GO` when a critical assumption remains unresolved.
Do not hide a weak evidence level behind confident prose.

## Self-Review

Before returning:

1. verify every required template section;
2. remove unresolved guidance;
3. verify IDs and acceptance mappings;
4. distinguish facts from assumptions;
5. verify success metrics are measurable;
6. confirm scope and non-goals are coherent;
7. confirm the decision matches evidence;
8. list open questions with owners or decision needs.

Do not discuss framework, database, or API choices unless they are externally imposed product constraints.
The next phase owns implementation design.
