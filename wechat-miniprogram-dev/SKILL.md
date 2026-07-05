---
name: wechat-miniprogram-dev
description: Develop, modify, review, and release WeChat Mini Programs against WeChat Open Docs platform rules. Use for 微信小程序 development, Mini Program architecture, app.json/pages.json/project.config.json changes, WXML/WXSS/JS/TS components, uni-app or Taro mp-weixin output, wx API usage, login/session flows, privacy compliance, performance optimization, package splitting, miniprogram-ci preview/upload, and pre-submission review.
---

# WeChat Mini Program Dev

## Overview

Use this skill as a platform guardrail for WeChat Mini Program work. Prefer the user's existing architecture, framework, and tooling; apply WeChat platform constraints before writing or reviewing code.

If current behavior conflicts with the WeChat Open Docs or project-specific rules, follow the stricter rule and call out the conflict.

## Operating Rules

1. Inspect the project first: identify whether it is native Mini Program, uni-app, Taro, or another framework that outputs `mp-weixin`.
2. Locate platform configuration before changing routes or capabilities: `app.json`, `project.config.json`, `sitemap.json`, `privacy.json`, `pages.json`, `manifest.json`, or framework equivalents.
3. Do not introduce a new framework, state library, UI library, or cloud/backend provider unless the user explicitly asks or the existing project already uses it.
4. Never put `appSecret`, service-side access tokens, payment keys, private certificates, or permanent credentials in Mini Program client code.
5. Treat login, payment, phone number, location, camera, album, files, Bluetooth, clipboard, and subscription messages as platform-sensitive flows that require explicit UX, permission, privacy, and failure-state handling.
6. Prefer small, reversible changes. Preserve generated framework output directories unless the user asks to edit build artifacts directly.

## Workflow

### 1. Classify the task

- Feature implementation: read `architecture-rules.md`, then load other references relevant to the feature.
- API/security-sensitive work: read `api-security-rules.md`.
- Performance, list, media, startup, or package-size work: read `performance-rules.md`.
- Privacy, authorization, personal information, or submission review work: read `privacy-compliance-rules.md`.
- Code review, release, preview, upload, or audit work: read `review-checklist.md`.
- When official behavior or API names are uncertain, read `official-docs-map.md` and verify against the current WeChat Open Docs before acting.

### 2. Establish project context

Check only the files needed for the task:

- Native: `app.json`, page `.json`, `.wxml`, `.wxss`, `.js/.ts`, `project.config.json`, `miniprogram_npm/`.
- uni-app: `src/pages.json`, `src/manifest.json`, `src/App.vue`, `src/pages/**`, `src/components/**`, `vite.config.*`.
- Taro: `src/app.config.*`, page config files, `project.config.json`, `config/index.*`, `src/pages/**`, `src/components/**`.
- CI/release: `package.json`, CI scripts, private-key references, `miniprogram-ci` config, environment variable docs.

### 3. Design before editing

Before implementation, state the minimal design in one short paragraph:

- affected pages/components/config files;
- involved `wx.*` APIs or framework wrappers;
- privacy/security/performance risks;
- validation commands available in this repo.

If the user asks for review only, do not edit files.

### 4. Implement platform-safe changes

- Keep route declarations, tabBar entries, subpackage roots, and component paths consistent with the framework.
- Add explicit empty, loading, retry, permission-denied, and network-error states for user-facing flows.
- Use server APIs for credential exchange and privileged operations; the Mini Program client should receive only scoped, short-lived, least-privilege data.
- Keep request domains, upload/download domains, and socket domains aligned with the Mini Program platform configuration and deployment environment.
- Avoid broad `setData` updates, large payloads, deep object churn, and repeated updates in hot paths.

### 5. Verify

Run the repo's existing checks when available:

- type check or framework compile command;
- lint;
- unit/component tests;
- `mp-weixin` build;
- preview/upload dry-run if the project already has safe `miniprogram-ci` scripts.

Do not upload, submit for review, deploy, or publish without explicit user approval.

## Review Output Format

For audits and reviews, report findings by severity:

- Critical: secrets, payment/session compromise, privacy violations, data leakage, app-breaking route/config errors.
- Major: broken permission flows, likely review rejection, severe performance or package-size risk, missing server boundary.
- Minor: maintainability, naming, duplicated code, weak loading/error states.
- Suggestions: optional improvements that are safe to defer.

Each finding should include file/path, impact, and concrete fix.

## Reference Loading Guide

- `references/official-docs-map.md`: official WeChat Open Docs entry points and verification map.
- `references/architecture-rules.md`: project structure, routing, pages, components, subpackages, tabBar, framework-specific rules.
- `references/api-security-rules.md`: login, session, request, payment, subscription messages, files, sensitive APIs, secret handling.
- `references/performance-rules.md`: startup, rendering, `setData`, lists, media, package size, network resilience.
- `references/privacy-compliance-rules.md`: privacy, authorization, personal information, permission UX, review readiness.
- `references/review-checklist.md`: implementation and release review checklist.
