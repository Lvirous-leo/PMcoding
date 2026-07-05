# Architecture Rules

## Project classification

Identify the project type before editing:

- Native Mini Program: `app.json`, `project.config.json`, `pages/**/*.wxml`, `pages/**/*.wxss`, `pages/**/*.js|ts`.
- uni-app: `src/pages.json`, `src/manifest.json`, Vue single-file components, `uni.*` wrappers, `dist/dev/mp-weixin` output.
- Taro: `src/app.config.*`, page config files, React/Vue components, `taro build --type weapp` or equivalent.
- Mixed or generated projects: treat source files as authoritative and generated `dist` output as disposable unless the user says otherwise.

## Routing and configuration

- Keep route declarations and files in sync. Adding a page requires the page file, route config, navigation entry when needed, and correct path casing.
- Use `app.json` or framework equivalents for global pages, window behavior, tabBar, subpackages, permission text, and plugins.
- Do not rename page paths, tabBar entries, or subpackage roots casually; these are public app navigation contracts.
- Keep page-level config close to the page when the framework supports it.
- Do not edit compiled `mp-weixin` output if source files exist.

## Pages

- Keep each page focused on one user task.
- Put business orchestration in page logic, reusable rendering in components, and API access in services/modules.
- Always handle initial loading, refresh, empty data, network failure, permission denial, and retry.
- Use lifecycle hooks intentionally: initialize from route params on load, refresh visible data on show only when needed, and clean timers/listeners on unload.
- Avoid storing large derived state in page data; compute locally when possible.

## Components

- Build components with explicit props, events, and slot contracts.
- Keep components platform-safe: no hidden global state, no implicit page route assumptions, no direct login/payment side effects inside visual-only components.
- Use `externalClasses` or project conventions for style extension when needed.
- Avoid component APIs that expose raw backend payloads unless the payload is already a stable frontend contract.

## Subpackages

- Use subpackages for low-frequency flows, large feature areas, heavy media, large dependencies, admin-like screens, or feature modules not needed on first launch.
- Keep the main package limited to app shell, landing pages, login entry, tabBar pages, shared essentials, and critical utilities.
- Avoid importing heavy subpackage-only dependencies into main-package code.
- For independent subpackages, verify that the flow can work without main-package state.

## Framework-specific notes

### Native

- Keep WXML templates simple and move nontrivial logic into JS/TS.
- Keep WXSS scoped by page/component naming conventions; avoid broad selectors that leak across components.
- Use `usingComponents` explicitly and keep relative paths stable.

### uni-app

- Change `src/pages.json` and `src/manifest.json`, not generated WeChat output.
- Use conditional compilation only for true platform differences.
- Prefer `uni.*` APIs unless the feature requires a WeChat-specific `wx.*` API and the code path is guarded for `mp-weixin`.

### Taro

- Change source config (`app.config.*`, page config) and source components.
- Use Taro abstractions where practical; use raw `wx.*` only when the wrapper lacks required capability.
- Verify the generated WeChat output only after source changes.
