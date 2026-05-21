## Parent PRD

`issues/prd_old-like_gameplay.md`

## Status

Implemented in the current codebase. Static tests cover this slice.

## What to build

Implement simplified Old-like Cruise Elroy behavior for red ghost. When few pellets remain, red should increase late-board pressure through staged speed changes and a scatter override, without affecting frightened or eaten behavior.

## Acceptance criteria

- [x] Old-like mode defines two Cruise Elroy stages based on remaining pellets.
- [x] Red ghost gains staged speed pressure when Old-like Elroy thresholds are reached.
- [x] Red ghost targets the player during scatter when Elroy is active.
- [x] Elroy applies only to red ghost in normal chase-capable state.
- [x] Elroy does not apply while red is frightened.
- [x] Elroy does not apply while red is eaten.
- [x] Maze Muncher mode keeps existing red ghost behavior unless a shared bug fix is required.
- [x] Static tests cover the Elroy spec and state restrictions.

## Blocked by

- Blocked by `issues/009-add-mode-aware-tuning-functions.md`
- Blocked by `issues/012-add-old-like-speed-and-tunnel-dynamics.md`

## User stories addressed

- User story 34
- User story 35
- User story 36
- User story 39
- User story 41
- User story 45
- User story 47
- User story 48
- User story 49
