# Technical Design and Planning Policy

## Repository First

Inspect the actual repository before selecting architecture, dependencies, paths, or verification commands. Existing approved conventions outrank the default stack.

## Default Stack

Use these defaults only for a genuine greenfield product without conflicting constraints:

- Next.js and TypeScript;
- Tailwind CSS;
- Next.js route handlers;
- Supabase PostgreSQL, Auth, and Storage;
- Vercel;
- GitHub and GitHub Actions.

Defaults are not requirements.

## Architecture Quality

A technical design should make boundaries, data flow, ownership, failure, security, deployment, and testing explicit.

Prefer:

- cohesive modules;
- stable interfaces;
- dependency direction that supports testing;
- reversible decisions;
- incremental migrations;
- explicit operational ownership.

Avoid:

- architecture by fashion;
- duplicated sources of truth;
- speculative services;
- hidden cross-system coupling;
- security deferred to implementation;
- release plans without rollback.

## Data and API Design

For each stored entity define purpose, lifecycle, keys, constraints, relations, indexes, retention, and authorization.

For each API define request, response, errors, permissions, idempotency, pagination where relevant, compatibility, and mapped requirements.

## Security

Address:

- authentication and session behavior;
- authorization at every trust boundary;
- input and output validation;
- secret handling;
- least privilege;
- sensitive data and privacy;
- abuse, rate limiting, and denial behavior;
- dependency and supply-chain risk;
- audit evidence.

## Testing

Map tests to risks and requirements. Use the lowest-cost test that catches the failure at the correct boundary, then add higher-level tests for critical user loops.

Include migration and rollback tests when data changes. Include accessibility, contract, performance, or security tests when requirements demand them.

## Task Design

A task is implementation-ready when the engineer can identify:

- one objective;
- exact scope and expected files;
- approved upstream versions;
- dependencies and order;
- requirement and test IDs;
- observable acceptance;
- verification commands;
- stop conditions.

Claude Code must report ambiguity instead of redesigning requirements or architecture.
