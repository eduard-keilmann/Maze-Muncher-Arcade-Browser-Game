# Maze Muncher

A fast little browser arcade game inspired by classic maze chases. Eat every pellet, grab power pellets, turn the chase around, and survive the ghosts long enough to clear the maze.

No install. No build. Open one HTML file and play.

## Play

Open the actual game file in a browser:

```text
maze_muncher_browser_arcade.html
```

Or play online:

- Gameplay instructions: https://eduard-keilmann.github.io/Maze-Muncher-Arcade-Browser-Game/
- Play the game: https://eduard-keilmann.github.io/Maze-Muncher-Arcade-Browser-Game/maze_muncher_browser_arcade.html

The game runs directly in a modern browser.

## Why Try It

- Classic pellet-chasing tension in a compact browser game.
- Smooth grid movement with buffered turns.
- Four ghosts with chase, scatter, frightened, home, and eaten states.
- Power pellets let you hunt the ghosts for combo points.
- Score, high score, lives, levels, pause, ready, death, game-over states, and generated arcade-style sound effects and quiet threat-reactive music.
- Works on desktop and touch screens.

## Controls

Desktop:

- Move: Arrow keys or WASD
- Start: Space, Enter, or a movement key
- Pause/resume: Space or P
- Sound: use SOUND: ON/OFF toggle
- Music: use MUSIC: ON/OFF toggle
- Restart from title/game-over: Enter

Touch/mobile:

- Move: use continuous swipe anywhere on the game page or use the on-screen D-pad
- Hold a D-pad direction to keep that turn queued
- Pause: tap Pause
- Restart: hold Restart
- Sound: use SOUND: ON/OFF toggle
- Music: use MUSIC: ON/OFF toggle

## Mobile-Friendly

Maze Muncher includes thumb-friendly controls for phones and tablets:

- large on-screen D-pad
- press-and-hold direction input
- visible held-button feedback
- compact short-phone portrait layout
- side-by-side short landscape layout
- safer long-press restart to avoid accidental resets

## Run Tests

The repo uses dependency-free Python tests for the static HTML contract:

```sh
python -B -m unittest tests/test_mobile_controls.py tests/test_mobile_qa_checklist.py
```

## Project Notes

- Main game file: `maze_muncher_browser_arcade.html`
- Product notes: `specs_product.md`
- Architecture notes: `specs_architecture.md`
- Mobile QA checklist: `issues/mobile-qa-checklist.md`
- Remaining human/device validation: `issues/hitl-remaining.md`
