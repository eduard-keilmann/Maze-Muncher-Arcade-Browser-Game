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

    def test_mobile_restart_requires_deliberate_long_press(self):
        assert_html_contains(self, r'data-action="restart"[^>]*data-long-press-ms="900"', "restart declares long-press duration")
        assert_html_contains(self, r'Hold restart', "restart button communicates long press")
        assert_html_contains(self, r'let restartPressTimer = null;', "restart long-press timer exists")
        assert_html_contains(self, r'function startRestartPress', "restart press start handler exists")
        assert_html_contains(self, r'function cancelRestartPress', "restart press cancel handler exists")
        assert_html_contains(self, r'setTimeout\(\(\) => \{[\s\S]*newGame\(\);[\s\S]*\},\s*restartLongPressMs\)', "restart only fires after timeout")
        assert_html_contains(self, r'clearTimeout\(restartPressTimer\)', "restart press can be cancelled")
        assert_html_contains(self, r'classList\.add\("is-arming"\)', "restart arming visual state starts")
        assert_html_contains(self, r'classList\.remove\("is-arming"\)', "restart arming visual state clears")

    def test_short_portrait_layout_compacts_without_tiny_touch_targets(self):
        assert_html_contains(
            self,
            r'@media\s*\(pointer:\s*coarse\)\s*and\s*\(max-height:\s*760px\)\s*and\s*\(orientation:\s*portrait\)',
            "short portrait mobile media query",
        )
        assert_html_contains(self, r'--touch-size:\s*58px', "short portrait keeps larger thumb-friendly D-pad buttons")
        assert_html_contains(self, r'--touch-action-height:\s*46px', "short portrait keeps larger usable action buttons")
        assert_html_contains(self, r'--touch-action-width:\s*120px', "short portrait keeps wider action buttons")
        assert_html_contains(self, r'--mobile-gap:\s*6px', "short portrait compacts vertical spacing")
        assert_html_contains(self, r'width:\s*min\(100%,\s*calc\(100svh\s*-\s*320px\)\)', "short portrait caps canvas height pressure")
        assert_html_contains(self, r'\.touch-controls\s*\{[^}]*order:\s*3;', "touch controls remain below canvas")

    def test_held_direction_button_exposes_persistent_active_state(self):
        for direction in ("up", "left", "down", "right"):
            assert_html_contains(
                self,
                rf'data-direction="{direction}"[^>]*aria-pressed="false"',
                f"{direction} D-pad starts unpressed",
            )

        assert_html_contains(self, r'\.touch-button\.is-held', "visible held-button CSS state")
        assert_html_contains(self, r'classList\.add\("is-held"\)', "held button gets active class")
        assert_html_contains(self, r'classList\.remove\("is-held"\)', "held button clears active class")
        assert_html_contains(self, r'setAttribute\("aria-pressed",\s*"true"\)', "held button exposes pressed accessibility state")
        assert_html_contains(self, r'setAttribute\("aria-pressed",\s*"false"\)', "released button clears pressed accessibility state")

    def test_landscape_mobile_layout_places_controls_beside_canvas(self):
        assert_html_contains(
            self,
            r'@media\s*\(pointer:\s*coarse\)\s*and\s*\(orientation:\s*landscape\)\s*and\s*\(max-height:\s*520px\)',
            "landscape mobile media query",
        )
        assert_html_contains(self, r'grid-template-areas:\s*"title title"\s*"game controls"', "landscape uses side-by-side shell areas")
        assert_html_contains(self, r'\.frame\s*\{[^}]*grid-area:\s*game;', "frame assigned to game area")
        assert_html_contains(self, r'\.touch-controls\s*\{[^}]*grid-area:\s*controls;', "touch controls assigned beside canvas")
        assert_html_contains(self, r'\.help\s*\{[^}]*display:\s*none;', "landscape hides help to reduce scroll pressure")
        assert_html_contains(self, r'--touch-size:\s*56px', "landscape keeps larger thumb-friendly controls")
        assert_html_contains(self, r'--touch-action-height:\s*44px', "landscape keeps larger action controls")
        assert_html_contains(self, r'--touch-action-width:\s*110px', "landscape keeps wider action controls")
        assert_html_contains(self, r'minmax\(214px,\s*250px\)', "landscape reserves enough width for larger controls")

    def test_mobile_controls_use_larger_default_touch_targets(self):
        assert_html_contains(self, r'--touch-size:\s*64px', "default mobile D-pad buttons are larger")
        assert_html_contains(self, r'--touch-action-height:\s*50px', "default mobile action buttons are taller")
        assert_html_contains(self, r'--touch-action-width:\s*124px', "default mobile action buttons are wider")
        assert_html_contains(self, r'--touch-font-size:\s*1\.62rem', "default mobile D-pad icons are larger")
        assert_html_contains(self, r'width:\s*min\(100%,\s*360px\)', "touch controls container fits larger controls")


if __name__ == "__main__":
    unittest.main()
