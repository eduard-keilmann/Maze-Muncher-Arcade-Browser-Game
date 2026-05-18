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

## Relationships

- **Original-like dynamics** may use original Pac-Man tables and mechanics while keeping Maze Muncher identity.
- **Arcade-accurate clone** requires stricter precision than **Original-like dynamics**.
- **Step-band formulas** are one implementation style for **Original-like dynamics**.

## Example Dialogue

> **Dev:** "Should level 256 split-screen behavior be part of original-like dynamics?"
> **Domain expert:** "No. Original-like dynamics means the important gameplay pressure, not arcade-perfect hardware bugs."

## Flagged Ambiguities

- "closer to original Pac-Man" resolved as **Original-like dynamics**, not **Arcade-accurate clone**.
- Difficulty progression should use **Step-band formulas**, not exact level tables or smooth linear scaling.
