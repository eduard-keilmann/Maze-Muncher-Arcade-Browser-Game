## Parent PRD

`issues/prd_old-like_gameplay.md`

## Status

Implemented in the current codebase. Static tests cover this slice.

## What to build

Implement Old-like scoring changes from the parent PRD. Old-like mode should use original-like fruit names and values, and it should award one extra life when the score first crosses 10,000 points. Fruit artwork can remain simple in this slice.

## Acceptance criteria

- [x] Old-like bonus fruit uses level-based names and values, including 100, 300, 500, 700, 1000, 2000, 3000, and 5000 point values.
- [x] Fruit still appears through the existing in-level bonus-fruit flow.
- [x] Fruit visuals may remain simple and cherry-like.
- [x] Old-like mode awards one extra life when score first crosses 10,000 points.
- [x] Extra life is awarded only once per game.
- [x] Current lives display model remains unchanged.
- [x] Score updates use a shared path where practical so high score and extra-life checks are consistent.
- [x] Maze Muncher mode keeps existing fruit and life behavior unless a shared bug fix is required.
- [x] Static tests cover Old-like fruit values and the 10,000-point extra-life threshold.

## Blocked by

- Blocked by `issues/009-add-mode-aware-tuning-functions.md`

## User stories addressed

- User story 24
- User story 25
- User story 26
- User story 27
- User story 28
- User story 29
- User story 30
- User story 45
- User story 47
- User story 48
- User story 49
