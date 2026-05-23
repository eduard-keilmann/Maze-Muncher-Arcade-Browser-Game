import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "maze_muncher_browser_arcade.html"
HTML = HTML_PATH.read_text(encoding="utf-8")


def assert_html_contains(test_case, pattern, description):
    test_case.assertRegex(
        HTML,
        re.compile(pattern),
        f"Missing expected gameplay tuning behavior: {description}",
    )


def find_function_body(name):
    match = re.search(rf"function {name}\([^)]*\) \{{(?P<body>[\s\S]*?)\n    \}}", HTML)
    if not match:
        raise AssertionError(f"Missing function {name}")
    return match.group("body")


def find_object_method_body(object_name, method_name):
    match = re.search(
        rf"const {object_name}\s*=\s*\{{[\s\S]*?{method_name}\([^)]*\)\s*\{{(?P<body>[\s\S]*?)\n      \}}",
        HTML,
    )
    if not match:
        raise AssertionError(f"Missing {object_name}.{method_name}")
    return match.group("body")


class GameplayTuningTests(unittest.TestCase):
    def test_mode_aware_tuning_entry_points_exist(self):
        for name in [
            "levelBandFor",
            "getGameplayTuning",
            "playerSpeedFor",
            "ghostSpeedFor",
            "frightenedTimeFor",
            "fruitValueFor",
            "tunnelGhostSpeedMultiplierFor",
            "ghostReleaseBaseFor",
            "modeCycleFor",
        ]:
            assert_html_contains(self, rf"function {name}\(", f"{name} tuning function")

        for name in [
            "playerSpeedFor",
            "ghostSpeedFor",
            "frightenedTimeFor",
            "fruitValueFor",
            "tunnelGhostSpeedMultiplierFor",
            "ghostReleaseBaseFor",
            "modeCycleFor",
        ]:
            assert_html_contains(self, rf"{name}\(activeGameplayMode,\s*level", f"{name} uses active mode")

    def test_maze_muncher_tuning_preserves_existing_formulas(self):
        assert_html_contains(self, r'GAMEPLAY_TUNING\s*=\s*\{', "gameplay tuning registry")
        assert_html_contains(self, r'"maze-muncher":\s*\{', "Maze Muncher tuning block")
        assert_html_contains(self, r"playerSpeed:\s*\(level\)\s*=>\s*Math\.min\(123\.48,\s*99\.225 \+ level \* 2\.75625\)", "current player speed formula")
        assert_html_contains(self, r"ghostSpeed:\s*\(level\)\s*=>\s*Math\.min\(119\.07,\s*85\.995 \+ level \* 2\.8665\)", "current ghost speed formula")
        assert_html_contains(self, r"frightenedTime:\s*\(level\)\s*=>\s*Math\.max\(4\.2,\s*7\.5 - level \* 0\.25\)", "current frightened-time formula")
        assert_html_contains(self, r"fruitValue:\s*\(level,\s*mark\)\s*=>\s*Math\.min\(5000,\s*100 \+ level \* 100 \+ mark\)", "current fruit value formula")
        assert_html_contains(self, r"ghostReleaseBase:\s*\(level\)\s*=>\s*Math\.max\(0,\s*2\.5 - level \* 0\.15\)", "current ghost release formula")
        assert_html_contains(self, r"modeCycle:\s*\(\)\s*=>\s*MODE_CYCLE", "current scatter/chase cycle")

    def test_old_like_speed_bands_get_small_uniform_five_percent_bump(self):
        for band, player_speed, ghost_speed in [
            ("level-1", 101.87, 94.93),
            ("levels-2-4", 108.82, 101.87),
            ("levels-5-8", 114.66, 111.13),
            ("levels-9-16", 119.29, 119.29),
            ("levels-17-plus", 122.71, 125.02),
        ]:
            assert_html_contains(
                self,
                rf'"{band}":\s*\{{[\s\S]*?playerSpeed:\s*{player_speed}[\s\S]*?ghostSpeed:\s*{ghost_speed}',
                f"Old-like {band} speeds keep the tuned 5 percent increase",
            )

    def test_old_like_mode_cycles_use_level_bands_and_get_more_chase_heavy(self):
        assert_html_contains(self, r"OLD_LIKE_MODE_CYCLES\s*=\s*\{", "Old-like mode-cycle table")
        assert_html_contains(
            self,
            r'"level-1":\s*\[[\s\S]*?\{ mode:\s*"scatter",\s*duration:\s*7 \}[\s\S]*?\{ mode:\s*"chase",\s*duration:\s*20 \}',
            "Old-like level 1 begins with original-like scatter and chase",
        )
        assert_html_contains(
            self,
            r'"levels-2-4":\s*\[[\s\S]*?\{ mode:\s*"chase",\s*duration:\s*1033 \}',
            "Old-like levels 2-4 become chase-heavy",
        )
        assert_html_contains(
            self,
            r'"levels-5-8":\s*\[[\s\S]*?\{ mode:\s*"scatter",\s*duration:\s*5 \}[\s\S]*?\{ mode:\s*"chase",\s*duration:\s*1037 \}',
            "Old-like levels 5+ shorten scatter and extend chase",
        )
        assert_html_contains(
            self,
            r"modeCycle:\s*\(level\)\s*=>\s*OLD_LIKE_MODE_CYCLES\[levelBandFor\(level\)\]",
            "Old-like mode cycle uses level-band selection",
        )

    def test_frightened_mode_interrupts_scatter_chase_timing(self):
        update_mode_body = find_object_method_body("ghostState", "updateModeTimer")
        self.assertRegex(
            update_mode_body,
            re.compile(r"if\s*\(frightenedTimer > 0\)\s*\{[\s\S]*?frightenedTimer -= dt[\s\S]*?return;"),
            "Frightened mode should consume frightened time before scatter/chase timing",
        )
        self.assertRegex(
            update_mode_body,
            re.compile(r"modeTimer \+= dt[\s\S]*?modeCycleFor\(activeGameplayMode,\s*level\)[\s\S]*?reverseNormalGhosts\(\)"),
            "Normal scatter/chase timing should resume after frightened mode ends",
        )

    def test_old_like_level_bands_are_defined(self):
        assert_html_contains(self, r"if\s*\(level <= 1\) return \"level-1\";", "level 1 band")
        assert_html_contains(self, r"if\s*\(level <= 4\) return \"levels-2-4\";", "levels 2-4 band")
        assert_html_contains(self, r"if\s*\(level <= 8\) return \"levels-5-8\";", "levels 5-8 band")
        assert_html_contains(self, r"if\s*\(level <= 16\) return \"levels-9-16\";", "levels 9-16 band")
        assert_html_contains(self, r"return \"levels-17-plus\";", "levels 17+ band")

    def test_old_like_tuning_has_band_values_for_later_slices(self):
        assert_html_contains(self, r'"old-like":\s*\{', "Old-like tuning block")
        assert_html_contains(self, r"OLD_LIKE_LEVEL_BANDS\s*=\s*\{", "Old-like level-band table")
        for band in ["level-1", "levels-2-4", "levels-5-8", "levels-9-16", "levels-17-plus"]:
            assert_html_contains(self, rf'"{band}":\s*\{{', f"{band} tuning values")

        assert_html_contains(self, r"frightenedTime:\s*0", "late Old-like frightened time can reach zero")
        assert_html_contains(self, r'value:\s*5000', "Old-like high-value fruit tuning exists")
        assert_html_contains(self, r"tunnelGhostSpeedMultiplier:\s*0\.[0-9]+", "Old-like tunnel slowdown tuning exists")


    def test_old_like_power_mode_duration_gets_one_second_tuning_boost(self):
        for band, seconds in [
            ("level-1", 7),
            ("levels-2-4", 6),
            ("levels-5-8", 3.5),
            ("levels-9-16", 2),
            ("levels-17-plus", 0),
        ]:
            assert_html_contains(
                self,
                rf'"{band}":\s*\{{[\s\S]*?frightenedTime:\s*{seconds}',
                f"Old-like {band} frightened time",
            )

    def test_old_like_fruit_names_and_values_follow_original_like_sequence(self):
        assert_html_contains(self, r"OLD_LIKE_FRUIT_SEQUENCE\s*=\s*\[", "Old-like fruit sequence")
        for fruit_name, fruit_value in [
            ("cherry", 100),
            ("strawberry", 300),
            ("orange", 500),
            ("apple", 700),
            ("melon", 1000),
            ("galaxian", 2000),
            ("bell", 3000),
            ("key", 5000),
        ]:
            assert_html_contains(
                self,
                rf'name:\s*"{fruit_name}",\s*value:\s*{fruit_value}',
                f"Old-like {fruit_name} fruit value",
            )

        assert_html_contains(self, r"fruitValueFor\(activeGameplayMode,\s*level,\s*mark\)", "spawned fruit uses active mode value")
        assert_html_contains(self, r"fruitNameFor\(activeGameplayMode,\s*level,\s*mark\)", "spawned fruit uses active mode name")

    def test_old_like_frightened_movement_is_random_without_target_fallback(self):
        assert_html_contains(self, r"frightenedMovement:\s*\"random\"", "Old-like frightened random movement tuning")
        assert_html_contains(self, r"frightenedMovementFor\(activeGameplayMode,\s*level\)", "active mode selects frightened movement")

        choose_body = find_object_method_body("ghostPersonality", "chooseDirection")
        frightened_branch = re.search(
            r'if\s*\(frightenedTimer > 0 && g\.state === "normal"\)\s*\{(?P<body>[\s\S]*?)\n\s+\}',
            choose_body,
        )
        self.assertIsNotNone(frightened_branch, "Missing frightened ghost direction branch")
        self.assertRegex(
            frightened_branch.group("body"),
            re.compile(r'frightenedMovementFor\(activeGameplayMode,\s*level\)\s*===\s*"random"'),
            "Old-like frightened branch should force random movement",
        )

    def test_old_like_tunnel_slowdown_applies_only_to_normal_ghosts(self):
        assert_html_contains(
            self,
            r"tunnelGhostSpeedMultiplier:\s*\(\)\s*=>\s*1",
            "Maze Muncher keeps current tunnel speed behavior",
        )
        assert_html_contains(
            self,
            r"tunnelGhostSpeedMultiplier:\s*\(level\)\s*=>\s*OLD_LIKE_LEVEL_BANDS\[levelBandFor\(level\)\]\.tunnelGhostSpeedMultiplier",
            "Old-like tunnel slowdown uses level-band tuning",
        )

        actor_body = find_function_body("actorSpeed")
        self.assertRegex(
            actor_body,
            re.compile(r'actorType === "player"[\s\S]*?return player\.baseSpeed'),
            "Tunnel slowdown should not apply to the player",
        )
        self.assertRegex(
            actor_body,
            re.compile(r'actor\.state === "eaten"[\s\S]*?return Math\.min\(160,\s*normal \* 1\.85\)'),
            "Tunnel slowdown should not interfere with eaten ghost return speed",
        )
        self.assertRegex(
            actor_body,
            re.compile(r"tunnelGhostSpeedMultiplierFor\(activeGameplayMode,\s*level\)"),
            "Normal ghost speed should use mode-aware tunnel multiplier",
        )



    def test_ghosts_continue_horizontally_through_tunnel_sides(self):
        assert_html_contains(self, r"function tunnelContinuationDirection\(actor\)", "tunnel continuation helper exists")
        assert_html_contains(
            self,
            r"function isTunnelContinuationZone\(actor\)[\s\S]*?c < 6[\s\S]*?c >= COLS - 6",
            "tunnel continuation applies only inside side tunnels, not at mouth intersections",
        )
        assert_html_contains(
            self,
            r"function tunnelContinuationDirection\(actor\)[\s\S]*?if \(!isTunnelContinuationZone\(actor\)\) return null;",
            "tunnel continuation only applies in tunnel side lanes after entry",
        )
        assert_html_contains(
            self,
            r"actor\.dir && actor\.dir\.dy === 0 && canMove\(actor, actor\.dir, \"ghost\"\)",
            "ghost keeps existing horizontal tunnel direction when valid",
        )
        assert_html_contains(
            self,
            r"actor\.x < 0[\s\S]*?return DIRS\.right;[\s\S]*?actor\.x >= COLS \* TILE[\s\S]*?return DIRS\.left;",
            "offscreen tunnel ghosts are pushed back toward the maze if direction was lost",
        )

        tunnel_body = find_function_body("tunnelMovementDirection")
        self.assertRegex(
            tunnel_body,
            re.compile(r"return tunnelContinuationDirection\(actor\);"),
            "Ghost tunnel movement should continue horizontally inside the side tunnel",
        )

    def test_tunnel_mouth_intersections_use_ghost_target_selection(self):
        continuation_body = find_function_body("tunnelContinuationDirection")
        self.assertNotRegex(
            continuation_body,
            re.compile(r"c === 6|c === COLS - 7"),
            "Tunnel mouth intersections should not force ghosts into the tunnel before target selection",
        )
        assert_html_contains(
            self,
            r"function isTunnelContinuationZone\(actor\)[\s\S]*?c < 6[\s\S]*?c >= COLS - 6",
            "tunnel continuation applies only after ghosts are inside the side tunnel",
        )

    def test_ghost_direction_uses_one_tunnel_aware_entry_point(self):
        assert_html_contains(
            self,
            r"function chooseGhostMovementDirection\(g\)",
            "ghost movement should have one tunnel-aware direction chooser",
        )

        chooser_body = find_function_body("chooseGhostMovementDirection")
        self.assertRegex(
            chooser_body,
            re.compile(r"const tunnelDir = tunnelMovementDirection\(g\);[\s\S]*?if \(tunnelDir\) return tunnelDir;[\s\S]*?return chooseGhostTargetDirection\(g\);"),
            "tunnel movement should stay behind one chooser before normal target direction",
        )

        decision_body = find_function_body("handleDecisionPoint")
        self.assertRegex(
            decision_body,
            re.compile(r'actor\.dir = chooseGhostMovementDirection\(actor\);'),
            "ghost decision points should use the shared tunnel-aware chooser",
        )


    def test_low_frame_delta_does_not_snap_tunnel_ghost_back_to_center(self):
        assert_html_contains(
            self,
            r"function shouldHandleCenterDecision\(actor\)",
            "movement has a center-decision guard for tiny frame steps",
        )
        assert_html_contains(
            self,
            r"actor\.dir\.dx > 0 && actor\.x > centerX[\s\S]*?return false",
            "right-moving actors that already left center are not snapped back",
        )
        assert_html_contains(
            self,
            r"actor\.dir\.dx < 0 && actor\.x < centerX[\s\S]*?return false",
            "left-moving actors that already left center are not snapped back",
        )

        move_body = find_function_body("moveActor")
        self.assertRegex(
            move_body,
            re.compile(r"if \(shouldHandleCenterDecision\(actor\)\)"),
            "Movement should use the direction-aware center guard instead of raw center tolerance",
        )


    def test_ghosts_do_not_enter_hidden_tunnel_dead_ends(self):
        assert_html_contains(
            self,
            r"function tunnelDeadEndEscapeDirection\(actor\)[\s\S]*?c > 6[\s\S]*?c <= 9[\s\S]*?DIRS\.left[\s\S]*?c >= COLS - 10[\s\S]*?c < COLS - 7[\s\S]*?DIRS\.right",
            "ghosts already in hidden tunnel mouth dead ends are pushed back to the real mouth",
        )
        assert_html_contains(
            self,
            r"function isTunnelMouthDeadEndDirection\(actor, dir\)[\s\S]*?c === 6[\s\S]*?dir\.name === \"right\"[\s\S]*?c === COLS - 7[\s\S]*?dir\.name === \"left\"",
            "ghosts must not choose the hidden dead-end direction from tunnel mouths",
        )

        tunnel_body = find_function_body("tunnelMovementDirection")
        self.assertRegex(
            tunnel_body,
            re.compile(r"const deadEndDir = tunnelDeadEndEscapeDirection\(actor\);[\s\S]*?if \(deadEndDir\) return deadEndDir;"),
            "Ghosts in hidden tunnel dead ends should be corrected before target selection",
        )

        available_body = find_function_body("availableDirections")
        self.assertRegex(
            available_body,
            re.compile(r"DIR_ORDER\.filter\(dir => canMove\(g, dir, \"ghost\"\) && !isTunnelMouthDeadEndDirection\(g, dir\)\)"),
            "Ghost direction choices should exclude hidden tunnel dead ends",
        )


    def test_old_like_red_cruise_elroy_adds_staged_speed_only_to_normal_red(self):
        assert_html_contains(self, r"OLD_LIKE_ELROY_STAGES\s*=\s*\[", "Old-like Cruise Elroy stage table")
        for remaining_pellets, speed_multiplier in [(20, 1.06), (10, 1.12)]:
            assert_html_contains(
                self,
                rf"pelletsRemaining:\s*{remaining_pellets},\s*speedMultiplier:\s*{speed_multiplier}",
                f"Old-like Elroy stage at {remaining_pellets} pellets",
            )

        assert_html_contains(self, r"function oldLikeElroyStage\(ghost\)", "Elroy stage helper")
        elroy_body = find_function_body("oldLikeElroyStage")
        self.assertRegex(
            elroy_body,
            re.compile(r'activeGameplayMode\.id !== "old-like"[\s\S]*?return null'),
            "Elroy should not affect Maze Muncher mode",
        )
        self.assertRegex(
            elroy_body,
            re.compile(r'ghost\.name !== "red"[\s\S]*?return null'),
            "Elroy should only affect red ghost",
        )
        self.assertRegex(
            elroy_body,
            re.compile(r'ghost\.state !== "normal"[\s\S]*?return null'),
            "Elroy should only affect normal chase-capable red",
        )
        self.assertRegex(
            elroy_body,
            re.compile(r"frightenedTimer > 0[\s\S]*?return null"),
            "Elroy should not apply while red is frightened",
        )

        actor_body = find_function_body("actorSpeed")
        self.assertRegex(
            actor_body,
            re.compile(r"oldLikeElroyStage\(actor\)[\s\S]*?speed \*= elroy\.speedMultiplier"),
            "Red speed should gain staged Elroy pressure",
        )

    def test_old_like_red_cruise_elroy_targets_player_during_scatter(self):
        target_body = find_object_method_body("ghostPersonality", "targetTile")
        self.assertRegex(
            target_body,
            re.compile(r"oldLikeElroyStage\(g\)[\s\S]*?return \{ x: p\.x, y: p\.y \}"),
            "Elroy red should target the player instead of scatter corner",
        )
        self.assertRegex(
            target_body,
            re.compile(r"modeCycleFor\(activeGameplayMode,\s*level\)\[modeIndex\]\.mode"),
            "Scatter targeting should use the active mode cycle",
        )
        self.assertRegex(
            target_body,
            re.compile(r'currentMode === "scatter"[\s\S]*?oldLikeElroyStage\(g\)[\s\S]*?return g\.scatter'),
            "Non-Elroy ghosts and inactive Elroy red should keep scatter target",
        )

    def test_ghost_personality_module_is_the_targeting_and_direction_seam(self):
        assert_html_contains(self, r"const ghostPersonality\s*=\s*\{", "ghost personality module object exists")
        assert_html_contains(self, r"targetTile\(g\)\s*\{", "ghost personality module exposes target selection")
        assert_html_contains(self, r"chooseDirection\(g\)\s*\{", "ghost personality module exposes direction choice")

        target_body = find_function_body("targetForGhost")
        self.assertRegex(
            target_body,
            re.compile(r"return ghostPersonality\.targetTile\(g\);"),
            "Public target helper should delegate to ghost personality module",
        )

        choose_body = find_function_body("chooseGhostDirection")
        self.assertRegex(
            choose_body,
            re.compile(r"return ghostPersonality\.chooseDirection\(g\);"),
            "Public chooser should delegate to ghost personality module",
        )

    def test_ghost_personality_targeting_uses_tile_coordinates(self):
        assert_html_contains(self, r"function actorTile\(actor\)", "shared actor tile-coordinate helper")

        target_body = find_object_method_body("ghostPersonality", "targetTile")
        self.assertRegex(
            target_body,
            re.compile(r'g\.state === "leaving"[\s\S]*?return \{ x: 13, y: 11 \}'),
            "Leaving ghosts should target the door tile, not a half-tile center",
        )
        self.assertRegex(
            target_body,
            re.compile(r'g\.state === "eaten"[\s\S]*?return \{ x: 13, y: 14 \}'),
            "Eaten ghosts should target the home tile, not a half-tile center",
        )
        self.assertNotRegex(
            target_body,
            re.compile(r'13\.5|14\.5|11\.5'),
            "Ghost target tiles should not mix half-tile centers into direction decisions",
        )
        self.assertRegex(
            target_body,
            re.compile(r'if \(g\.name === "red"\) return \{ x: p\.x, y: p\.y \};'),
            "Red should target Maze Muncher tile directly in chase",
        )
        self.assertRegex(
            target_body,
            re.compile(r'if \(g\.name === "pink"\)[\s\S]*?dirAheadTiles\(pDir, 4\)'),
            "Pink should target four tiles ahead of Maze Muncher",
        )
        self.assertRegex(
            target_body,
            re.compile(r'const redTile = actorTile\(red\);[\s\S]*?ahead\.x \* 2 - redTile\.x[\s\S]*?ahead\.y \* 2 - redTile\.y'),
            "Cyan should use red ghost tile for the two-ahead vector target",
        )
        self.assertRegex(
            target_body,
            re.compile(r'const ghostTile = actorTile\(g\);[\s\S]*?ghostTile\.x - p\.x[\s\S]*?ghostTile\.y - p\.y'),
            "Orange distance decision should use ghost tile coordinates",
        )

        choose_body = find_object_method_body("ghostPersonality", "chooseDirection")
        self.assertRegex(
            choose_body,
            re.compile(r"const nextX = Math\.floor\(g\.x / TILE\) \+ dir\.dx;[\s\S]*?const nextY = Math\.floor\(g\.y / TILE\) \+ dir\.dy;"),
            "Ghost path choice should compare next tile coordinates to target tile coordinates",
        )
        self.assertNotRegex(
            choose_body,
            re.compile(r"\+ 0\.5"),
            "Ghost path choice should not mix half-tile centers with target tiles",
        )


    def test_old_like_ghost_release_uses_pellet_thresholds_with_timer_fallback(self):
        assert_html_contains(self, r"OLD_LIKE_GHOST_RELEASE\s*=\s*\{", "Old-like ghost release spec")
        for ghost_name, pellet_threshold, fallback_seconds in [
            ("pink", 0, 1),
            ("cyan", 30, 7),
            ("orange", 60, 13),
        ]:
            assert_html_contains(
                self,
                rf'{ghost_name}:\s*\{{\s*pellets:\s*{pellet_threshold},\s*fallback:\s*{fallback_seconds}',
                f"Old-like {ghost_name} pellet threshold and timer fallback",
            )

        update_body = find_object_method_body("ghostState", "updateRelease")
        self.assertRegex(
            update_body,
            re.compile(r'activeGameplayMode\.id !== "old-like"[\s\S]*?releaseLeft -= dt'),
            "Maze Muncher should keep timer-based release behavior",
        )
        self.assertRegex(
            update_body,
            re.compile(r"pelletsEaten >= release\.pellets[\s\S]*?releaseTimer >= release\.fallback"),
            "Old-like home ghosts should leave by pellet progress or fallback timing",
        )

    def test_ghost_state_module_is_the_state_transition_seam(self):
        assert_html_contains(self, r"const ghostState\s*=\s*\{", "ghost state module object exists")
        for method_name in [
            "resetRoundState",
            "startLeaving",
            "updateRelease",
            "finishLeaving",
            "finishEatenReturn",
            "updateModeTimer",
        ]:
            assert_html_contains(
                self,
                rf"{method_name}\([^)]*\)\s*\{{",
                f"ghost state module exposes {method_name}",
            )

        reset_body = find_function_body("resetActors")
        self.assertRegex(
            reset_body,
            re.compile(r"ghostState\.resetRoundState\(\)"),
            "Actor reset should delegate round-state resets to ghost state module",
        )

        update_mode_body = find_function_body("updateMode")
        self.assertRegex(
            update_mode_body,
            re.compile(r"return ghostState\.updateModeTimer\(dt\);"),
            "Mode updates should delegate scatter/chase timing to ghost state module",
        )

        update_ghosts_body = find_function_body("updateGhosts")
        self.assertRegex(
            update_ghosts_body,
            re.compile(r"ghostState\.updateRelease\(g,\s*dt\)"),
            "Home ghost release should delegate to ghost state module",
        )
        self.assertRegex(
            update_ghosts_body,
            re.compile(r'ghostState\.finishLeaving\(g\)'),
            "Leaving-to-normal transition should delegate to ghost state module",
        )
        self.assertRegex(
            update_ghosts_body,
            re.compile(r"ghostState\.finishEatenReturn\(g\)"),
            "Eaten ghost return should delegate to ghost state module",
        )

    def test_old_like_ghost_release_thresholds_survive_player_death(self):
        make_ghost_body = find_function_body("makeGhost")
        self.assertRegex(
            make_ghost_body,
            re.compile(r'name === "red" \? "normal" : "home"'),
            "Red should start outside while other ghosts start in the house",
        )

        start_level_body = find_object_method_body("gameLifecycle", "startLevel")
        self.assertRegex(
            start_level_body,
            re.compile(r"pelletsEaten = 0"),
            "New boards should reset pellet progress",
        )

        update_body = find_function_body("update")
        death_branch = re.search(r'if\s*\(state === "death"\)\s*\{(?P<body>[\s\S]*?)\n      \}', update_body)
        self.assertIsNotNone(death_branch, "Missing death-state reset branch")
        self.assertRegex(death_branch.group("body"), re.compile(r"gameLifecycle\.updateStateTimer\(dt\)"), "Death should delegate to lifecycle timer updates")
        death_update_body = find_object_method_body("gameLifecycle", "updateStateTimer")
        lifecycle_death_branch = re.search(r'if\s*\(state === "death"\)\s*\{(?P<body>[\s\S]*?)\n        \}', death_update_body)
        self.assertIsNotNone(lifecycle_death_branch, "Missing lifecycle death-update branch")
        self.assertRegex(lifecycle_death_branch.group("body"), re.compile(r"resetActors\(\)"), "Death should reset actors")
        self.assertNotRegex(
            lifecycle_death_branch.group("body"),
            re.compile(r"pelletsEaten = 0|startLevel\(\)"),
            "Death reset should preserve current board pellet progress for Old-like release thresholds",
        )

    def test_old_like_awards_one_extra_life_when_score_first_crosses_10000(self):
        assert_html_contains(self, r"let extraLifeAwarded\s*=\s*false", "extra-life award state")
        assert_html_contains(self, r"function awardScore\(points\)", "shared score award path")

        award_body = find_object_method_body("gameLifecycle", "awardScore")
        self.assertRegex(award_body, re.compile(r"const previousScore = score"), "Extra-life check should compare previous score")
        self.assertRegex(award_body, re.compile(r"score \+= points"), "Shared score path should add points")
        self.assertRegex(award_body, re.compile(r'this\.setHighScore\(\)'), "Shared score path should update high score")
        self.assertRegex(
            award_body,
            re.compile(r'activeGameplayMode\.id === "old-like"[\s\S]*?previousScore < 10000[\s\S]*?score >= 10000'),
            "Old-like extra life should trigger only when crossing 10000",
        )
        self.assertRegex(award_body, re.compile(r"!extraLifeAwarded"), "Extra life should be one-time")
        self.assertRegex(award_body, re.compile(r"lives\+\+"), "Crossing 10000 should add one life")
        self.assertRegex(award_body, re.compile(r"extraLifeAwarded = true"), "Extra-life award should latch")

        new_game_body = find_object_method_body("gameLifecycle", "startNewGame")
        self.assertRegex(new_game_body, re.compile(r"extraLifeAwarded = false"), "New game should reset extra-life award")

    def test_game_lifecycle_module_is_the_lifecycle_and_scoring_seam(self):
        assert_html_contains(self, r"const gameLifecycle\s*=\s*\{", "game lifecycle module object exists")
        for method_name in [
            "startLevel",
            "startNewGame",
            "setHighScore",
            "awardScore",
            "startDeathReset",
            "startLevelClear",
            "loseLife",
            "updateStateTimer",
        ]:
            assert_html_contains(
                self,
                rf"{method_name}\([^)]*\)\s*\{{",
                f"game lifecycle module exposes {method_name}",
            )

        start_level_body = find_function_body("startLevel")
        self.assertRegex(
            start_level_body,
            re.compile(r"return gameLifecycle\.startLevel\(\);"),
            "Start level wrapper should delegate to lifecycle module",
        )

        new_game_body = find_function_body("newGame")
        self.assertRegex(
            new_game_body,
            re.compile(r"return gameLifecycle\.startNewGame\(\);"),
            "New game wrapper should delegate to lifecycle module",
        )

        set_high_score_body = find_function_body("setHighScore")
        self.assertRegex(
            set_high_score_body,
            re.compile(r"return gameLifecycle\.setHighScore\(\);"),
            "High-score wrapper should delegate to lifecycle module",
        )

        award_score_body = find_function_body("awardScore")
        self.assertRegex(
            award_score_body,
            re.compile(r"return gameLifecycle\.awardScore\(points\);"),
            "Score wrapper should delegate to lifecycle module",
        )

        lose_life_body = find_function_body("loseLife")
        self.assertRegex(
            lose_life_body,
            re.compile(r"return gameLifecycle\.loseLife\(\);"),
            "Life-loss wrapper should delegate to lifecycle module",
        )

        eat_body = find_function_body("eatAtPlayerTile")
        self.assertRegex(
            eat_body,
            re.compile(r"gameLifecycle\.startLevelClear\(\)"),
            "Level clear should delegate to lifecycle module",
        )

        update_body = find_function_body("update")
        death_branch = re.search(r'if\s*\(state === "death"\)\s*\{(?P<body>[\s\S]*?)\n      \}', update_body)
        self.assertIsNotNone(death_branch, "Missing death-state branch")
        self.assertRegex(
            death_branch.group("body"),
            re.compile(r"gameLifecycle\.updateStateTimer\(dt\)"),
            "Death-state updates should delegate to lifecycle module",
        )

        level_clear_branch = re.search(r'if\s*\(state === "levelclear"\)\s*\{(?P<body>[\s\S]*?)\n      \}', update_body)
        self.assertIsNotNone(level_clear_branch, "Missing level-clear branch")
        self.assertRegex(
            level_clear_branch.group("body"),
            re.compile(r"gameLifecycle\.updateStateTimer\(dt\)"),
            "Level-clear updates should delegate to lifecycle module",
        )

    def test_power_pellets_score_and_reverse_even_when_frightened_time_is_zero(self):
        eat_body = find_function_body("eatAtPlayerTile")
        power_branch = re.search(r'if\s*\(cell === "o"\)\s*\{(?P<body>[\s\S]*?)\n        \}', eat_body)
        self.assertIsNotNone(power_branch, "Missing power-pellet branch")

        self.assertRegex(eat_body, re.compile(r'awardScore\(cell === "\."\s*\?\s*10\s*:\s*50\)'), "Power pellet should always award 50 points")
        self.assertRegex(
            power_branch.group("body"),
            re.compile(r'frightenedTimer\s*=\s*frightenedTimeFor\(activeGameplayMode,\s*level\)'),
            "Power pellet should use mode-aware frightened time, including zero",
        )
        self.assertRegex(power_branch.group("body"), re.compile(r"reverseNormalGhosts\(\)"), "Power pellet should always reverse normal ghosts")

    def test_ghosts_are_edible_and_combo_scored_only_while_frightened_timer_is_active(self):
        collision_body = find_function_body("checkCollisions")
        edible_branch = re.search(
            r'if\s*\(g\.state === "normal" && frightenedTimer > 0\)\s*\{(?P<body>[\s\S]*?)\n        \}',
            collision_body,
        )
        self.assertIsNotNone(edible_branch, "Missing edible ghost collision branch")
        self.assertRegex(edible_branch.group("body"), re.compile(r"awardScore\(ghostEatValue\)"), "Ghost combo score should be inside edible state")
        self.assertRegex(edible_branch.group("body"), re.compile(r"playGhostEatenSound\(ghostEatValue\)"), "Ghost combo sound should receive the current combo value")
        self.assertRegex(edible_branch.group("body"), re.compile(r"ghostEatValue = Math\.min\(1600,\s*ghostEatValue \* 2\)"), "Ghost combo should advance only inside edible state")

        normal_hit = re.search(
            r'if\s*\(g\.state === "normal"\)\s*\{(?P<body>[\s\S]*?)\n        \}',
            collision_body,
        )
        self.assertIsNotNone(normal_hit, "Missing normal ghost collision branch")
        self.assertRegex(normal_hit.group("body"), re.compile(r"loseLife\(\)"), "Zero frightened time should leave normal ghosts dangerous")


if __name__ == "__main__":
    unittest.main()
