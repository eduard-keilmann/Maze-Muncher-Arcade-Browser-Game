## Parent PRD

`issues/prd_old-like_gameplay.md`

## Status

Implemented in the current codebase. Static tests cover this slice.

## What to build

Implement Old-like movement-pressure tuning from the parent PRD. Old-like mode should use level-band player and ghost speeds, and ghosts should slow down in tunnels while the player does not.

## Acceptance criteria

- [x] Old-like player speed uses level-band tuning.
- [x] Old-like ghost speed uses level-band tuning that increases pressure over time.
- [x] Ghosts slow down while crossing the tunnel in Old-like mode.
- [x] Tunnel slowdown does not apply to the player.
- [x] Tunnel slowdown does not interfere with eaten ghost return behavior.
- [x] Maze Muncher mode keeps existing speed and tunnel behavior unless a shared bug fix is required.
- [x] Static tests cover Old-like speed tuning entry points and tunnel slowdown behavior.

## Prerequisites

- [x] `issues/009-add-mode-aware-tuning-functions.md`

## User stories addressed

- User story 15
- User story 16
- User story 17
- User story 22
- User story 23
- User story 41
- User story 45
- User story 47
- User story 48
- User story 49
