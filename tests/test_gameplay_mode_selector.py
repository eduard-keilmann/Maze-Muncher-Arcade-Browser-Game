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
        f"Missing expected gameplay mode behavior: {description}",
    )


def find_function_body(name):
    match = re.search(rf'function {name}\([^)]*\) \{{(?P<body>[\s\S]*?)\n    \}}', HTML)
    if not match:
        raise AssertionError(f"Missing function {name}")
    return match.group("body")


class GameplayModeSelectorTests(unittest.TestCase):
    def test_page_exposes_gameplay_mode_selector(self):
        assert_html_contains(self, r'class="mode-controls"', "mode controls area")
        assert_html_contains(self, r'aria-label="Gameplay mode"', "accessible gameplay mode label")
        assert_html_contains(self, r'data-action="mode"', "mode selector action button")
        assert_html_contains(self, r'MODE:\s*MAZE MUNCHER', "Maze Muncher mode label")
        assert_html_contains(self, r'MODE:\s*OLD-LIKE', "Old-like mode label")

    def test_selected_gameplay_mode_is_restored_saved_and_rendered(self):
        assert_html_contains(self, r'GAMEPLAY_MODES\s*=\s*\[', "gameplay mode list")
        assert_html_contains(self, r'"maze-muncher"', "Maze Muncher mode id")
        assert_html_contains(self, r'"old-like"', "Old-like mode id")
        assert_html_contains(self, r'DEFAULT_GAMEPLAY_MODE_ID\s*=\s*"old-like"', "Old-like default mode")
        assert_html_contains(self, r'GAMEPLAY_MODE_STORAGE_KEY\s*=\s*"mazeMuncherGameplayMode"', "mode storage key")
        assert_html_contains(self, r'localStorage\.getItem\(GAMEPLAY_MODE_STORAGE_KEY\)', "saved mode restored")
        assert_html_contains(self, r'localStorage\.setItem\(GAMEPLAY_MODE_STORAGE_KEY,\s*activeGameplayMode\.id\)', "selected mode saved")
        assert_html_contains(self, r'function setGameplayMode', "mode setter exists")
        assert_html_contains(self, r'function toggleGameplayMode', "mode toggle exists")
        assert_html_contains(self, r'modeLabel\.textContent\s*=\s*activeGameplayMode\.label', "button label updates")

        finder_body = find_function_body("findGameplayMode")
        self.assertRegex(
            finder_body,
            re.compile(r'DEFAULT_GAMEPLAY_MODE_ID'),
            "Unknown or absent stored mode should fall back to the explicit default",
        )

    def test_mode_switching_is_limited_to_title_and_game_over_without_starting(self):
        assert_html_contains(self, r'modeButton\.addEventListener\("click"', "mode button click listener")
        assert_html_contains(self, r'toggleGameplayMode\(\)', "mode button calls shared toggle")
        assert_html_contains(
            self,
            r'if\s*\(state !== "title" && state !== "gameover"\) return;',
            "active run mode switching is blocked",
        )

        toggle_body = find_function_body("toggleGameplayMode")
        setter_body = find_function_body("setGameplayMode")
        self.assertNotRegex(toggle_body, re.compile(r'newGame\(\)'), "Mode switch should not auto-start a game")
        self.assertRegex(toggle_body, re.compile(r'setGameplayMode\(nextMode\.id\)'), "Mode toggle should use the shared setter")
        self.assertRegex(setter_body, re.compile(r'highScore\s*=\s*readHighScore\(\)'), "Mode switch should refresh displayed high score")

    def test_high_scores_are_stored_per_gameplay_mode(self):
        assert_html_contains(self, r'highScoreKey:\s*"mazeMuncherHighScore"', "Maze Muncher high-score key")
        assert_html_contains(self, r'highScoreKey:\s*"mazeMuncherOldLikeHighScore"', "Old-like high-score key")
        assert_html_contains(self, r'localStorage\.getItem\(activeGameplayMode\.highScoreKey\)', "active mode high score read")
        assert_html_contains(self, r'localStorage\.setItem\(activeGameplayMode\.highScoreKey,\s*String\(highScore\)\)', "active mode high score write")

    def test_footer_shows_active_gameplay_mode(self):
        assert_html_contains(
            self,
            r'ctx\.fillText\(`\$\{activeGameplayMode\.footerLabel\}`,\s*W - 12,\s*HUD \+ ROWS \* TILE \+ 21\)',
            "footer draws active gameplay mode",
        )


if __name__ == "__main__":
    unittest.main()
