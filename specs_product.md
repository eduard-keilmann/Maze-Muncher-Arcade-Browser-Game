# Pacman Arcade Product Spec

## Purpose

Pacman Arcade is a lightweight browser maze-chase game. Player controls a maze muncher, eats pellets, avoids ghosts, uses power pellets to reverse chase pressure, and advances levels after clearing the maze.

The game should run from a static HTML file with no build step and no required server.

## Core Gameplay

- Player starts from title screen and can begin a new game with keyboard, swipe, canvas tap, or touch controls.
- Player moves through a tile maze with buffered turns and immediate reverse turns.
- Pellets add score. Power pellets add score, trigger frightened ghosts, and allow ghost-eating score chains.
- Ghosts use deterministic maze movement with chase, scatter, home, leaving, frightened, and eaten states.
- Level clears when all pellets are eaten.
- Player has lives, score, high score, level display, ready/death/game-over/pause overlays, and generated arcade-style sound effects and quiet threat-reactive music.

## Supported Inputs

- Desktop:
  - Arrow keys and WASD move.
  - Space starts or pauses/resumes.
  - Enter starts/restarts from title or game-over.
  - P pauses/resumes.
  - Sound toggle enables/disables generated arcade-style effects. Music toggle enables/disables quiet threat-reactive music.
- Touch/mobile:
  - Canvas swipe changes direction.
  - On-screen D-pad changes direction.
  - Press-and-hold D-pad repeats the selected direction so queued turns remain responsive.
  - Touch pause button starts from title/game-over or pauses/resumes during active play.
  - Touch restart button starts a fresh game.
  - Sound and music toggles work on desktop and touch, with preferences saved locally.

## Mobile Experience Goals

- Controls must be thumb-friendly on Safari and Chrome mobile browsers.
- Touch targets should be large enough for reliable one-thumb play.
- Main canvas should remain large enough to read the maze while leaving room for controls below it.
- Controls should avoid browser scrolling, selection, and tap-highlight interference during play.
- Restart should be available but visually less dominant than movement and pause.

## Current Implemented Mobile Features

- On-screen directional pad below the canvas.
- Large touch buttons.
- Press-and-hold directional behavior.
- Pause and restart touch buttons.
- Mobile media query for tighter spacing and visible controls on coarse pointers/small screens.
- Generated Web Audio effects for start, pellets, power pellets, fruit, ghost-eaten, death, and level clear. Generated quiet music pulse reacts to nearby danger, chase pressure, low pellets, and frightened ending.

## Remaining Mobile Improvement Candidates

- Verify layout on real Safari iPhone and Chrome Android devices.
- Tune canvas/control sizing for short mobile viewports.
- Add landscape-specific layout if portrait controls feel cramped.
- Add touch-control pressed/active visual state that remains visible while held.
- Prevent accidental restart with a confirm/long-press pattern if testing shows accidental resets.
- Add browser-based interaction tests if a lightweight cross-platform browser test stack is introduced.
