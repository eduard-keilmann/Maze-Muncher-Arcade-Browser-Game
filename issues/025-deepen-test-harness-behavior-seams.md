## What to build

Deepen the test harness so one more gameplay behavior is verified through an executable Module interface instead of source-text matching.

This keeps Maze Muncher as a single-file shipped browser game. The implementation may add or adjust repo-local tests, but must not require splitting `maze_muncher_browser_arcade.html` into shipped source files or adding a browser-game build step.

Important source-of-truth rule:

- Do not create duplicated `src/` game-rule mirror files only to make behavior tests importable.
- Behavior tests must exercise logic from the actual shipped HTML, either by extracting inline JavaScript seams from `maze_muncher_browser_arcade.html` or by testing the HTML in a browser-like runtime if a separate decision approves that dependency.
- A test-only mirror that can drift from the inline game code does not satisfy this issue.

Recommended first target: a low-risk **Gameplay mode** behavior already covered by brittle static assertions, such as **Step-band formulas**, **Frightened time**, **Tunnel slowdown**, or **Bonus fruit** tuning.

## Acceptance criteria

- [ ] The shipped game remains one static HTML file with inline JavaScript.
- [ ] No duplicated `src/` game-rule mirror files are added for test convenience.
- [ ] Behavior tests use the actual shipped HTML as the source of truth.
- [ ] At least one gameplay behavior currently covered by regex-heavy assertions is covered by executable behavior tests through a Module interface.
- [ ] Python static tests remain for page-contract facts that are genuinely static, such as visible controls, storage keys, and wiring.
- [ ] No new dependency or build step is added unless the issue body is updated with the reason.
- [ ] Focused tests pass for the migrated behavior and the still-relevant static page contract.
- [ ] The final result improves locality: behavior failures point at the game rule, not at incidental source formatting.

## Blocked by

- None - can start immediately.
