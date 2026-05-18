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
            "ghostReleaseBaseFor",
            "modeCycleFor",
        ]:
            assert_html_contains(self, rf"function {name}\(", f"{name} tuning function")

        for name in [
            "playerSpeedFor",
            "ghostSpeedFor",
            "frightenedTimeFor",
            "fruitValueFor",
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
        assert_html_contains(self, r"fruitValue:\s*5000", "Old-like high-value fruit tuning exists")
        assert_html_contains(self, r"tunnelGhostSpeedMultiplier:\s*0\.[0-9]+", "Old-like tunnel slowdown tuning exists")

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


if __name__ == "__main__":
    unittest.main()
