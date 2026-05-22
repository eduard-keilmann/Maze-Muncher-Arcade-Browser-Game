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


def assert_html_not_contains(test_case, pattern, description):
    test_case.assertNotRegex(
        HTML,
        re.compile(pattern),
        f"Unexpected mobile controls behavior present: {description}",
    )


class MobileControlsTests(unittest.TestCase):
    def test_page_background_does_not_repeat_under_tall_mobile_controls(self):
        assert_html_contains(self, r'html\s*\{[^}]*background:\s*#000;', "page overflow background stays black")
        assert_html_contains(self, r'body\s*\{[^}]*min-height:\s*100svh;', "body covers mobile viewport")
        assert_html_contains(self, r'background-repeat:\s*no-repeat;', "radial page gradient does not repeat")
        assert_html_contains(self, r'background-size:\s*100%\s*100svh;', "radial page gradient is limited to viewport height")

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
        assert_html_contains(self, r'--touch-square-size:\s*64px', "short portrait keeps saved square D-pad size")
        assert_html_contains(self, r'--touch-width:\s*96px', "short portrait makes left and right D-pad buttons a bit wider")
        assert_html_contains(self, r'--touch-vertical-width:\s*154px', "short portrait gives centered up and down buttons visible side overlap")
        assert_html_contains(self, r'--touch-height:\s*var\(--touch-square-size\)', "short portrait preserves saved square height")
        assert_html_contains(self, r'--touch-wing-offset:\s*5px', "short portrait nudges left and right outward")
        assert_html_contains(self, r'--touch-action-height:\s*50px', "short portrait keeps larger usable action buttons")
        assert_html_contains(self, r'--touch-action-width:\s*124px', "short portrait keeps wider action buttons")
        assert_html_contains(self, r'--mobile-gap:\s*6px', "short portrait compacts vertical spacing")
        assert_html_contains(self, r'width:\s*min\(100%,\s*calc\(100svh\s*-\s*350px\)\)', "short portrait caps canvas height pressure")
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
        assert_html_contains(self, r'--touch-square-size:\s*60px', "landscape keeps saved square D-pad size")
        assert_html_contains(self, r'--touch-width:\s*84px', "landscape makes left and right D-pad buttons a bit wider")
        assert_html_contains(self, r'--touch-vertical-width:\s*142px', "landscape gives centered up and down buttons visible side overlap")
        assert_html_contains(self, r'--touch-height:\s*var\(--touch-square-size\)', "landscape preserves saved square height")
        assert_html_contains(self, r'--touch-wing-offset:\s*5px', "landscape nudges left and right outward")
        assert_html_contains(self, r'--touch-action-height:\s*48px', "landscape keeps larger action controls")
        assert_html_contains(self, r'--touch-action-width:\s*116px', "landscape keeps wider action controls")
        assert_html_contains(self, r'minmax\(230px,\s*260px\)', "landscape reserves enough width for larger controls")

    def test_mobile_controls_use_wider_dpad_with_saved_square_layout(self):
        assert_html_contains(self, r'--touch-square-size:\s*72px', "default mobile keeps saved square D-pad size")
        assert_html_contains(self, r'--touch-width:\s*108px', "default mobile left and right D-pad buttons are a bit wider")
        assert_html_contains(self, r'--touch-vertical-width:\s*172px', "default mobile up and down D-pad buttons visibly pass side-button inner edges")
        assert_html_contains(self, r'--touch-height:\s*var\(--touch-square-size\)', "default mobile D-pad height keeps saved square size")
        assert_html_contains(self, r'--touch-wing-offset:\s*6px', "default mobile nudges left and right outward")
        assert_html_contains(self, r'grid-template-columns:\s*repeat\(3,\s*var\(--touch-width\)\)', "D-pad grid uses widened columns")
        assert_html_contains(self, r'grid-template-rows:\s*repeat\(3,\s*var\(--touch-height\)\)', "D-pad grid keeps centered row height")
        assert_html_contains(self, r'width:\s*var\(--touch-width\);[\s\S]*?height:\s*var\(--touch-height\);', "side D-pad buttons keep rectangular dimensions")
        assert_html_contains(self, r'\.dpad-up,\s*\.dpad-down\s*\{[^}]*width:\s*var\(--touch-vertical-width\);', "up and down D-pad buttons use centered vertical width")
        assert_html_contains(self, r'\.dpad-up,\s*\.dpad-down\s*\{[^}]*justify-self:\s*center;', "wider up and down buttons stay symmetric around the center column")
        assert_html_contains(self, r'Saved square D-pad layout:[^\n]*--touch-width and --touch-vertical-width to var\(--touch-square-size\)[^\n]*--touch-wing-offset:\s*0px', "old square D-pad layout is documented for easy rollback")
        assert_html_contains(self, r'\.dpad-left\s*\{[^}]*--touch-button-offset:\s*calc\(-1 \* var\(--touch-wing-offset\)\);', "left D-pad button shifts slightly outward")
        assert_html_contains(self, r'\.dpad-right\s*\{[^}]*--touch-button-offset:\s*var\(--touch-wing-offset\);', "right D-pad button shifts slightly outward")
        assert_html_contains(self, r'--touch-action-height:\s*54px', "default mobile action buttons are taller")
        assert_html_contains(self, r'--touch-action-width:\s*132px', "default mobile action buttons are wider")
        assert_html_contains(self, r'--touch-font-size:\s*1\.8rem', "default mobile D-pad icons are larger")
        assert_html_contains(self, r'width:\s*min\(100%,\s*360px\)', "touch controls container fits larger controls")

    def test_mobile_help_text_sits_below_dpad_with_original_kbd_style(self):
        assert_html_contains(
            self,
            r'<div class="dpad"[\s\S]*?</div>\s*<p class="help touch-help">\s*Move with <kbd>Arrow Keys</kbd>, <kbd>WASD</kbd>, continuous swipe, or the touch D-pad\. Press <kbd>Space</kbd> to pause/resume, <kbd>Enter</kbd> to start/restart\.\s*</p>\s*<div class="touch-actions">',
            "mobile help text appears directly below the D-pad with the original sentence and kbd style",
        )
        assert_html_contains(self, r'class="help desktop-help"', "desktop keyboard help remains available")
        assert_html_contains(self, r'\.touch-help\s*\{[^}]*display:\s*none;', "mobile help starts hidden on desktop")
        assert_html_contains(self, r'\.touch-help\s*\{[^}]*display:\s*block;', "mobile help appears with touch controls")
        assert_html_contains(self, r'\.desktop-help\s*\{[^}]*display:\s*none;', "desktop help hides on mobile")
        assert_html_contains(self, r'kbd\s*\{[^}]*color:\s*#fff;', "kbd chips keep old white text")
        assert_html_contains(self, r'background:\s*#1b1b36;', "kbd chips keep old dark blue fill")
        assert_html_contains(self, r'border:\s*1px solid #3b3b82;', "kbd chips keep old blue frame")
        assert_html_contains(self, r'border-bottom-width:\s*2px;', "kbd chips keep old bottom border depth")
        assert_html_not_contains(self, r'kbd\s*\{[^}]*box-shadow:', "kbd chips should not use added glow")

    def test_touch_button_visual_feedback_is_stronger(self):
        assert_html_contains(self, r'filter:\s*brightness\(1\.1\);', "pressed controls get 10% brighter")
        assert_html_contains(self, r'transform:\s*translateX\(var\(--touch-button-offset,\s*0px\)\) translateY\(2\.2px\);', "pressed controls move 10% farther while preserving side offsets")
        assert_html_contains(self, r'0 3\.3px 11px rgba\(0,\s*0,\s*0,\s*0\.35\)', "tap shadow is 10% stronger")
        assert_html_contains(self, r'0 0 20px rgba\(255,\s*232,\s*90,\s*0\.42\)', "held direction glow is stronger")
        assert_html_contains(self, r'0 0 20px rgba\(255,\s*92,\s*117,\s*0\.42\)', "restart arming glow is stronger")

    def test_touch_buttons_trigger_haptic_feedback_on_normal_tap(self):
        assert_html_contains(self, r'function triggerTouchFeedback\(pattern = 12\)', "haptic feedback helper exists")
        assert_html_contains(self, r'typeof navigator\.vibrate !== "function"', "haptic helper safely checks browser support")
        assert_html_contains(self, r'navigator\.vibrate\(pattern\)', "haptic helper uses browser vibration")
        assert_html_contains(
            self,
            r'if \(actionButton\) \{[\s\S]*?event\.preventDefault\(\);[\s\S]*?triggerTouchFeedback\(\);',
            "action buttons vibrate on normal tap",
        )
        assert_html_contains(
            self,
            r'const directionButton = event\.target\.closest\("\[data-direction\]"\);[\s\S]*?event\.preventDefault\(\);[\s\S]*?triggerTouchFeedback\(\);',
            "direction buttons vibrate on normal tap",
        )
        assert_html_contains(self, r'triggerTouchFeedback\(\[18,\s*40,\s*18\]\);', "completed restart long press gets confirm feedback")

    def test_whole_page_swipes_control_player_on_mobile(self):
        assert_html_contains(
            self,
            r'@media\s*\(pointer:\s*coarse\),\s*\(max-width:\s*700px\)\s*\{[\s\S]*?body\s*\{[^}]*touch-action:\s*none;[^}]*overscroll-behavior:\s*none;',
            "mobile page panning is disabled so swipes steer reliably",
        )
        assert_html_contains(self, r'function shouldHandlePageSwipe\(event\)', "page swipe target helper exists")
        assert_html_contains(
            self,
            r'target\.closest\("button, a, input, textarea, select"\)',
            "page swipe ignores interactive controls",
        )
        assert_html_contains(
            self,
            r'return event\.pointerType !== "mouse" \|\| target === canvas;',
            "desktop mouse swipes stay limited to the canvas",
        )
        assert_html_contains(self, r'document\.addEventListener\("pointerdown"', "whole-page swipe starts on document")
        assert_html_contains(self, r'document\.addEventListener\("pointerup"', "whole-page swipe ends on document")
        assert_html_contains(self, r'document\.addEventListener\("pointercancel"', "cancelled page swipes clear state")
        assert_html_contains(
            self,
            r'if \(state === "title" \|\| state === "gameover"\) newGame\(\);[\s\S]*?setDirection',
            "valid page swipe starts game before steering",
        )
        assert_html_not_contains(self, r'canvas\.addEventListener\("pointerdown"', "swipe should not be canvas-only")
        assert_html_not_contains(self, r'canvas\.addEventListener\("pointerup"', "swipe should not be canvas-only")

    def test_continuous_page_swipes_steer_before_finger_release(self):
        assert_html_contains(self, r'const swipeThreshold = 12;', "continuous swipe threshold is low latency")
        assert_html_contains(self, r'document\.addEventListener\("pointermove"', "page swipes steer while finger moves")
        assert_html_contains(
            self,
            r'function applyPageSwipeDirection\(direction\)[\s\S]*?newGame\(\);[\s\S]*?setDirection\(direction\);',
            "page swipe starts game before steering",
        )
        assert_html_contains(
            self,
            r'function handlePageSwipeMove\(event\)[\s\S]*?Math\.hypot\(dx,\s*dy\) < swipeThreshold[\s\S]*?return;',
            "small finger drift is ignored",
        )
        assert_html_contains(
            self,
            r'handlePageSwipeMove\(event\)[\s\S]*?applyPageSwipeDirection\([\s\S]*?\);[\s\S]*?touchStart\.x = event\.clientX;[\s\S]*?touchStart\.y = event\.clientY;',
            "accepted swipe resets anchor for continuous steering",
        )

    def test_canvas_tap_steers_relative_to_player_without_breaking_swipe(self):
        assert_html_contains(self, r'function directionFromCanvasTap\(event\)', "canvas tap helper exists")
        assert_html_contains(
            self,
            r'const rect = canvas\.getBoundingClientRect\(\);[\s\S]*?const tapX = \(event\.clientX - rect\.left\) \* \(canvas\.width / rect\.width\);[\s\S]*?const tapY = \(event\.clientY - rect\.top\) \* \(canvas\.height / rect\.height\);',
            "tap converts page coordinates into canvas coordinates",
        )
        assert_html_contains(
            self,
            r'const dx = tapX - player\.x;[\s\S]*?const dy = tapY - \(HUD \+ player\.y\);',
            "tap direction is relative to Maze Muncher position",
        )
        assert_html_contains(
            self,
            r'if \(Math\.abs\(dx\) > Math\.abs\(dy\)\) return dx < 0 \? DIRS\.left : DIRS\.right;[\s\S]*?return dy < 0 \? DIRS\.up : DIRS\.down;',
            "larger tap delta chooses horizontal or vertical direction",
        )
        assert_html_contains(self, r'moved:\s*false,', "pointer starts as possible tap")
        assert_html_contains(self, r'touchStart\.moved = true;', "movement past threshold stops tap handling")
        assert_html_contains(
            self,
            r'if \(touchStart\.target === canvas && !touchStart\.moved\) \{[\s\S]*?applyPageSwipeDirection\(directionFromCanvasTap\(event\)\);[\s\S]*?touchStart = null;',
            "short canvas tap applies relative direction on release",
        )
        assert_html_contains(
            self,
            r'function applyPageSwipeDirection\(direction\)[\s\S]*?newGame\(\);[\s\S]*?setDirection\(direction\);',
            "tap uses same title/gameover start-before-steer path",
        )



if __name__ == "__main__":
    unittest.main()
