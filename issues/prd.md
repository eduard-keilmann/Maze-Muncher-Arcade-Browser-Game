## Problem Statement

Mobile gameplay is now functional, but not yet systematically validated or polished for real Safari and Chrome phone use. The current touch controls provide a D-pad, large buttons, press-and-hold direction behavior, pause, restart, and mobile spacing. Remaining risk is practical playability: short screens may feel cramped, landscape may be awkward, held buttons may not clearly show active state, restart may be too easy to hit by accident, and tests do not yet exercise real browser interaction.

The user wants a systematic plan to finish mobile gameplay improvements without overengineering the static browser-game architecture.

## Solution

Improve mobile gameplay in small, validated phases:

1. Establish a mobile QA checklist for Safari on iPhone and Chrome on Android.
2. Tune portrait layout for short mobile viewports.
3. Add a landscape-specific layout only if testing shows portrait controls do not translate well.
4. Improve held-button visual feedback so the player can see which direction is being pressed.
5. Make restart safer if testing shows accidental resets.
6. Add browser interaction tests only if the added confidence is worth the tooling.

Each phase should start with a clear acceptance check, then make the smallest implementation change needed, then re-run existing tests and perform targeted manual mobile validation.

## User Stories

1. As a mobile player, I want the maze to remain readable on a phone, so that I can plan turns and avoid ghosts.
2. As a mobile player, I want the D-pad to stay reachable below the canvas, so that one-thumb play feels natural.
3. As a mobile player, I want controls to fit on short phone screens, so that I do not need constant scrolling during play.
4. As a mobile player, I want controls to avoid browser scroll gestures, so that pressing buttons does not move the page.
5. As a mobile player, I want held direction buttons to keep queueing that direction, so that turning at intersections feels responsive.
6. As a mobile player, I want the held direction to look visibly active, so that I know the game received my input.
7. As a mobile player, I want active button feedback to remain visible while my thumb is held down, so that feedback does not depend only on a quick tap animation.
8. As a mobile player, I want the pause button to be easy to hit, so that I can stop the game quickly.
9. As a mobile player, I want restart to be available, so that I can recover from a bad run without using a keyboard.
10. As a mobile player, I want restart to be hard to trigger accidentally, so that I do not lose a good run from a stray tap.
11. As a mobile player, I want portrait mode to work well, so that the default phone orientation is comfortable.
12. As a mobile player, I want landscape mode to be usable if I rotate the phone, so that the game does not become awkward or clipped.
13. As a mobile player, I want touch controls not to cover the canvas, so that gameplay remains visible.
14. As a mobile player, I want touch controls near the canvas, so that eye movement between action and controls is minimal.
15. As a mobile player, I want consistent Safari and Chrome behavior, so that the game feels reliable across common mobile browsers.
16. As a mobile player, I want no accidental text selection or tap highlights during play, so that the game feels like an app rather than a web page.
17. As a mobile player, I want the title, help text, canvas, and controls to share space efficiently, so that the game surface is prioritized.
18. As a mobile player, I want controls to remain large enough after responsive layout changes, so that small-screen support does not make buttons too small.
19. As a mobile player, I want game controls to work with touch, stylus, and mouse pointer events, so that input behavior is consistent.
20. As a desktop player, I want existing keyboard behavior preserved, so that mobile improvements do not regress desktop play.
21. As a maintainer, I want mobile changes made in small phases, so that regressions are easy to isolate.
22. As a maintainer, I want static tests to keep checking the mobile control contract, so that important controls are not removed accidentally.
23. As a maintainer, I want manual mobile QA findings recorded as actionable decisions, so that layout changes are based on evidence.
24. As a maintainer, I want browser automation added only if needed, so that the project stays lightweight.
25. As a maintainer, I want any future browser test tooling to be cross-platform, so that the repo does not gain platform-specific scripts.

## Implementation Decisions

- Keep the app static and dependency-free unless browser-level testing becomes clearly valuable.
- Preserve existing shared game-action boundaries for direction, pause, and restart.
- Treat mobile-control work as input and layout polish, not as a gameplay-rules rewrite.
- Start with real-device QA before adding more layout complexity.
- Use measured viewport cases for QA: small portrait phone, tall portrait phone, and landscape phone.
- Prefer CSS layout changes for sizing and spacing before changing canvas internals.
- Add landscape-specific layout only after confirming the default mobile layout is not enough.
- Keep touch controls as real buttons for accessibility and browser compatibility.
- Use a persistent pressed state for held D-pad buttons if visual feedback needs improvement.
- Decide restart safety from testing: keep one-tap restart if accidental taps are not observed; otherwise use a safer interaction such as confirm or long-press.
- Keep restart visually secondary to movement and pause.
- Do not duplicate game logic inside mobile-only handlers.
- Keep the browser-event layer thin and routed through existing game actions.
- Record any durable product or architecture decisions in the existing specs after implementation choices are made.

## Testing Decisions

- Good tests should verify user-visible behavior and public page contract, not private implementation details.
- Keep existing static mobile-control tests as the baseline regression suite.
- Add or update static tests for any new public control contract, such as active-state attributes or safer restart UI text.
- Run existing Python tests after each implementation phase.
- Perform manual QA on Safari iPhone and Chrome Android for each layout-affecting phase.
- Manual QA should check portrait, short viewport, landscape, button reachability, page scrolling, held direction repeat, pause, restart, and desktop keyboard regression.
- Browser automation is optional and should be introduced only if manual QA repeatedly catches regressions that static tests cannot cover.
- If browser automation is added, it must be cross-platform and should test real interactions: tap, hold, release, rotate/responsive viewport, pause, restart safety, and keyboard preservation.

## Out of Scope

- Rewriting the game engine.
- Changing ghost AI, scoring, pellet rules, or level progression.
- Adding a build system without a separate decision.
- Adding mobile app packaging.
- Adding multiplayer, save slots, settings menus, or audio.
- Supporting unusual browsers beyond current Safari and Chrome mobile targets.
- Introducing platform-specific scripts or test files.

## Further Notes

Recommended order:

1. Fix current test target drift if the main HTML filename changed.
2. Create a manual QA checklist and capture first Safari/Chrome observations.
3. Tune portrait sizing and spacing for short screens.
4. Re-test and decide whether landscape layout is necessary.
5. Add held-button visual state if current feedback is unclear.
6. Decide restart safety from QA evidence.
7. Reassess whether browser interaction tests are worth adding.

Success criteria:

- Phone gameplay is comfortable without accidental page scroll.
- D-pad remains easy to use for repeated turns.
- Maze remains readable.
- Pause and restart are usable without restart becoming dangerous.
- Existing desktop input remains unchanged.
- Tests remain cross-platform and dependency-light.
