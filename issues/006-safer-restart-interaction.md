## Parent PRD

`issues/prd.md`

## Type

HITL

## What to build

Decide whether restart is too easy to trigger accidentally on mobile. If QA shows risk, replace one-tap restart with a safer interaction such as confirmation or long-press while keeping restart available without a keyboard.

## Acceptance criteria

- [ ] QA evidence or design review decides whether current restart behavior is acceptable.
- [ ] If current behavior is acceptable, document the decision and make no unnecessary UI change.
- [ ] If safer restart is needed, restart requires deliberate intent and remains usable on mobile.
- [ ] Pause stays easier to trigger than restart.
- [ ] Desktop restart behavior remains unchanged unless explicitly decided.
- [ ] Static tests cover any new public restart interaction contract.

## Blocked by

- Blocked by `issues/002-mobile-real-device-qa-checklist.md`

## User stories addressed

- User story 8
- User story 9
- User story 10
- User story 15
- User story 20
- User story 22
- User story 23
