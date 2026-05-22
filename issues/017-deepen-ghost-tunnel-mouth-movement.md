## What to build

Deepen the ghost movement path around tunnel mouths so ghosts use normal target selection at the tunnel entry, and only use forced tunnel continuation after they are truly inside the side tunnel.

This slice keeps the current single-file static game shape. The goal is better locality for the known tunnel-entry bug: red and other ghosts should not enter the tunnel just because they are next to the tunnel mouth when their target says otherwise.

Use the project glossary terms:

- Ghost personality
- Tunnel slowdown
- Original-like dynamics
- Old-like mode

Architecture target:

- Create a deeper ghost tunnel-movement Module, even if it remains inside the HTML script for now.
- Keep the interface small: given ghost state, tile position, direction, and target context, choose the next legal movement direction.
- Keep tunnel special cases behind this Module, not spread across unrelated movement callers.
- Preserve the existing public game controls and rendering.

## Acceptance criteria

- [x] At a tunnel mouth, red ghost chase targeting can choose a non-tunnel direction when Maze Muncher is elsewhere.
- [x] Tunnel continuation is applied only after a ghost is inside the side tunnel lane or offscreen tunnel wrap area.
- [x] Hidden tunnel dead-end escape logic still prevents ghosts from freezing inside the side tunnel.
- [x] Tunnel slowdown remains applied to normal ghosts in Old-like mode and not to Maze Muncher.
- [x] Maze Muncher mode keeps existing tuning unless the tunnel fix is a shared bug fix.
- [x] Static tests cover tunnel-mouth target selection, tunnel continuation after entry, and no forced tunnel entry at mouth.
- [x] Full test suite passes.

## Blocked by

None - can start immediately
