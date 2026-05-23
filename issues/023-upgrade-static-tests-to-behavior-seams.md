## What to build

Upgrade static tests toward behavior seams after at least one deepened Module exists.

Current tests are useful but heavily regex-based. They often verify source text shape instead of behavior. This slice should reduce brittleness by testing Module interfaces where possible while keeping the no-build, no-dependency project constraint.

Architecture target:

- The interface is the test surface.
- Keep tests dependency-free unless a separate decision reopens browser automation.
- Prefer behavior assertions over implementation-text assertions.
- Keep static regex checks only for page contract facts that are truly static, such as visible controls or storage keys.

Possible first behavior seams:

- Ghost personality: choose next direction from a board/ghost/player snapshot.
- Touch steering: classify pointer sequence as swipe or tap and output direction.
- Audio threat music: compute threat level from a small game-facts object.
- Gameplay tuning: query mode/level tuning values directly.

## Acceptance criteria

- [x] At least one deepened Module has tests that verify behavior through its interface rather than only source regex.
- [x] Existing important page-contract tests remain covered.
- [x] No browser automation dependency is added unless the existing browser-interaction test decision is explicitly reopened.
- [x] Test names use project domain language from `CONTEXT.md`.
- [x] Tests stay deterministic and readable.
- [x] Full test suite passes.

## Blocked by

- At least one of:
  - `issues/017-deepen-ghost-tunnel-mouth-movement.md`
  - `issues/018-deepen-ghost-personality-targeting.md`
  - `issues/019-deepen-ghost-state-transitions.md`
  - `issues/020-deepen-touch-steering.md`
  - `issues/021-deepen-generated-audio-and-threat-music.md`
  - `issues/022-deepen-game-lifecycle-and-scoring.md`

## Completed note

- Added `tests/test_audio_behavior_seams.py` as the first executable behavior-seam test path.
- The new tests run extracted `gameAudio` behavior through `node` without adding repo dependencies or browser automation.
- `tests/test_sound_controls.py` now keeps static page-contract and wiring checks, while threat scoring details moved to behavior assertions.
