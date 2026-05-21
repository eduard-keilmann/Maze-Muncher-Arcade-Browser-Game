## Parent PRD

`issues/prd_old-like_gameplay.md`

## Status

Implemented in the current codebase. Static tests cover this slice.

## What to build

Implement Old-like power-pellet behavior from the parent PRD. Power pellets should become less protective across Old-like level bands, still reverse ghosts even when frightened time is zero, and only make ghosts edible while frightened time is actually active.

## Acceptance criteria

- [x] Old-like frightened time uses level-band behavior and can reach zero in late levels.
- [x] Power pellets still score points in Old-like mode at every level.
- [x] Power pellets reverse normal ghosts in Old-like mode even when frightened time is zero.
- [x] Ghosts are edible only when Old-like frightened time is greater than zero.
- [x] Ghost combo scoring is possible only during edible frightened state.
- [x] Frightened ghost movement is simplified to random available non-reverse movement.
- [x] Maze Muncher mode keeps its existing power-pellet behavior unless a shared bug fix is required.
- [x] Static tests cover zero frightened time and edible-only-when-frightened behavior.

## Prerequisites

- [x] `issues/009-add-mode-aware-tuning-functions.md`

## User stories addressed

- User story 18
- User story 19
- User story 20
- User story 21
- User story 38
- User story 40
- User story 47
- User story 48
- User story 49
