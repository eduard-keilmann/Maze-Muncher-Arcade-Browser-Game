## What to build

Deepen generated audio and threat-reactive music into one local Module so Web Audio setup, iPhone unlock, sound preferences, music preferences, tone scheduling, and threat pulse decisions have better locality.

This slice preserves current behavior:

- No audio files.
- No copied Pac-Man melody.
- Sound effects stay separate from music.
- Sound toggle controls event effects.
- Music toggle controls quiet threat-reactive pulse.
- Music stops outside active playing state.
- Music responds to nearby dangerous ghosts, chase pressure, low pellets, frightened ending, and Cruise Elroy pressure.
- Audio unlock works through touch/click/user gestures.

Architecture target:

- Game loop should supply events and danger facts; audio Module should own Web Audio details.
- Keep the interface small: enable/disable, unlock, play event sound, update music from game facts.
- Keep threat formula readable and testable.
- Avoid gameplay rules hiding inside audio implementation beyond music danger scoring.

## Acceptance criteria

- [ ] Sound and music toggles still persist user preference.
- [ ] Generated Web Audio remains the only audio source.
- [ ] Audio unlock still works through the existing iPhone-safe gesture path.
- [ ] Sound effects still fire for start, pellet, power pellet, fruit, ghost eaten, death, and level clear.
- [ ] Music loop remains gated to active playing state and stops on title, game-over, pause, death, ready, and level clear.
- [ ] Threat computation still uses ghost distance, pellets remaining, Scatter/chase cycle, frightened ending, and Elroy pressure.
- [ ] Static tests cover the deepened audio Module behavior where practical.
- [ ] Full test suite passes.

## Blocked by

None - can start immediately
