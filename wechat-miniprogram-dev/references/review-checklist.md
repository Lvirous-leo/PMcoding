# Review Checklist

Use this checklist for implementation review, release preparation, or pre-submission audit.

## Architecture

- Project type is identified: native, uni-app, Taro, or other `mp-weixin` output.
- Source files, not generated output, were changed.
- Routes, page files, page config, tabBar, and subpackages are consistent.
- Components have clear props/events and no hidden business side effects.
- Shared utilities do not create cyclic dependencies or pull heavy code into the main package.

## Security

- No `appSecret`, private key, merchant certificate, permanent token, or privileged credential exists in client code.
- Login code is exchanged on the server.
- Client session is scoped and revocable.
- Backend revalidates user identity and ownership.
- Logs do not expose tokens, phone numbers, payment data, addresses, IDs, or sensitive payloads.

## Privacy and permissions

- Sensitive APIs have clear user intent and purpose copy.
- Denied permissions produce useful fallback UI.
- Privacy policy/configuration matches actual data collection.
- Personal data is minimized, redacted in logs, and not cached unnecessarily.
- Phone, location, camera, album, microphone, files, clipboard, and subscription-message flows are reviewed when present.

## Performance

- Main package avoids low-frequency pages, heavy dependencies, and large assets.
- Lists paginate and show loading/empty/error/no-more states.
- `setData` updates are precise and not triggered excessively.
- Images/media are compressed, lazy-loaded, or remote-hosted when appropriate.
- Startup requests are essential or deferred.

## UX resilience

- Every networked feature has loading, success, empty, error, retry, and offline/timeout handling when relevant.
- Destructive actions require confirmation or clear undo/recovery.
- Payment and order flows handle cancel, pending, duplicate submit, and server reconciliation.
- Navigation failures and missing route params are handled.

## Build and release

- Existing lint/type/test/build commands pass or failures are documented.
- WeChat DevTools or framework `mp-weixin` build is verified when UI/config changes.
- `miniprogram-ci` preview/upload scripts do not expose private keys in repo.
- Production config uses approved domains and production appid.
- Debug pages, mock switches, staging base URLs, verbose logs, and test accounts are handled before submission.

## Handoff format

Report:

1. files changed or reviewed;
2. checks run and results;
3. official-doc topics consulted when platform-sensitive;
4. remaining risks or manual WeChat DevTools checks;
5. release/upload actions that still require explicit approval.
