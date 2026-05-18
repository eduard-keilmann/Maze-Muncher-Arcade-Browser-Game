## Parent PRD

`issues/prd.md`

## What to build

Implement Old-like ghost house release behavior from the parent PRD. Ghosts should leave the house based on pellet progress with timer fallback, and release thresholds already passed should remain passed after player death.

## Acceptance criteria

- [ ] Old-like mode releases home ghosts using pellet-count thresholds.
- [ ] Old-like mode includes timer fallback so ghosts can leave even if pellet progress stalls.
- [ ] Red starts outside according to the existing ghost setup.
- [ ] Pink exits quickly in Old-like mode.
- [ ] Cyan and orange release later based on Old-like pellet progress or fallback timing.
- [ ] After player death, current board pellet progress still controls release thresholds.
- [ ] Maze Muncher mode keeps existing ghost release behavior unless a shared bug fix is required.
- [ ] Static tests cover the release-spec contract and after-death threshold expectation.

## Blocked by

- Blocked by `issues/009-add-mode-aware-tuning-functions.md`

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
