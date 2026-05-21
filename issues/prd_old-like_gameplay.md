## Problem Statement

Maze Muncher is already playable as a compact browser maze-chase game, but its gameplay dynamics are only loosely inspired by original Pac-Man. Levels currently scale through smooth formulas, fruit is always cherry-like with formula-based values, power pellets stay useful too long, ghost house release is timed only, there is no Cruise Elroy pressure, tunnels do not slow ghosts, and there is no extra-life threshold.

The user wants gameplay that feels closer to original Pac-Man dynamics without turning Maze Muncher into an arcade-perfect clone. The existing Maze Muncher behavior must remain available. The original-like behavior should be an alternative player-selectable gameplay mode named "Old-like" in the UI, introduced in phases so each change can be tested and tuned safely.

## Solution

Add gameplay modes. Keep the current Maze Muncher tuning available as a selectable baseline mode, and add an Old-like mode that approximates original Pac-Man pressure, pacing, scoring, fruit progression, ghost timing, and late-board tension. Old-like is now the default mode.

The work should be phased:

1. Add mode infrastructure first, with no gameplay differences yet.
2. Add Old-like core dynamics: level-band formulas, speed tuning, frightened-time behavior, fruit values, extra life, and ghost tunnel slowdown.
3. Add Old-like ghost-pressure dynamics: pellet-based ghost house release, Cruise Elroy, level-band scatter/chase cycles, and simplified frightened movement.

The user should choose the gameplay mode before starting a run when changing away from the default. Mode switching should be allowed on title and game-over screens, persisted across sessions, and reflected in separate high scores. The active mode should also be visible during play through a compact footer label.

## User Stories

1. As a player, I want the current Maze Muncher mode to remain available, so that I can keep playing the familiar version.
2. As a player, I want an Old-like mode, so that the game feels closer to original Pac-Man dynamics.
3. As a player, I want to switch mode before starting a run, so that I can choose the rule set intentionally.
4. As a player, I want mode switching on the title screen, so that I can choose before playing.
5. As a player, I want mode switching on the game-over screen, so that I can change mode between runs.
6. As a player, I do not want mode switching during active play, so that physics and scoring do not change mid-run.
7. As a player, I want the mode choice saved, so that the game remembers my preferred mode.
8. As a player, I want Old-like mode labeled clearly as "MODE: OLD-LIKE", so that the choice is short and understandable.
9. As a player, I want Maze Muncher mode labeled clearly as "MODE: MAZE MUNCHER", so that I know when I am using the current tuning.
10. As a player, I want the current gameplay mode visible during play, so that I can confirm which rule set is active.
11. As a player, I want separate high scores per gameplay mode, so that scores are comparable within the same rules.
12. As a player, I want switching modes on title or game-over to update the displayed high score, so that I immediately see the selected mode's record.
13. As a player, I want switching modes not to auto-start a game, so that mode choice and run start remain separate actions.
14. As a player, I want Old-like mode to use level bands instead of smooth scaling, so that difficulty changes feel closer to original Pac-Man.
15. As a player, I want early Old-like levels to feel forgiving, so that the mode is learnable.
16. As a player, I want mid Old-like levels to become noticeably more dangerous, so that progression creates real pressure.
17. As a player, I want late Old-like levels to become chase-heavy, so that clearing boards feels tense.
18. As a player, I want power pellets in early Old-like levels to make ghosts edible for useful time, so that I can hunt ghosts.
19. As a player, I want power pellets in later Old-like levels to lose most edible time, so that late levels feel more like original Pac-Man.
20. As a player, I want late Old-like power pellets to still reverse ghosts, so that they remain tactical even when ghosts are not edible.
21. As a player, I want ghost combo scoring to remain possible only when ghosts are actually edible, so that scoring matches the visible risk.
22. As a player, I want ghosts to slow in tunnels in Old-like mode, so that tunnel escapes become tactically valuable.
23. As a player, I want the player not to slow in tunnels, so that tunnels feel like a useful escape tool.
24. As a player, I want Old-like fruit values to follow an original-like sequence, so that bonus scoring feels familiar.
25. As a player, I want level 1 Old-like fruit to behave like cherry scoring, so that the first board resembles original Pac-Man.
26. As a player, I want later Old-like fruit values to increase by level, so that bonus fruit stays meaningful.
27. As a player, I accept that fruit art can remain simple at first, so that gameplay dynamics improve before visual polish.
28. As a player, I want one extra life at 10,000 points in Old-like mode, so that scoring milestones matter.
29. As a player, I want the extra life awarded only once per game, so that it resembles original arcade behavior.
30. As a player, I want the current lives display model preserved, so that the UI remains simple.
31. As a player, I want ghosts to leave the house based on pellet progress in Old-like mode, so that opening pressure feels more authentic.
32. As a player, I want ghost release to include timer fallback, so that ghosts do not stay trapped if I avoid pellets.
33. As a player, I want ghost release thresholds already passed to remain passed after death, so that late-board recovery is not too easy.
34. As a player, I want red ghost to enter Cruise Elroy behavior when few pellets remain, so that late-board clears become tense.
35. As a player, I want Cruise Elroy to apply only to normal red ghost behavior, so that frightened and eaten states remain understandable.
36. As a player, I want red ghost in Elroy state to keep pressure even during scatter, so that the late board has a distinct threat.
37. As a player, I want scatter/chase timing to vary by level band in Old-like mode, so that higher levels become less forgiving.
38. As a player, I want frightened mode to interrupt normal scatter/chase timing, so that existing power-pellet flow remains understandable.
39. As a player, I want ghost personalities to remain recognizable, so that each ghost still pressures me differently.
40. As a player, I want frightened ghost movement to feel unpredictable, so that frightened mode does not look like normal chasing.
41. As a player, I want Old-like changes introduced gradually, so that the mode can be tuned if it becomes too hard.
42. As a desktop player, I want keyboard controls preserved, so that gameplay-mode work does not regress existing input.
43. As a mobile player, I want touch controls preserved, so that the new mode remains playable on phones.
44. As a maintainer, I want mode infrastructure separated from gameplay changes, so that UI/state bugs are easier to isolate.
45. As a maintainer, I want gameplay tuning behind small named rule functions, so that Old-like behavior is readable and adjustable.
46. As a maintainer, I want current Maze Muncher tuning preserved unless a shared bug fix is needed, so that old behavior does not drift silently.
47. As a maintainer, I want tests for each phase, so that mode selection and gameplay rules do not regress.
48. As a maintainer, I want static tests to remain dependency-free, so that the project stays lightweight.
49. As a maintainer, I want the Old-like mode to avoid exact ROM emulation, so that implementation remains practical in a static browser game.
50. As a maintainer, I want documentation to distinguish Old-like mode from an arcade-accurate clone, so that future changes follow the intended target.

