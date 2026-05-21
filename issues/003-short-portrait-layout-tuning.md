## Parent PRD

`issues/prd.md`

## Type

AFK

## Status

Implemented in the current codebase. Static tests cover this slice; real-device QA remains in `issues/mobile-qa-checklist.md`.

## What to build

Tune the portrait mobile layout for short phone screens while keeping the maze readable and controls thumb-friendly. This slice should make the default phone orientation comfortable without changing core gameplay rules.

## Acceptance criteria

- [x] On short portrait viewports, the canvas, D-pad, pause, and restart controls fit with minimal or no gameplay-disrupting scrolling.
- [x] The maze remains readable after responsive sizing changes.
- [x] D-pad buttons remain large enough for reliable thumb input.
- [x] Touch controls stay below the canvas and do not cover gameplay.
- [x] Existing desktop layout and keyboard behavior remain unchanged.
- [x] Static tests are updated if public control/layout contract changes.

## Prerequisites

- [x] `issues/002-mobile-real-device-qa-checklist.md` checklist artifact exists; real-device observations remain pending.

## User stories addressed

- User story 1
- User story 2
- User story 3
- User story 4
- User story 11
- User story 13
- User story 14
- User story 17
- User story 18
- User story 20
- User story 22
