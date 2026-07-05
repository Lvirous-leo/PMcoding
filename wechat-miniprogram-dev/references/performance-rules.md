# Performance Rules

## Startup

- Keep the main package small and focused on first-run essentials.
- Move low-frequency pages, heavy feature modules, large assets, and optional dependencies into subpackages.
- Avoid loading full dictionaries, large config blobs, or media metadata on app launch.
- Defer noncritical requests until the page is visible or the user expresses intent.

## Rendering and `setData`

- Send the smallest possible `setData` payload.
- Do not update entire large objects or arrays when only one field changed.
- Avoid high-frequency `setData` in scroll, drag, animation, timer, or input hot paths.
- Batch related updates, debounce noisy events, and keep data paths precise.
- Do not put non-rendering data into page/component data when a plain instance field is enough.

## Lists and pagination

- Use pagination or virtualized patterns for long lists.
- Maintain explicit states: first loading, pull-to-refresh, loading more, no more data, empty, error, retry.
- Avoid rendering large hidden lists.
- Keep list item components light; avoid nested expensive computed rendering.

## Images and media

- Compress images and use suitable dimensions.
- Lazy-load below-the-fold media.
- Avoid bundling large media in the main package unless needed on first screen.
- Prefer CDN or approved download domains for large remote assets.

## Network

- Use request timeouts and user-visible recovery.
- Cache stable, low-risk data with clear invalidation.
- Avoid duplicate concurrent requests for the same resource.
- Do not block first paint on nonessential analytics or optional personalization.

## Package size

- Monitor main package and total package size before release.
- Split feature areas that are not needed for launch.
- Check UI libraries and utility packages for tree-shaking or platform-specific imports.
- Remove unused assets, mocks, debug pages, and dead dependencies from production builds.

## Framework builds

- Native: verify in WeChat DevTools after structural changes.
- uni-app: run the project command that builds `mp-weixin`; inspect generated output only for verification.
- Taro: run the project command that builds WeChat output; do not patch generated output as source.
