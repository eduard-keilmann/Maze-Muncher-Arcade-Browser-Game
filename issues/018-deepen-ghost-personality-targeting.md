## What to build

Deepen Ghost personality targeting into one local Module so red, pink, cyan, orange, frightened movement, scatter targets, chase targets, and Cruise Elroy override are easier to reason about and test.

This slice should preserve current visible behavior:

- Red targets Maze Muncher's current tile during chase.
- Pink targets ahead of Maze Muncher, including the current old ambush quirk feel when moving up.
- Cyan uses the red ghost tile plus a two-ahead vector target.
- Orange chases when far and scatters when close.
- Scatter/chase cycle still controls normal ghost pressure.
- Cruise Elroy still lets red target Maze Muncher during scatter only when active.
- Frightened movement remains mode-aware.

Architecture target:

- Put target-tile selection and direction choice behind one Ghost personality Module interface.
- Keep the implementation free to use current globals initially, but reduce duplicated ghost knowledge outside the Module.
- The interface is the test surface: tests should verify behavior, not scattered source snippets.

## Acceptance criteria

- [x] Red chase target remains Maze Muncher's tile.
- [x] Pink ahead target remains four tiles ahead with the current up-direction ambush quirk feel.
- [x] Cyan target remains based on red ghost tile and the two-ahead vector.
- [x] Orange target remains player tile when far and scatter corner when close.
- [x] Cruise Elroy red still targets Maze Muncher during scatter only while active.
- [x] Frightened movement remains random in Old-like mode and mixed in Maze Muncher mode.
- [x] Static tests cover each Ghost personality through the deepened Module interface.
- [x] Full test suite passes.

## Blocked by

None - completed after `issues/017-deepen-ghost-tunnel-mouth-movement.md`
