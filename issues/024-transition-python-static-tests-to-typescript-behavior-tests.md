## What to build (rejected/suspended for now!)

Start the transition from Python regex/static tests to TypeScript behavior tests with one narrow, complete tracer bullet.

This slice should add the smallest useful TypeScript test path and migrate one already-deepened game-rule surface to it. The goal is not to rewrite the whole test suite at once. The goal is to prove that core game behavior can be tested in the same language/runtime as the game logic, through a stable public interface, without losing the useful page-contract coverage that the current Python tests provide.

Recommended first behavior surface:

- Audio threat scoring, touch steering direction classification, gameplay tuning queries, ghost state transitions, or game lifecycle/scoring.
- Choose the smallest surface that can be tested without canvas rendering, browser input events, Web Audio, localStorage, or animation timing.

Architecture target:

- TypeScript behavior tests should own executable game-rule assertions.
- Python tests should remain only for static page contracts that are still valuable, such as visible controls, storage keys, and script/page wiring.
- Avoid a broad build-system migration in this slice unless it is required for the first TypeScript behavior test to run.
- Keep the new test command simple, documented, and deterministic.

## Acceptance criteria

- [ ] A minimal TypeScript test runner exists and can run one focused behavior test file.
- [ ] One existing behavior currently covered mostly by Python source-shape assertions is covered by executable TypeScript behavior tests.
- [ ] The tested game-rule code is reachable through a small public interface rather than private source-text matching.
- [ ] Existing Python tests are kept for page-contract coverage that TypeScript unit tests do not replace.
- [ ] Project documentation explains when to use TypeScript behavior tests vs Python static/page-contract tests.
- [ ] The full existing Python test suite still passes.
- [ ] The new TypeScript test command passes.

## Blocked by

- `issues/023-upgrade-static-tests-to-behavior-seams.md`