## Implementation Decisions

- Add a player-selectable gameplay mode concept with two modes: current Maze Muncher tuning and Old-like tuning.
- The UI label for the original-like mode is "Old-like"; internal documentation may continue using "original-like dynamics" for precision.
- Old-like mode is the default. The current Maze Muncher mode is preserved as a selectable baseline, so Old-like is additive and not a forced replacement.
- Mode switching is allowed only before a run starts, on title and game-over states.
- Mode switching updates selected mode and displayed high score but does not start a new run automatically.
- Selected gameplay mode is persisted locally.
- High scores are separated by gameplay mode.
- The active gameplay mode is shown during play through a compact footer label.
- Implement mode work in phases: mode infrastructure, Old-like core dynamics, then Old-like ghost-pressure dynamics.
- Phase 0 adds mode state, mode toggle UI, persisted selected mode, separate high-score handling, active-mode display, and static tests. Both modes behave identically in this phase.
- Phase 1 adds Old-like level-band formulas for player speed, ghost speed, frightened time, fruit values, extra life, and tunnel slowdown.
- Phase 2 adds Old-like pellet-count ghost release, timer fallback, Cruise Elroy, level-band scatter/chase cycles, and simplified frightened movement.
- Old-like difficulty uses step-band formulas, not exact level tables and not smooth linear scaling.
- Old-like level bands are level 1, levels 2-4, levels 5-8, levels 9-16, and levels 17+.
- Old-like frightened time is useful early, short in the middle game, and zero in late game. Current tuned values are 7, 6, 3.5, 2, and 0 seconds across the configured level bands.
- Power pellets always score points and reverse normal ghosts. They only make ghosts edible when the current Old-like frightened time is above zero.
- Old-like player and ghost speeds use level bands so ghosts close the pressure gap over time.
- Ghost tunnel slowdown applies to ghosts only, and not while eaten.
- Old-like bonus fruit uses original-like names and values by level. Distinct fruit drawings are deferred.
- Old-like extra life is awarded once when score first crosses 10,000 points.
- The current total-lives model remains unchanged.
- Old-like ghost house release uses pellet progress with timer fallback.
- After death, ghost release uses the current level's existing pellet progress rather than resetting progress.
- Old-like Cruise Elroy applies only to red ghost in normal chase-capable state.
- Cruise Elroy does not affect frightened or eaten red ghost states.
- Old-like scatter/chase timing varies by level band and becomes chase-heavy later.
- Frightened mode continues to interrupt normal scatter/chase timing.
- Current ghost target personalities remain mostly unchanged.
- Old-like frightened ghost movement is simplified to random available non-reverse movement.
- Keep the static single-file browser-game architecture. Do not add build tooling or dependencies for this feature.
- Keep game rules in named JavaScript functions rather than spreading mode-specific logic through input handlers or rendering code.
- Keep input adapters thin. Keyboard, swipe, touch controls, pause, restart, and mode selection should call shared game actions.
- Keep rendering responsible for display only. Rendering may read mode state but should not own gameplay decisions.
- Deep module opportunity: centralize all gameplay tuning behind small stable functions for mode-aware rule lookup. These functions should encapsulate many gameplay differences behind simple interfaces.
- Deep module opportunity: centralize score changes behind one scoring path so high score and extra-life handling are consistent across pellets, fruit, and ghosts.

