## What to build

Deepen the **Gameplay mode** tuning query Module so callers and tests can ask for current gameplay facts without knowing the internal table layout.

This slice should preserve the single-file shipped browser game. Keep the Module local to the existing inline JavaScript unless there is a separately approved decision to split source files.

The Module should concentrate **Step-band formulas**, **Level band** selection, **Frightened time**, **Tunnel slowdown**, **Ghost house release**, **Bonus fruit** name/value, and scatter/chase cycle lookup behind a small behavior-oriented interface.

## Acceptance criteria

- [ ] The shipped game remains one static HTML file with inline JavaScript.
- [ ] Existing Maze Muncher and **Old-like mode** tuning behavior is unchanged.
- [ ] Callers no longer need to know the internal shape of the tuning tables for common gameplay queries.
- [ ] Tests verify behavior through the tuning Module interface instead of matching exact formula source text where practical.
- [ ] Static tests remain only for useful page-contract or wiring facts.
- [ ] The Module passes the deletion test: deleting it would spread tuning knowledge across multiple callers or tests.

## Blocked by

- `issues/025-deepen-test-harness-behavior-seams.md`
