## What to build

Deepen game lifecycle and scoring into one local Module so new game, start level, death reset, level clear, score changes, high score, extra life, fruit scoring, and ghost scoring have better locality.

This slice preserves current gameplay:

- New game resets score, level, lives, extra-life state, actors, and board.
- Level clear advances level after the clear timer.
- Death with lives remaining resets actors but keeps board pellet progress.
- Game over writes high score.
- Extra life is awarded once when Old-like mode first crosses 10,000 points.
- Pellets, power pellets, fruit, and eaten ghosts all score through the shared score path.

Architecture target:

- State transitions should be in one lifecycle Module.
- Score changes should go through one scoring Module or one scoring path inside lifecycle, whichever is simpler.
- Rendering and input should request transitions; they should not own lifecycle rules.

## Acceptance criteria

- [ ] New game, start level, death reset, level clear, and game over behavior remain unchanged.
- [ ] Score additions still update high score where appropriate.
- [ ] Old-like extra life still triggers once when crossing 10,000 points.
- [ ] Fruit and ghost score messages still appear.
- [ ] Death reset preserves current board pellet progress.
- [ ] Static tests cover lifecycle and scoring through the deepened interface where practical.
- [ ] Full test suite passes.

## Blocked by

None - can start immediately
