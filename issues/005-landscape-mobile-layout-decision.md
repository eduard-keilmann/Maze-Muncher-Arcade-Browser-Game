## Parent PRD

`issues/prd.md`

## Type

HITL

## Status

Decision and landscape CSS are implemented. Real-device landscape observations remain pending in `issues/mobile-qa-checklist.md`.

## What to build

Evaluate landscape phone play after baseline QA and portrait tuning. If landscape is cramped or clipped, implement the smallest landscape-specific layout that keeps the canvas readable and controls reachable.

## Acceptance criteria

- [ ] Landscape behavior is tested on real mobile devices.
- [x] Decision is recorded: no landscape-specific layout needed, or landscape layout required.
- [x] If required, landscape layout keeps controls reachable without covering the canvas.
- [x] If required, landscape layout avoids gameplay-disrupting page scroll.
- [x] Portrait layout remains unchanged except where shared CSS improvements are intentional.
- [x] Static tests are updated if public layout/control contract changes.

## Prerequisites

- [x] `issues/002-mobile-real-device-qa-checklist.md` checklist artifact exists; real-device observations remain pending.
- [x] `issues/003-short-portrait-layout-tuning.md`

## User stories addressed

- User story 1
- User story 2
- User story 4
- User story 12
- User story 13
- User story 14
- User story 15
- User story 17
- User story 18
- User story 23
