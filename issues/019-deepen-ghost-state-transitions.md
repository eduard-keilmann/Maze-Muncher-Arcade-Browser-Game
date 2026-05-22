## What to build

Deepen ghost state transitions into one local Module so home, leaving, normal, frightened, and eaten behavior have better locality.

This slice should make ghost state changes easier to verify without changing visible gameplay. It should preserve:

- Ghost house release.
- Pellet-threshold release in Old-like mode.
- Timer fallback release.
- Release thresholds surviving player death.
- Eaten ghost return to the house.
- Leaving ghost transition to normal state.
- Frightened time interrupting Scatter/chase cycle.

Architecture target:

- Concentrate ghost state transition rules behind one ghost-state Module interface.
- Keep movement and rendering as callers of state facts, not owners of state decisions.
- Keep side effects explicit: release timers, eaten return, and death reset should be easy to find in one place.

## Acceptance criteria

- [ ] Home ghosts leave by Old-like pellet thresholds or fallback timer.
- [ ] Maze Muncher mode preserves current timer-based release behavior.
- [ ] Red starts outside according to existing setup.
- [ ] Player death resets actors but does not reset board pellet progress.
- [ ] Eaten ghosts return to the house and then leave again.
- [ ] Frightened time still pauses normal Scatter/chase cycle progression.
- [ ] Static tests cover state transitions through the deepened Module interface where practical.
- [ ] Full test suite passes.

## Blocked by

- Recommended after `issues/017-deepen-ghost-tunnel-mouth-movement.md`, but can start independently if scoped carefully.
