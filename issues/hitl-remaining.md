# Remaining HITL Work

Parent PRD: `issues/prd.md`

This file tracks the human/device validation still needed after implementation of issues `001` through `007`.

## Summary

Code and static tests are complete for the mobile gameplay improvement pass. Remaining work is human-in-the-loop validation on real devices and recording observations back into the QA/decision files.

## Still Needed

### 1. Real Safari iPhone QA

Record results in `issues/mobile-qa-checklist.md`.

- [ ] Fill device, iOS version, and Safari version.
- [ ] Test small portrait phone behavior.
- [ ] Test tall portrait phone behavior.
- [ ] Test landscape phone behavior.
- [ ] Check maze readability.
- [ ] Check D-pad reachability.
- [ ] Check page scrolling during button press/hold.
- [ ] Check held direction repeat for at least 2 seconds per direction.
- [ ] Check pause one-tap behavior.
- [ ] Check long-press restart behavior.
- [ ] Check short taps on restart do not restart active gameplay.
- [ ] Check no text selection, zoom, or tap-highlight distraction during play.
- [ ] Record main issues found.
- [ ] Record positive findings.

### 2. Real Chrome Android QA

Record results in `issues/mobile-qa-checklist.md`.

- [ ] Fill device, Android version, and Chrome version.
- [ ] Test small portrait phone behavior.
- [ ] Test tall portrait phone behavior.
- [ ] Test landscape phone behavior.
- [ ] Check maze readability.
- [ ] Check D-pad reachability.
- [ ] Check page scrolling during button press/hold.
- [ ] Check held direction repeat for at least 2 seconds per direction.
- [ ] Check pause one-tap behavior.
- [ ] Check long-press restart behavior.
- [ ] Check short taps on restart do not restart active gameplay.
- [ ] Check no text selection, zoom, or tap-highlight distraction during play.
- [ ] Record main issues found.
- [ ] Record positive findings.

### 3. Representative Landscape Viewport QA

Use `issues/landscape-layout-decision.md` as reference.

- [ ] Check 667x375.
- [ ] Check 740x360.
- [ ] Check 844x390.
- [ ] Check 932x430.
- [ ] Confirm controls are reachable beside the canvas.
- [ ] Confirm controls do not cover the canvas.
- [ ] Confirm layout avoids gameplay-disrupting page scroll.
- [ ] Confirm portrait layout still behaves as expected after landscape changes.

### 4. Restart Safety Validation

Use `issues/restart-safety-decision.md` as reference.

- [ ] Confirm mobile restart requires deliberate long press.
- [ ] Confirm short tap does not restart.
- [ ] Confirm releasing/cancelling before 900 ms cancels restart.
- [ ] Confirm pause remains one tap.
- [ ] Confirm desktop Enter restart behavior remains unchanged.
- [ ] Decide whether the `Hold restart` label is clear enough on real devices.

### 5. Browser Automation Revisit

Use `issues/browser-interaction-test-decision.md` as reference.

- [ ] Keep current decision if manual QA finds no recurring interaction regressions.
- [ ] Reopen browser automation decision if Safari/Chrome QA finds D-pad hold/release issues.
- [ ] Reopen browser automation decision if long-press restart misfires or fails.
- [ ] Reopen browser automation decision if layout regressions recur after CSS changes.
- [ ] If automation is added later, keep it cross-platform and avoid platform-specific scripts.

## Done By Code/Static Tests

- [x] Mobile-control tests target current HTML file.
- [x] QA checklist artifact exists.
- [x] Short portrait layout contract exists.
- [x] Held D-pad active-state contract exists.
- [x] Landscape layout decision exists.
- [x] Landscape CSS layout contract exists.
- [x] Restart safety decision exists.
- [x] Long-press mobile restart contract exists.
- [x] Browser automation decision exists.

## Current Verification Command

```sh
python -B -m unittest tests/test_mobile_controls.py tests/test_mobile_qa_checklist.py
```

Expected current result: all tests pass.
