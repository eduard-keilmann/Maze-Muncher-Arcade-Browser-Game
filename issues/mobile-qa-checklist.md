# Mobile QA Checklist

Parent issue: `issues/002-mobile-real-device-qa-checklist.md`

Use this checklist on real Safari iPhone and Chrome Android devices before changing layout further. Record device, browser, orientation, viewport notes, and exact problems observed.

## Test Setup

- Game file: `maze_muncher_browser_arcade.html`
- Start state: title screen
- Required regression command before and after mobile changes:

```sh
python -B -m unittest discover tests
```

## Small Portrait Phone

Suggested target: narrow/short phone viewport.

- [ ] Maze readability: pellets, walls, ghosts, player, score, lives readable.
- [ ] D-pad reachability: direction buttons reachable by thumb without awkward stretch.
- [ ] Page scrolling: D-pad holds and whole-page swipes do not cause gameplay-disrupting scroll.
- [ ] Whole-page continuous swipe: swipes outside the canvas steer Maze Muncher before finger release.
- [ ] Canvas tap-to-turn: taps on the canvas steer based on tap position relative to Maze Muncher.
- [ ] Held direction: hold each D-pad direction for at least 2 seconds; queued turns keep responding.
- [ ] Pause: pause button is easy to trigger intentionally.
- [ ] Restart: short tap does not restart; long press does restart.
- [ ] Sound/music: first user gesture unlocks audio; SOUND and MUSIC toggles behave as labeled.
- [ ] Touch interference: no text selection, zoom, or tap-highlight distraction during play.
- [ ] Notes:

## Tall Portrait Phone

Suggested target: common modern tall phone viewport.

- [ ] Maze readability: pellets, walls, ghosts, player, score, lives readable.
- [ ] D-pad reachability: direction buttons reachable by thumb without awkward stretch.
- [ ] Page scrolling: D-pad holds and whole-page swipes do not cause gameplay-disrupting scroll.
- [ ] Whole-page continuous swipe: swipes outside the canvas steer Maze Muncher before finger release.
- [ ] Canvas tap-to-turn: taps on the canvas steer based on tap position relative to Maze Muncher.
- [ ] Held direction: hold each D-pad direction for at least 2 seconds; queued turns keep responding.
- [ ] Pause: pause button is easy to trigger intentionally.
- [ ] Restart: short tap does not restart; long press does restart.
- [ ] Sound/music: first user gesture unlocks audio; SOUND and MUSIC toggles behave as labeled.
- [ ] Touch interference: no text selection, zoom, or tap-highlight distraction during play.
- [ ] Notes:

## Landscape Phone

Suggested target: same devices rotated landscape.

- [ ] Maze readability: gameplay remains readable without severe clipping.
- [ ] D-pad reachability: direction buttons are reachable and not too far from the canvas.
- [ ] Page scrolling: D-pad holds and whole-page swipes do not cause gameplay-disrupting scroll.
- [ ] Whole-page continuous swipe: swipes outside the canvas steer Maze Muncher before finger release.
- [ ] Canvas tap-to-turn: taps on the canvas steer based on tap position relative to Maze Muncher.
- [ ] Held direction: hold each D-pad direction for at least 2 seconds; queued turns keep responding.
- [ ] Pause: pause button remains usable.
- [ ] Restart: short tap does not restart; long press does restart.
- [ ] Sound/music: first user gesture unlocks audio; SOUND and MUSIC toggles behave as labeled.
- [ ] Layout fit: controls do not cover the canvas.
- [ ] Notes:

## Desktop Keyboard Regression

- [ ] Arrow keys move.
- [ ] WASD moves.
- [ ] Space starts from title and pauses/resumes during play.
- [ ] Enter starts/restarts from title or game-over.
- [ ] P pauses/resumes.
- [ ] Canvas mouse swipe/tap steers only when started on the canvas.

## Safari iPhone Observations

- Device:
- iOS version:
- Safari version:
- Small Portrait Phone: Not tested yet.
- Tall Portrait Phone: Not tested yet.
- Landscape Phone: Not tested yet.
- Main issues found:
- Positive findings:

## Chrome Android Observations

- Device:
- Android version:
- Chrome version:
- Small Portrait Phone: Not tested yet.
- Tall Portrait Phone: Not tested yet.
- Landscape Phone: Not tested yet.
- Main issues found:
- Positive findings:

## Follow-up Decisions

Fill these after real-device QA.

- Sizing decision:
  - Current status: pending real-device observations.
  - Action if cramped: tune portrait canvas/control spacing in `issues/003-short-portrait-layout-tuning.md`.
- Landscape decision:
  - Current status: pending real-device observations.
  - Action if cramped/clipped: handle in `issues/005-landscape-mobile-layout-decision.md`.
- Held state decision:
  - Current status: implemented; verify visible feedback on real devices.
  - Action if feedback unclear: tune held-button and pressed feedback.
- Restart safety decision:
  - Current status: implemented as long press; verify on real devices.
  - Action if accidental taps occur: increase delay or strengthen visual arming feedback.
- Whole-page swipe decision:
  - Current status: implemented; verify no unwanted page panning or double-triggering.
  - Action if unreliable: revisit document-level pointer handling.
- Canvas tap-to-turn decision:
  - Current status: implemented; verify it does not fight continuous swiping.
  - Action if confusing: tune threshold or documentation.
- Audio decision:
  - Current status: generated sound effects and generated music implemented; verify mobile unlock behavior.
  - Action if unreliable: revisit Web Audio unlock path.
- Test needs decision:
  - Current status: pending real-device observations.
  - Action if regressions remain likely: evaluate browser interaction tests in `issues/007-browser-interaction-test-decision.md`.
