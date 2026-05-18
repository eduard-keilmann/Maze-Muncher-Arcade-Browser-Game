## Parent PRD

`issues/prd_old-like_gameplay.md`

## What to build

Implement simplified Old-like Cruise Elroy behavior for red ghost. When few pellets remain, red should increase late-board pressure through staged speed changes and a scatter override, without affecting frightened or eaten behavior.

## Acceptance criteria

- [ ] Old-like mode defines two Cruise Elroy stages based on remaining pellets.
- [ ] Red ghost gains staged speed pressure when Old-like Elroy thresholds are reached.
- [ ] Red ghost targets the player during scatter when Elroy is active.
- [ ] Elroy applies only to red ghost in normal chase-capable state.
- [ ] Elroy does not apply while red is frightened.
- [ ] Elroy does not apply while red is eaten.
- [ ] Maze Muncher mode keeps existing red ghost behavior unless a shared bug fix is required.
- [ ] Static tests cover the Elroy spec and state restrictions.

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
