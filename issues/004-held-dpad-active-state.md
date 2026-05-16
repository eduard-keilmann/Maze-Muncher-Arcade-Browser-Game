## Parent PRD

`issues/prd.md`

## Type

AFK

## What to build

Add persistent visual feedback for the currently held D-pad direction. The player should be able to tell which direction is actively being held for turn buffering.

## Acceptance criteria

- [ ] Pressing and holding a D-pad direction applies a visible active state for that button.
- [ ] Active state remains visible for the full hold duration.
- [ ] Active state clears on release, cancel, and pointer leave.
- [ ] Hold-repeat direction behavior continues to work.
- [ ] Mouse, stylus, and touch pointer paths stay consistent.
- [ ] Static tests cover the public active-state contract.

## Blocked by

- Blocked by `issues/001-fix-mobile-control-test-target.md`

## User stories addressed

- User story 5
- User story 6
- User story 7
- User story 16
- User story 19
- User story 22
