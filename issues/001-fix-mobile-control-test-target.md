## Parent PRD

`issues/prd.md`

## Type

AFK

## What to build

Restore the existing mobile-control regression tests after the main HTML file rename. This is the baseline slice that makes later mobile work safely verifiable again.

## Acceptance criteria

- [ ] Existing mobile-control tests read the current game HTML file.
- [ ] The mobile-control tests pass without creating platform-specific scripts.
- [ ] The test command remains cross-platform and uses the Python standard library.
- [ ] No `.ps1` or other platform-specific test files are introduced.

## Blocked by

None - can start immediately

## User stories addressed

- User story 20
- User story 22
- User story 25
