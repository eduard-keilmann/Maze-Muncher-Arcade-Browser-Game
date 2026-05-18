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


if __name__ == "__main__":
    unittest.main()
