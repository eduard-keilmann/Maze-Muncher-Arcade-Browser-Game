## Parent PRD

`issues/prd.md`

## Type

AFK

## Status

Implemented in the current codebase. Static tests cover this slice.

## What to build

Restore the existing mobile-control regression tests after the main HTML file rename. This is the baseline slice that makes later mobile work safely verifiable again.

## Acceptance criteria

- [x] Existing mobile-control tests read the current game HTML file.
- [x] The mobile-control tests pass without creating platform-specific scripts.
- [x] The test command remains cross-platform and uses the Python standard library.
- [x] No `.ps1` or other platform-specific test files are introduced.

## Blocked by

None - can start immediately

## User stories addressed

- User story 20
- User story 22
- User story 25
