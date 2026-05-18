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
        assert_html_contains(self, r"playerSpeed:\s*\(level\)\s*=>\s*Math\.min\(112,\s*90 \+ level \* 2\.5\)", "current player speed formula")
        assert_html_contains(self, r"ghostSpeed:\s*\(level\)\s*=>\s*Math\.min\(108,\s*78 \+ level \* 2\.6\)", "current ghost speed formula")
        assert_html_contains(self, r"frightenedTime:\s*\(level\)\s*=>\s*Math\.max\(4\.2,\s*7\.5 - level \* 0\.25\)", "current frightened-time formula")
        assert_html_contains(self, r"fruitValue:\s*\(level,\s*mark\)\s*=>\s*Math\.min\(5000,\s*100 \+ level \* 100 \+ mark\)", "current fruit value formula")
        assert_html_contains(self, r"ghostReleaseBase:\s*\(level\)\s*=>\s*Math\.max\(0,\s*2\.5 - level \* 0\.15\)", "current ghost release formula")
        assert_html_contains(self, r"modeCycle:\s*\(\)\s*=>\s*MODE_CYCLE", "current scatter/chase cycle")

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

        choose_body = find_function_body("chooseGhostDirection")
        frightened_branch = re.search(
            r'if\s*\(frightenedTimer > 0 && g\.state === "normal"\)\s*\{(?P<body>[\s\S]*?)\n      \}',
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

    def test_old_like_awards_one_extra_life_when_score_first_crosses_10000(self):
        assert_html_contains(self, r"let extraLifeAwarded\s*=\s*false", "extra-life award state")
        assert_html_contains(self, r"function awardScore\(points\)", "shared score award path")

        award_body = find_function_body("awardScore")
        self.assertRegex(award_body, re.compile(r"const previousScore = score"), "Extra-life check should compare previous score")
        self.assertRegex(award_body, re.compile(r"score \+= points"), "Shared score path should add points")
        self.assertRegex(award_body, re.compile(r'setHighScore\(\)'), "Shared score path should update high score")
        self.assertRegex(
            award_body,
            re.compile(r'activeGameplayMode\.id === "old-like"[\s\S]*?previousScore < 10000[\s\S]*?score >= 10000'),
            "Old-like extra life should trigger only when crossing 10000",
        )
        self.assertRegex(award_body, re.compile(r"!extraLifeAwarded"), "Extra life should be one-time")
        self.assertRegex(award_body, re.compile(r"lives\+\+"), "Crossing 10000 should add one life")
        self.assertRegex(award_body, re.compile(r"extraLifeAwarded = true"), "Extra-life award should latch")

        new_game_body = find_function_body("newGame")
        self.assertRegex(new_game_body, re.compile(r"extraLifeAwarded = false"), "New game should reset extra-life award")

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
        self.assertRegex(edible_branch.group("body"), re.compile(r"ghostEatValue = Math\.min\(1600,\s*ghostEatValue \* 2\)"), "Ghost combo should advance only inside edible state")

        normal_hit = re.search(
            r'if\s*\(g\.state === "normal"\)\s*\{(?P<body>[\s\S]*?)\n        \}',
            collision_body,
        )
        self.assertIsNotNone(normal_hit, "Missing normal ghost collision branch")
        self.assertRegex(normal_hit.group("body"), re.compile(r"loseLife\(\)"), "Zero frightened time should leave normal ghosts dangerous")


if __name__ == "__main__":
    unittest.main()
