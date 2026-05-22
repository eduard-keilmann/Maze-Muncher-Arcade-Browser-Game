## Status

Implemented in the current codebase. Static tests cover the shared touch steering interface and the full test suite is green.

## What to build

Deepen Touch steering so D-pad, whole-page continuous swipe, canvas tap-to-turn, and touch actions share a small, clear steering interface.

This slice keeps all existing mobile gameplay behavior:

- Whole-page continuous swipe steers before finger release.
- Canvas tap-to-turn steers relative to Maze Muncher.
- D-pad directions route into the shared direction path.
- Press-and-hold D-pad keeps the turn queued.
- Interactive controls are ignored by swipe logic.
- Mouse swipe/tap steering remains canvas-only on desktop.
- Title/game-over input starts or restarts before steering.

Architecture target:

- Event listeners should become thin adapters.
- Gesture classification should live in one Touch steering Module.
- The Module should convert input facts into shared game actions like `setDirection`, `newGame`, and `togglePause`.
- Do not duplicate movement physics or pause/restart logic inside separate input handlers.

## Acceptance criteria

- [x] D-pad, whole-page swipe, and canvas tap-to-turn all still call the shared direction path.
- [x] Continuous swipe remains low latency and updates direction during pointer movement.
- [x] Tap-to-turn still loses to swipe when movement exceeds the swipe threshold.
- [x] Interactive controls do not double-trigger swipe logic.
- [x] Desktop mouse steering remains canvas-only.
- [x] Title/game-over swipe or tap starts the game before applying direction.
- [x] Static tests cover behavior through the deepened Touch steering interface where practical.
- [x] Full test suite passes.

## Blocked by

None - can start immediately
