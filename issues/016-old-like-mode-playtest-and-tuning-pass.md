## Parent PRD

`issues/prd.md`

## What to build

Run a human playtest and tuning pass for Old-like mode after the mode infrastructure, core dynamics, and ghost-pressure slices are implemented. The goal is to verify that Old-like mode feels meaningfully closer to original Pac-Man without becoming an arcade-perfect clone or an unfair difficulty spike.

## Acceptance criteria

- [ ] Compare Maze Muncher mode and Old-like mode across early, mid, and later levels.
- [ ] Verify Old-like mode feels more original-like in power-pellet value, fruit scoring, tunnel escapes, ghost pressure, and late-board tension.
- [ ] Confirm Old-like mode remains playable with keyboard controls.
- [ ] Confirm Old-like mode remains playable with touch controls.
- [ ] Confirm mode switching does not mutate active runs.
- [ ] Record any tuning adjustments needed before considering Old-like mode complete.
- [ ] Confirm no new requirement has pushed the feature toward arcade-perfect clone scope.

## Blocked by

- Blocked by `issues/010-add-old-like-power-pellet-dynamics.md`
- Blocked by `issues/011-add-old-like-fruit-and-extra-life-scoring.md`
- Blocked by `issues/012-add-old-like-speed-and-tunnel-dynamics.md`
- Blocked by `issues/013-add-old-like-ghost-house-release.md`
- Blocked by `issues/014-add-old-like-cruise-elroy.md`
- Blocked by `issues/015-add-old-like-scatter-chase-cycles.md`

## User stories addressed

- User story 2
- User story 15
- User story 16
- User story 17
- User story 41
- User story 49
- User story 50
