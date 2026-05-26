## What to build

Deepen rendering around a renderer snapshot so canvas drawing reads a stable view of game state instead of reaching across many global variables directly.

This slice should preserve the single-file shipped browser game. The renderer may remain a local Module in the existing inline JavaScript. Do not introduce canvas libraries, assets, or a build step.

This is lower priority than gameplay behavior Modules because current risk is mostly maintainability. The value is locality for HUD, overlay, lives, messages, actor drawing, **Gameplay mode** footer, and future distinct **Bonus fruit** artwork.

## Acceptance criteria

- [ ] The shipped game remains one static HTML file with inline JavaScript.
- [ ] Existing canvas visuals and layout are unchanged.
- [ ] Rendering still owns drawing only; it does not decide gameplay rules.
- [ ] Draw functions consume a compact snapshot or equivalent local interface instead of needing broad direct knowledge of mutable game state.
- [ ] Tests or static checks cover the useful renderer contract without overfitting to incidental drawing order.
- [ ] The Module passes the deletion test: deleting it would spread render-state knowledge back across draw callers.

## Blocked by

- `issues/025-deepen-test-harness-behavior-seams.md`
