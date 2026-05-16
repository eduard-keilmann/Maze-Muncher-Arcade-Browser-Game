## Parent PRD

`issues/prd.md`

## Type

HITL

## What to build

Reassess whether static tests and manual QA are enough after mobile polish. If browser interaction tests are justified, add the smallest cross-platform browser test setup that verifies real tap, hold, release, responsive layout, pause, restart safety, and keyboard preservation.

## Acceptance criteria

- [ ] Decision is recorded: no browser automation needed yet, or browser automation needed now.
- [ ] If no automation is needed, existing static test coverage remains green and documented as sufficient for current risk.
- [ ] If automation is needed, chosen tooling is cross-platform and does not add platform-specific scripts.
- [ ] If automation is needed, tests cover at least one real hold/release D-pad interaction.
- [ ] If automation is needed, tests cover pause and restart behavior at a mobile viewport.
- [ ] If automation is needed, tests do not replace the manual Safari/Chrome QA checklist.

## Blocked by

- Blocked by `issues/003-short-portrait-layout-tuning.md`
- Blocked by `issues/004-held-dpad-active-state.md`
- Blocked by `issues/005-landscape-mobile-layout-decision.md`
- Blocked by `issues/006-safer-restart-interaction.md`

## User stories addressed

- User story 15
- User story 19
- User story 20
- User story 21
- User story 22
- User story 24
- User story 25
