import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "Pacman_maze_muncher_browser_arcade.html"
HTML = HTML_PATH.read_text(encoding="utf-8")


def assert_html_contains(test_case, pattern, description):
    test_case.assertRegex(
        HTML,
        re.compile(pattern),
        f"Missing expected mobile controls behavior: {description}",
    )


class MobileControlsTests(unittest.TestCase):
    def test_page_exposes_accessible_directional_pad(self):
        assert_html_contains(self, r'class="touch-controls"', "touch controls area")
        assert_html_contains(self, r'aria-label="Touch controls"', "accessible touch controls label")

        for direction in ("up", "left", "down", "right"):
            assert_html_contains(self, rf'data-direction="{direction}"', f"{direction} D-pad button")
            assert_html_contains(self, rf'aria-label="Move {direction}"', f"{direction} D-pad accessible label")

    def test_direction_buttons_repeat_held_direction_until_released(self):
        assert_html_contains(self, r'querySelector\("\.touch-controls"\)', "touch controls script lookup")
        assert_html_contains(self, r'closest\("\[data-direction\]"\)', "direction button event delegation")
        assert_html_contains(self, r'DIRS\[directionName\]', "direction-name to game direction mapping")
        assert_html_contains(self, r'setInterval\(', "press-and-hold direction repeat")
        assert_html_contains(self, r'clearInterval\(', "press-and-hold cleanup")

        for event_name in ("pointerup", "pointercancel", "pointerleave"):
            assert_html_contains(self, rf'"{event_name}"', f"{event_name} hold release handling")

    def test_touch_controls_include_pause_and_restart_actions(self):
        for action_name, label in (("pause", "Pause game"), ("restart", "Restart game")):
            assert_html_contains(self, rf'data-action="{action_name}"', f"{action_name} touch action")
            assert_html_contains(self, rf'aria-label="{label}"', f"{action_name} accessible label")

        assert_html_contains(self, r'closest\("\[data-action\]"\)', "action button event delegation")
        assert_html_contains(self, r'actionName === "pause"', "pause action branch")
        assert_html_contains(self, r'togglePause\(\)', "pause action calls existing pause behavior")
        assert_html_contains(self, r'actionName === "restart"', "restart action branch")
        assert_html_contains(self, r'newGame\(\)', "restart action calls existing restart behavior")


if __name__ == "__main__":
    unittest.main()
