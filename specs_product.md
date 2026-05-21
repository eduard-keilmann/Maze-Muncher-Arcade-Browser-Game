# Pacman Arcade Product Spec

## Purpose

Pacman Arcade is a lightweight browser maze-chase game. Player controls a maze muncher, eats pellets, avoids ghosts, uses power pellets to reverse chase pressure, and advances levels after clearing the maze.

The game should run from a static HTML file with no build step and no required server.

## Core Gameplay

- Player starts from title screen and can begin a new game with keyboard, swipe, canvas tap, or touch controls.
- Default gameplay mode is Old-like. Maze Muncher mode remains selectable before a run.
- Player moves through a tile maze with buffered turns and immediate reverse turns.
- Pellets add score. Power pellets add score, reverse normal ghosts, and create ghost-eating score chains only while frightened time is active.
- Ghosts use deterministic maze movement with chase, scatter, home, leaving, frightened, and eaten states.
- Level clears when all pellets are eaten.
- Player has lives, score, high score, level display, ready/death/game-over/pause overlays, and generated arcade-style sound effects and quiet threat-reactive music.

## Supported Inputs

- Desktop:
  - Arrow keys and WASD move.
  - Space starts or pauses/resumes.
  - Enter starts/restarts from title or game-over.
  - P pauses/resumes.
  - Mouse swipe and canvas tap can steer when they start on the canvas.
  - Sound toggle enables/disables generated arcade-style effects. Music toggle enables/disables quiet threat-reactive music.
- Touch/mobile:
  - Continuous swipe anywhere on the game page changes direction before finger release.
  - Canvas tap-to-turn changes direction based on tap position relative to Maze Muncher.
  - On-screen D-pad changes direction.
  - Press-and-hold D-pad repeats the selected direction so queued turns remain responsive.
  - Touch pause button starts from title/game-over or pauses/resumes during active play.
  - Touch restart requires a deliberate long press and starts a fresh game.
  - Sound and music toggles work on desktop and touch, with preferences saved locally.

## Mobile Experience Goals

- Controls must be thumb-friendly on Safari and Chrome mobile browsers.
- Touch targets should be large enough for reliable one-thumb play.
- Main canvas should remain large enough to read the maze while leaving room for controls below it.
- Whole-page mobile swipes should steer reliably instead of panning the page during play.
- Controls should avoid browser scrolling, selection, and tap-highlight interference during play.
- Restart should be available but require deliberate intent.

## Current Implemented Mobile Features

- On-screen directional pad below the canvas.
- Large touch buttons.
- Whole-page continuous swipe steering on touch devices.
- Canvas tap-to-turn steering relative to Maze Muncher.
- Press-and-hold directional behavior.
- Visible held-button feedback and stronger pressed visual feedback.
- Haptic feedback where supported by the browser vibration API.
- Pause and long-press restart touch buttons.
- Mobile media queries for tighter spacing, short portrait layout, and side-by-side short landscape layout.
- Generated Web Audio effects for start, pellets, power pellets, fruit, ghost-eaten, death, and level clear. Generated quiet music pulse reacts to nearby danger, chase pressure, low pellets, and frightened ending.

## Remaining Mobile Improvement Candidates

- Verify layout and controls on real Safari iPhone and Chrome Android devices.
- Record real-device behavior for whole-page continuous swipe, canvas tap-to-turn, D-pad hold, long-press restart, sound unlock, and music toggle.
- Tune canvas/control sizing only if real-device QA shows cramped or clipped play.
- Add browser-based interaction tests only if repeated real-browser regressions justify the dependency cost.
