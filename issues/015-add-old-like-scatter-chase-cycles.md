## Parent PRD

`issues/prd_old-like_gameplay.md`

## Status

Implemented in the current codebase. Static tests cover this slice.

## What to build

Implement Old-like scatter/chase timing from the parent PRD. Old-like mode should vary scatter/chase cycles by level band, become chase-heavy in later levels, and preserve frightened-mode interruption behavior.

## Acceptance criteria

- [x] Old-like mode uses level-band scatter/chase cycles.
- [x] Later Old-like levels become more chase-heavy than early levels.
- [x] Frightened mode continues to interrupt normal scatter/chase timing.
- [x] Existing ghost personalities remain recognizable.
- [x] Maze Muncher mode keeps existing scatter/chase timing unless a shared bug fix is required.
- [x] Static tests cover Old-like mode-cycle selection and frightened interruption expectations.

## Blocked by

- Blocked by `issues/009-add-mode-aware-tuning-functions.md`

## User stories addressed

- User story 17
- User story 37
- User story 38
- User story 39
- User story 41
- User story 45
- User story 47
- User story 48
- User story 49
