# PMcoding Skills

 Codex skills and plugins.

## AI Product Factory

`ai-product-factory/` is a governed product-delivery plugin containing:

- one end-to-end orchestrator;
- product discovery and PRD analysis;
- OpenDesign, technical design, and sprint planning;
- Claude Code delivery, review, and release governance;
- shared templates, state schema, migration scripts, validators, tests, and evals.

English files are the authoritative execution source. Chinese overview files are concise, non-normative explanations.

### Install

Copy or link `ai-product-factory/` into a Codex plugin location, then validate it:

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py ai-product-factory
```

Primary entry:

```text
$ai-product-factory
```

## WeChat Mini Program Dev

`wechat-miniprogram-dev/` is a WeChat Mini Program development and review skill based on WeChat Open Docs platform guardrails. It covers native Mini Program, uni-app, and Taro projects that output `mp-weixin`.

It helps with:

- Mini Program architecture, routing, pages, components, tabBar, and subpackages;
- `wx.*` API usage, login/session boundaries, payment, subscription messages, and sensitive capabilities;
- privacy compliance, authorization UX, personal-data handling, and submission readiness;
- startup, `setData`, package-size, media, network, and list performance;
- `miniprogram-ci` preview/upload safety checks.

Primary entry:

```text
$wechat-miniprogram-dev
```
