## What to build

Deepen the movement rules Module for tile-center movement, wall blocking, tunnel continuation, **Tunnel slowdown**, **Cruise Elroy** speed pressure, frightened speed, eaten return speed, and actor direction decisions.

This slice has higher behavior risk than the tuning and scoring slices because movement ordering matters. Preserve the single-file shipped browser game and keep changes incremental.

The goal is not arcade-perfect movement. The goal is a deeper local Module whose interface can advance an actor or answer movement facts without callers knowing the ordering of center snapping, tunnel wrapping, speed selection, and direction selection.

## Acceptance criteria

- [ ] The shipped game remains one static HTML file with inline JavaScript.
- [ ] Existing Maze Muncher and **Old-like mode** movement feel is unchanged.
- [ ] Player movement, ghost movement, tunnel continuation, and wall-collision behavior remain stable.
- [ ] **Tunnel slowdown** still affects normal ghosts only, not the player or eaten ghosts.
- [ ] **Cruise Elroy** remains limited to red ghost in normal chase-capable state and does not affect frightened or eaten states.
- [ ] Focused movement behavior tests cover at least one tunnel path and one speed-selection path through the Module interface.
- [ ] The Module improves leverage: movement tests no longer need to inspect the exact ordering of many small helper functions.

## Blocked by

- `issues/025-deepen-test-harness-behavior-seams.md`
- `issues/026-deepen-gameplay-tuning-query-module.md`
- `issues/027-deepen-pellet-fruit-collision-scoring-module.md`
