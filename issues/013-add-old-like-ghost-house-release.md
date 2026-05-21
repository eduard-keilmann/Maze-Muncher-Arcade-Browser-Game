## Parent PRD

`issues/prd_old-like_gameplay.md`

## Status

Implemented in the current codebase. Static tests cover this slice.

## What to build

Implement Old-like ghost house release behavior from the parent PRD. Ghosts should leave the house based on pellet progress with timer fallback, and release thresholds already passed should remain passed after player death.

## Acceptance criteria

- [x] Old-like mode releases home ghosts using pellet-count thresholds.
- [x] Old-like mode includes timer fallback so ghosts can leave even if pellet progress stalls.
- [x] Red starts outside according to the existing ghost setup.
- [x] Pink exits quickly in Old-like mode.
- [x] Cyan and orange release later based on Old-like pellet progress or fallback timing.
- [x] After player death, current board pellet progress still controls release thresholds.
- [x] Maze Muncher mode keeps existing ghost release behavior unless a shared bug fix is required.
- [x] Static tests cover the release-spec contract and after-death threshold expectation.

## Prerequisites

- [x] `issues/009-add-mode-aware-tuning-functions.md`

## User stories addressed

- User story 31
- User story 32
- User story 33
- User story 39
- User story 41
- User story 45
- User story 47
- User story 48
- User story 49
