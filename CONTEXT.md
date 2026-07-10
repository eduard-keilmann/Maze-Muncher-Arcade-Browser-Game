# Maze Muncher

Maze Muncher is a browser maze-chase game context. This glossary fixes the game-design language used when comparing the project to original Pac-Man.

## Language

**Original-like dynamics**:
Gameplay behavior that follows original Pac-Man's major pressure, pacing, scoring, and ghost-behavior patterns without requiring frame-perfect arcade emulation.
_Avoid_: exact clone, arcade-perfect clone, ROM-accurate behavior

**Arcade-accurate clone**:
A frame-precise recreation target where original timing tables, movement quirks, bugs, and edge cases are reproduced as closely as possible.
_Avoid_: original-like dynamics

**Step-band formulas**:
Level-scaling rules that use a small number of original-like level ranges instead of exact tables or smooth per-level growth.
_Avoid_: exact level table, smooth linear scaling

**Level band**:
A named range of levels that shares the same original-like gameplay tuning.
_Avoid_: exact round table row

**Power pellet**:
A large pellet that always scores points and disrupts ghost movement, and only makes ghosts edible on level bands with frightened time above zero.
_Avoid_: plain pellet, guaranteed ghost-eating pellet

**Frightened time**:
The short period after a power pellet during which normal ghosts are edible.
_Avoid_: power-up duration, invincibility

**Tunnel slowdown**:
The rule that ghosts move slower while crossing the side tunnel, making tunnel escapes tactically valuable.
_Avoid_: tunnel wrap, player slowdown

**Bonus fruit**:
A temporary bonus target whose identity and value follow the current level, while its visual art may be simpler than its name.
_Avoid_: cherry for all levels

**Ghost house release**:
The rule that sends ghosts out of the home box using pellet progress with a timer fallback.
_Avoid_: pure timed release

**Cruise Elroy**:
The late-board red-ghost behavior where red becomes faster and keeps pressure on the player when few pellets remain.
_Avoid_: universal red speed boost

**Scatter/chase cycle**:
The repeating mode schedule that alternates ghost corner pressure with direct player pressure, interrupted by frightened time.
_Avoid_: fixed global mode cycle

**Extra life**:
A once-per-game bonus life awarded when score first crosses the configured score threshold.
_Avoid_: repeated bonus life

**Ghost personality**:
The target-selection behavior that makes each ghost pressure the player differently.
_Avoid_: identical ghost AI

**Gameplay mode**:
A player-selectable rule set that changes gameplay tuning while keeping the same maze-chase game identity.
_Avoid_: level, difficulty setting

**Original-like mode**:
A gameplay mode that uses original-like dynamics.
_Avoid_: forced replacement, arcade-accurate clone

**Old-like mode**:
The player-facing label for Original-like mode. It is currently the default gameplay mode, while Maze Muncher mode remains selectable.
_Avoid_: original-like UI label, only available mode

**Touch steering**:
The mobile input family where whole-page continuous swipe, canvas tap-to-turn, and the touch D-pad all route into the shared direction input path.
_Avoid_: separate mobile movement physics

**Online leaderboard**:
An optional shared ranking of completed game scores, stored outside the browser and unavailable without its server endpoint.
_Avoid_: Redis connection from browser, replacement for local high score

**Plausibility-checked run**:
A completed game attempt accepted for the **Online leaderboard** after server-side consistency checks, without claiming proof that its browser client was unmodified.
_Avoid_: cheat-proof score, server-authoritative game

**Mode leaderboard**:
The **Online leaderboard** ranking for exactly one **Gameplay mode**.
_Avoid_: cross-mode leaderboard

**Leaderboard name**:
The freely chosen visible name attached to a **Plausibility-checked run**, limited to a trimmed, non-empty, control-character-free Unicode string of at most 20 characters.
_Avoid_: account name, verified identity

**Leaderboard entry**:
A visible record of one **Plausibility-checked run**, consisting of its **Leaderboard name** and score.
_Avoid_: player account, unique player record

