# Pacman Arcade Architecture Spec

## Architecture Style

Current project is a static single-file browser game:

- HTML defines the page shell, canvas, help text, and touch controls.
- CSS defines presentation, mobile layout, and control sizing.
- JavaScript owns game state, input handling, update loop, collision/game rules, canvas rendering, and generated sound effects and quiet dynamic music.
- Tests are dependency-free Python source contract tests for the static HTML file.

This structure is acceptable while the project remains small. Changes should stay simple and avoid adding build tooling or dependencies without clear need.

## Separation Rules

- Keep core game rules in JavaScript functions, not in HTML attributes or CSS.
- Keep rendering in canvas draw functions.
- Keep input adapters thin: keyboard, swipe, touch buttons, and sound/music toggles should call shared game actions such as direction, pause, sound, music, and new game.
- Do not duplicate movement or pause/restart business logic inside separate input handlers.
- Keep CSS responsible for layout and touch affordance only.
- Keep tests focused on user-visible behavior and public page contract.

## Current Important Boundaries

- `setDirection(dir)` is the shared direction input path.
- `togglePause()` is the shared pause/resume path.
- `newGame()` is the shared start/restart path.
- Keyboard, canvas swipe, and touch controls should reuse these functions.
- Canvas rendering functions should not know whether input came from keyboard, swipe, or D-pad.
- Sound effects and music should be generated with Web Audio; do not copy copyrighted arcade audio assets.
- Sound and music preferences should stay local to the browser via localStorage.

## Testing Strategy

- Use Python `unittest` for repo-local, cross-platform static checks while no browser test stack exists.
- Run tests with:

```sh
python -B -m unittest tests/test_mobile_controls.py
```

- Add browser-level tests only if interaction risk justifies extra tooling.
- Do not add platform-specific test scripts.

## Mobile Architecture Guidance

- Mobile controls should remain ordinary buttons for accessibility and browser compatibility.
- Use pointer events for touch controls so mouse, stylus, and touch share one path.
- Prefer event delegation inside `.touch-controls` over per-button duplicated handlers.
- Keep hold-repeat timing local to input handling; game movement should stay frame/update-loop driven.
- Avoid coupling mobile layout decisions to game physics or canvas internals.

## Dependency Policy

- Do not add dependencies for basic layout, controls, generated sound/music, or simple static tests.
- Prefer standard browser APIs and Python standard library.
- If future browser automation becomes necessary, add one well-scoped cross-platform test tool and document why.