## Testing Decisions

- Good tests should verify externally meaningful behavior and public page contract, not fragile implementation details.
- Continue using dependency-free static Python tests as the baseline test strategy.
- Add or update tests per implementation phase.
- Phase 0 tests should verify the mode button exists, both player-facing mode labels exist, selected mode persistence exists, Old-like high-score storage exists, and mode switching is constrained to pre-run states.
- Phase 1 tests should verify Old-like tuning functions exist, frightened time can reach zero, original-like fruit values exist, the 10,000-point extra-life threshold exists, and tunnel slowdown exists.
- Phase 2 tests should verify ghost release specification exists, Cruise Elroy specification exists, level-band scatter/chase cycle behavior exists, and frightened movement no longer mixes in chase targeting.
- Existing mobile-control tests are prior art for static contract tests.
- Tests should preserve the project's no-build, no-dependency approach.
- Manual playtesting should compare Maze Muncher mode and Old-like mode after Phase 1 and Phase 2.
- Manual playtesting should check that Old-like mode feels closer to original Pac-Man without becoming an exact clone requirement.
- Manual playtesting should check that mode switching cannot unexpectedly mutate an active run.
- Manual playtesting should include desktop keyboard and mobile touch controls to ensure gameplay-mode work does not regress input.

## Out of Scope

- Arcade-perfect or ROM-accurate Pac-Man emulation.
- Frame-perfect timing.
- Exact original PRNG behavior.
- Exact original hardware bugs or level 256 behavior.
- Replacing Maze Muncher mode with Old-like mode.
- Switching gameplay mode during active play.
- Adding a full settings menu.
- Copying original Pac-Man audio or melody.
- Adding multiple mazes.
- Adding distinct fruit artwork in the first gameplay-dynamics pass.
- Adding new dependencies or a build system.
- Rewriting the game into multiple source files unless a separate architecture decision is made.
- Changing mobile controls except where needed to expose the mode toggle safely.

## Further Notes

The agreed product language is:

- "Original-like dynamics" means major original Pac-Man pressure, pacing, scoring, and ghost-behavior patterns without frame-perfect arcade emulation.
- "Old-like mode" is the player-facing label for original-like gameplay.
- "Step-band formulas" means compact level-range formulas that approximate original progression without exact tables.

Recommended implementation order:

1. Implement Phase 0 and verify the user can switch between Maze Muncher and Old-like mode without changing gameplay yet.
2. Implement Phase 1 and tune the immediate feel of Old-like mode.
3. Implement Phase 2 after Phase 1 feels stable, because ghost release, Cruise Elroy, and scatter/chase timing can significantly increase difficulty.

Success criteria:

- Maze Muncher mode still behaves like the current game.
- Old-like mode is the default, persists, and has separate high score; Maze Muncher mode remains selectable.
- Old-like mode becomes meaningfully closer to original Pac-Man dynamics.
- The project remains a static, dependency-light browser game.
- Tests document the public behavior expected from each phase.