## Relationships

- **Original-like dynamics** may use original Pac-Man tables and mechanics while keeping Maze Muncher identity.
- **Arcade-accurate clone** requires stricter precision than **Original-like dynamics**.
- **Step-band formulas** are one implementation style for **Original-like dynamics**.
- **Level bands** for **Step-band formulas** are `1`, `2-4`, `5-8`, `9-16`, and `17+`.
- A **Power pellet** has **Frightened time** only when the current **Level band** allows it.
- **Tunnel slowdown** affects ghosts, not the player.
- **Bonus fruit** appears during a level and uses original-like level-based value.
- **Ghost house release** depends on level pellet progress and may release ghosts quickly after player death.
- **Cruise Elroy** applies to red ghost only while red is in normal chase-capable state.
- **Scatter/chase cycle** varies by **Level band** and is paused during **Frightened time**.
- **Extra life** does not change the current total-lives display model.
- **Ghost personality** should remain approximate original behavior, not exact arcade emulation.
- **Original-like mode** is a **Gameplay mode**, not a forced replacement for existing Maze Muncher tuning.
- **Old-like mode** labels **Original-like mode** in the player UI.
- **Old-like mode** is the current default **Gameplay mode**, but Maze Muncher mode remains selectable.
- Each **Gameplay mode** has its own high score.
- **Touch steering** should not create separate movement rules; it should feed the same direction path as keyboard controls.
- An **Online leaderboard** is optional; its absence preserves the existing per-**Gameplay mode** local high score behavior.
- An **Online leaderboard** ranks **Plausibility-checked runs** only.
- An **Online leaderboard** contains one **Mode leaderboard** per **Gameplay mode**.
- A **Plausibility-checked run** has one **Leaderboard name** and does not identify a real-world player.
- A **Mode leaderboard** displays its top 100 **Leaderboard entries**.
- Multiple **Leaderboard entries** may use the same **Leaderboard name**.

## Example Dialogue

> **Dev:** "Should level 256 split-screen behavior be part of original-like dynamics?"
> **Domain expert:** "No. Original-like dynamics means the important gameplay pressure, not arcade-perfect hardware bugs."

## Flagged Ambiguities

- "closer to original Pac-Man" resolved as **Original-like dynamics**, not **Arcade-accurate clone**.
- Difficulty progression should use **Step-band formulas**, not exact level tables or smooth linear scaling.
- Late-game **Power pellets** should reverse normal ghosts but not create edible ghosts when **Frightened time** is zero.
- Ghost speed should use original-like **Level bands**, including **Tunnel slowdown**.
- **Bonus fruit** should get original-like names and values before adding distinct fruit drawings.
- **Ghost house release** should use pellet-count thresholds with timer fallback; thresholds already passed remain passed after player death.
- **Cruise Elroy** should not affect frightened or eaten red ghost states.
- **Scatter/chase cycle** should become chase-heavy in later **Level bands**.
- **Extra life** should be awarded once at 10,000 points.
- **Ghost personality** should keep current targeting patterns, with random frightened movement and a **Cruise Elroy** red override.
- Original-like gameplay changes should ship in phases, not one large change.
- **Gameplay mode** switching should happen only before a run starts, from title or game-over state.
- Maze Muncher mode preserves current tuning unless a shared bug fix is needed.
- **Gameplay mode** switching changes selected mode and displayed high score, but does not auto-start a run.
- Current **Gameplay mode** should be visible during play through a compact footer label.
- Current Old-like **Frightened time** tuning is `7`, `6`, `3.5`, `2`, and `0` seconds for level bands `1`, `2-4`, `5-8`, `9-16`, and `17+`.
- Canvas tap-to-turn should choose direction relative to Maze Muncher position; continuous swipe should remain available and low-latency.
- Online score validation should deter casual manipulation through run tickets, score and duration plausibility, one submission per run, and rate limiting; it is not server-authoritative gameplay.
