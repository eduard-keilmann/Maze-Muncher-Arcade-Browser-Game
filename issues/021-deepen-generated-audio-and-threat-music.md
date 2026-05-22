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

- [x] Sound and music toggles still persist user preference.
- [x] Generated Web Audio remains the only audio source.
- [x] Audio unlock still works through the existing iPhone-safe gesture path.
- [x] Sound effects still fire for start, pellet, power pellet, fruit, ghost eaten, death, and level clear.
- [x] Music loop remains gated to active playing state and stops on title, game-over, pause, death, ready, and level clear.
- [x] Threat computation still uses ghost distance, pellets remaining, Scatter/chase cycle, frightened ending, and Elroy pressure.
- [x] Static tests cover the deepened audio Module behavior where practical.
- [x] Full test suite passes.

## Completed

- Added local `gameAudio` seam in `maze_muncher_browser_arcade.html`.
- Moved Web Audio setup, unlock/prime path, event sound dispatch, threat scoring, and music pulse scheduling behind that seam.
- Kept existing wrapper functions thin so current game/input code stays readable.
- Changed music updates to consume a small `currentAudioFacts()` object from the game loop.

## Validation

- `python -B -m unittest discover -s tests -p 'test_sound_controls.py' -q`
- `python -B -m unittest discover tests -q`

## Blocked by

None
