## What to build

Deepen the scoring and gameplay-event path for **Power pellet**, **Bonus fruit**, pellet eating, ghost-eaten combos, normal ghost collisions, and level clear.

This slice should preserve the single-file shipped browser game. Keep any new Module local to the existing inline JavaScript, and avoid pass-through wrappers whose only job is calling another function.

The goal is to make the gameplay event path answer: what changed in score, lives, ghost state, timers, messages, sounds, and level state after the player eats something or collides with a ghost.

## Acceptance criteria

- [ ] The shipped game remains one static HTML file with inline JavaScript.
- [ ] Existing visible scoring and collision behavior is unchanged.
- [ ] **Power pellet** always scores and reverses normal ghosts, including level bands where **Frightened time** is zero.
- [ ] Ghost-eaten combo scoring and the 1600-point sound flourish remain intact.
- [ ] **Bonus fruit** spawn, timeout, score award, and message behavior remain intact.
- [ ] Tests verify behavior through the gameplay-event/scoring Module interface where practical.
- [ ] The Module improves locality: score/high-score/life/message/sound effects for these events are easier to reason about in one place.

## Blocked by

- `issues/025-deepen-test-harness-behavior-seams.md`
- `issues/026-deepen-gameplay-tuning-query-module.md`
