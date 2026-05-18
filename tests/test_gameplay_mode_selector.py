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
        assert_html_contains(self, r'GAMEPLAY_MODE_STORAGE_KEY\s*=\s*"mazeMuncherGameplayMode"', "mode storage key")
        assert_html_contains(self, r'localStorage\.getItem\(GAMEPLAY_MODE_STORAGE_KEY\)', "saved mode restored")
        assert_html_contains(self, r'localStorage\.setItem\(GAMEPLAY_MODE_STORAGE_KEY,\s*activeGameplayMode\.id\)', "selected mode saved")
        assert_html_contains(self, r'function setGameplayMode', "mode setter exists")
        assert_html_contains(self, r'function toggleGameplayMode', "mode toggle exists")
        assert_html_contains(self, r'modeLabel\.textContent\s*=\s*activeGameplayMode\.label', "button label updates")


if __name__ == "__main__":
    unittest.main()
