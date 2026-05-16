## Parent PRD

`issues/prd.md`

## Type

HITL

## What to build

Evaluate landscape phone play after baseline QA and portrait tuning. If landscape is cramped or clipped, implement the smallest landscape-specific layout that keeps the canvas readable and controls reachable.

## Acceptance criteria

- [ ] Landscape behavior is tested on real or representative mobile viewports.
- [ ] Decision is recorded: no landscape-specific layout needed, or landscape layout required.
- [ ] If required, landscape layout keeps controls reachable without covering the canvas.
- [ ] If required, landscape layout avoids gameplay-disrupting page scroll.
- [ ] Portrait layout remains unchanged except where shared CSS improvements are intentional.
- [ ] Static tests are updated if public layout/control contract changes.

## Blocked by

- Blocked by `issues/002-mobile-real-device-qa-checklist.md`
- Blocked by `issues/003-short-portrait-layout-tuning.md`

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
