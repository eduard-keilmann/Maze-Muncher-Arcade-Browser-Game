# Browser Interaction Test Decision

Parent issue: `issues/007-browser-interaction-test-decision.md`

## Decision

No browser automation needed yet.

## Reasoning

Static test coverage remains green and currently checks the public mobile-control contract:

- D-pad exists and remains accessible.
- D-pad hold-repeat wiring exists.
- Pause and restart actions exist.
- Short portrait layout contract exists.
- Held D-pad active state exists.
- Landscape layout contract exists.
- Long-press restart contract exists.
- QA and decision artifacts exist.

Manual Safari/Chrome QA checklist remains required because real mobile browser behavior can still differ from static source checks, especially for touch event timing, viewport chrome, scroll behavior, and long-press feel.

Adding browser automation now would add tooling cost before real-device QA has shown recurring interaction regressions. The project should stay dependency-light until that risk is demonstrated.

## Revisit Triggers

Revisit if manual QA finds interaction regressions, especially:

- D-pad hold/release behaves differently in Safari or Chrome.
- Long-press restart misfires or fails on mobile browsers.
- Landscape or short portrait layouts regress after CSS changes.
- Desktop keyboard behavior regresses during mobile work.
- Static tests miss repeated mobile interaction failures.

## Future Tooling Constraints

If automation becomes necessary, it must be cross-platform and must add no platform-specific scripts.

Preferred future scope:

- one real hold/release D-pad interaction;
- pause at a mobile viewport;
- long-press restart at a mobile viewport;
- short portrait and landscape viewport layout checks;
- desktop keyboard preservation.

Browser automation must not replace the manual Safari/Chrome QA checklist.
