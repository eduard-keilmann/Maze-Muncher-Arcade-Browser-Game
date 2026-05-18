## Parent PRD

`issues/prd_old-like_gameplay.md`

## What to build

Introduce mode-aware gameplay tuning functions that provide a stable rule lookup surface for later Old-like behavior. This slice should preserve current Maze Muncher behavior while adding the Old-like level-band structure described in the parent PRD.

## Acceptance criteria

- [ ] Gameplay tuning is routed through named functions instead of scattered one-off formulas where practical.
- [ ] Maze Muncher mode preserves current speed, frightened-time, fruit, and ghost-timing behavior.
- [ ] Old-like mode has level bands for level 1, levels 2-4, levels 5-8, levels 9-16, and levels 17+.
- [ ] Old-like tuning functions exist for the later slices to use.
- [ ] Static tests verify Old-like level bands and mode-aware tuning entry points.

## Blocked by

- Blocked by `issues/008-add-gameplay-mode-selector.md`

## User stories addressed

- User story 14
- User story 15
- User story 16
- User story 17
- User story 41
- User story 45
- User story 46
- User story 47
- User story 48
- User story 49
- User story 50
