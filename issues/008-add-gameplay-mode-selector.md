## Parent PRD

`issues/prd_old-like_gameplay.md`

## What to build

Add the player-facing gameplay mode selector described in the parent PRD. This slice creates the full end-to-end mode-selection path while keeping both modes behavior-identical for now: Maze Muncher remains the baseline, Old-like becomes selectable, the selected mode persists, high scores are separated by mode, and the active mode is visible during play.

## Acceptance criteria

- [ ] Title and game-over states allow switching between `MODE: MAZE MUNCHER` and `MODE: OLD-LIKE`.
- [ ] Active play does not allow changing gameplay mode mid-run.
- [ ] Selected gameplay mode is saved locally and restored on reload.
- [ ] Maze Muncher and Old-like modes use separate high-score storage.
- [ ] Switching mode before a run updates the displayed high score but does not auto-start a game.
- [ ] Footer or equivalent compact play-area text shows the active gameplay mode.
- [ ] Existing keyboard, swipe, touch movement, pause, and restart behavior still works.
- [ ] Static tests cover the public mode-selection contract.

## Blocked by

None - can start immediately

## User stories addressed

- User story 1
- User story 2
- User story 3
- User story 4
- User story 5
- User story 6
- User story 7
- User story 8
- User story 9
- User story 10
- User story 11
- User story 12
- User story 13
- User story 42
- User story 43
- User story 44
- User story 46
- User story 47
- User story 48
