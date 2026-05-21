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
        f"Missing expected sound behavior: {description}",
    )


class SoundControlsTests(unittest.TestCase):
    def test_page_exposes_persistent_sound_toggle(self):
        assert_html_contains(self, r"data-action=\"sound\"", "sound action button")
        assert_html_contains(self, r"aria-label=\"Sound\"", "accessible sound control")
        assert_html_contains(self, r"SOUND_STORAGE_KEY\s*=\s*\"mazeMuncherSoundEnabled\"", "sound preference storage key")
        assert_html_contains(self, r"localStorage\.getItem\(SOUND_STORAGE_KEY\)", "sound preference restored")
        assert_html_contains(self, r"localStorage\.setItem\(SOUND_STORAGE_KEY,\s*String\(soundEnabled\)\)", "sound preference saved")
        assert_html_contains(self, r"soundLabel\.textContent\s*=\s*soundEnabled \? \"SOUND: ON\" : \"SOUND: OFF\"", "sound label updates")

    def test_sound_uses_generated_web_audio_without_assets(self):
        assert_html_contains(self, r"function createAudioContext\(\)", "audio context factory")
        assert_html_contains(self, r"window\.AudioContext \|\| window\.webkitAudioContext", "standard and Safari Web Audio support")
        assert_html_contains(self, r"createOscillator\(\)", "oscillator generated tones")
        assert_html_contains(self, r"createGain\(\)", "gain envelopes")
        assert_html_contains(self, r"type = \"square\"", "arcade square-wave tone")
        assert_html_contains(self, r"function unlockAudio\(\)", "audio unlock helper")
        assert_html_contains(self, r"audioContext\.resume\(\)", "mobile audio resumes after gesture")

    def test_gameplay_events_trigger_original_like_sound_effects(self):
        expected_calls = {
            "playStartSound()": "new game jingle",
            "playPelletSound(cell)": "pellet and power pellet tick",
            "playLevelClearSound()": "level clear flourish",
            "playFruitSound()": "fruit bonus sound",
            "playGhostEatenSound()": "ghost eaten sound",
            "playDeathSound()": "death sound",
        }
        for call, description in expected_calls.items():
            assert_html_contains(self, re.escape(call), description)

    def test_user_gestures_unlock_audio_before_play_actions(self):
        assert_html_contains(self, r"function setDirection\(dir\)[\s\S]*?unlockAudio\(\);[\s\S]*?newGame\(\);", "movement unlocks audio before auto-start")
        assert_html_contains(self, r"modeButton\.addEventListener\(\"click\"[\s\S]*?unlockAudio\(\);", "mode button unlocks audio")
        assert_html_contains(self, r"soundButton\.addEventListener\(\"click\"[\s\S]*?unlockAudio\(\);", "sound button unlocks audio")
        assert_html_contains(self, r"touchControls\.addEventListener\(\"pointerdown\"[\s\S]*?unlockAudio\(\);", "touch controls unlock audio")


if __name__ == "__main__":
    unittest.main()
