# Mobile QA Checklist

Parent issue: `issues/002-mobile-real-device-qa-checklist.md`

Use this checklist on real Safari iPhone and Chrome Android devices before changing layout further. Record device, browser, orientation, viewport notes, and exact problems observed.

## Test Setup

- Game file: `maze_muncher_browser_arcade.html`
- Start state: title screen
- Required regression command before and after mobile changes:

```sh
python -B -m unittest tests/test_mobile_controls.py tests/test_mobile_qa_checklist.py
```

## Small Portrait Phone

Suggested target: narrow/short phone viewport.

- [ ] Maze readability: pellets, walls, ghosts, player, score, lives readable.
- [ ] D-pad reachability: direction buttons reachable by thumb without awkward stretch.
- [ ] Page scrolling: button presses and holds do not cause gameplay-disrupting scroll.
- [ ] Held direction: hold each D-pad direction for at least 2 seconds; queued turns keep responding.
- [ ] Pause: pause button is easy to trigger intentionally.
- [ ] Restart: restart is available and not easy to hit accidentally.
- [ ] Touch interference: no text selection, zoom, or tap-highlight distraction during play.
- [ ] Notes:

## Tall Portrait Phone

Suggested target: common modern tall phone viewport.

- [ ] Maze readability: pellets, walls, ghosts, player, score, lives readable.
- [ ] D-pad reachability: direction buttons reachable by thumb without awkward stretch.
- [ ] Page scrolling: button presses and holds do not cause gameplay-disrupting scroll.
- [ ] Held direction: hold each D-pad direction for at least 2 seconds; queued turns keep responding.
- [ ] Pause: pause button is easy to trigger intentionally.
- [ ] Restart: restart is available and not easy to hit accidentally.
- [ ] Touch interference: no text selection, zoom, or tap-highlight distraction during play.
- [ ] Notes:

## Landscape Phone

Suggested target: same devices rotated landscape.

- [ ] Maze readability: gameplay remains readable without severe clipping.
- [ ] D-pad reachability: direction buttons are reachable and not too far from the canvas.
- [ ] Page scrolling: button presses and holds do not cause gameplay-disrupting scroll.
- [ ] Held direction: hold each D-pad direction for at least 2 seconds; queued turns keep responding.
- [ ] Pause: pause button remains usable.
- [ ] Restart: restart remains available without becoming dangerous.
- [ ] Layout fit: controls do not cover the canvas.
- [ ] Notes:

## Desktop Keyboard Regression

- [ ] Arrow keys move.
- [ ] WASD moves.
- [ ] Space starts from title and pauses/resumes during play.
- [ ] Enter starts/restarts from title or game-over.
- [ ] P pauses/resumes.

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
  - Current status: pending real-device observations.
  - Action if feedback unclear: implement persistent held-button state in `issues/004-held-dpad-active-state.md`.
- Restart safety decision:
  - Current status: pending real-device observations.
  - Action if accidental taps occur: implement safer restart in `issues/006-safer-restart-interaction.md`.
- Test needs decision:
  - Current status: pending real-device observations.
  - Action if regressions remain likely: evaluate browser interaction tests in `issues/007-browser-interaction-test-decision.md`.
