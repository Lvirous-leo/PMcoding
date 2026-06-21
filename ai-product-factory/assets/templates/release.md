<!-- apf-template
artifact: release
required_headings: Release Scope|Artifact Versions|Quality Gate Results|Configuration and Secrets|Database and Storage|Deployment Plan|Smoke Tests|Monitoring|Rollback|Production Verification|Release Decision|Approval
-->
# Release 001

Status: draft  
Version: 1  
Last updated: [date]  
Upstream versions: review=[version], implementation_commit=[sha]

## Release Scope

[List included requirements, tasks, changes, and exclusions.]

## Artifact Versions

| Artifact | Version | Status |
|---|---|---|
| PRD | [Version] | approved |

## Quality Gate Results

| Gate | Result | Evidence |
|---|---|---|
| Lint | pass/fail | [Evidence] |
| Tests | pass/fail | [Evidence] |
| Build | pass/fail | [Evidence] |
| Review | pass/fail | [Evidence] |

## Configuration and Secrets

[Confirm environment variables, secret handling, and configuration ownership.]

## Database and Storage

[Describe migrations, backups, compatibility, and recovery.]

## Deployment Plan

[Describe target, sequence, automation, approvals, and observation window.]

## Smoke Tests

| Test | Expected | Actual |
|---|---|---|
| [Critical path] | [Expected] | [Actual] |

## Monitoring

[List dashboards, logs, alerts, owners, and thresholds.]

## Rollback

[Define trigger, command or action, data handling, and verification.]

## Production Verification

[Record deployed commit, deployment time, smoke result, and monitoring result.]

## Release Decision

Decision: [READY, HOLD, or ROLLBACK]  
Reason: [Reason]

## Approval

Approved by: [name]  
Approved at: [ISO-8601 timestamp]
