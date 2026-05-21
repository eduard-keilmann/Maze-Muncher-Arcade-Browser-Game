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

    def test_sound_toggle_gives_audible_preview_when_turning_sound_on(self):
        assert_html_contains(self, r"const MASTER_VOLUME = 0\.0336;", "sound effects use the previous quiet threat-music volume")
        assert_html_contains(self, r"function previewSound\(\)", "sound preview helper exists")
        assert_html_contains(
            self,
            r"function toggleSound\(\)[\s\S]*?soundEnabled = !soundEnabled;[\s\S]*?saveSoundPreference\(\);[\s\S]*?renderSoundMode\(\);",
            "sound button remains a real on/off toggle",
        )
        assert_html_contains(
            self,
            r"if \(soundEnabled\) \{[\s\S]*?unlockAudio\(\);[\s\S]*?previewSound\(\);[\s\S]*?\}",
            "turning sound on plays immediate preview",
        )


    def test_page_exposes_persistent_music_toggle(self):
        assert_html_contains(self, r"data-action=\"music\"", "music action button")
        assert_html_contains(self, r"aria-label=\"Music\"", "accessible music control")
        assert_html_contains(self, r"MUSIC_STORAGE_KEY\s*=\s*\"mazeMuncherMusicEnabled\"", "music preference storage key")
        assert_html_contains(self, r"localStorage\.getItem\(MUSIC_STORAGE_KEY\)", "music preference restored")
        assert_html_contains(self, r"localStorage\.setItem\(MUSIC_STORAGE_KEY,\s*String\(musicEnabled\)\)", "music preference saved")
        assert_html_contains(self, r"musicLabel\.textContent\s*=\s*musicEnabled \? \"MUSIC: ON\" : \"MUSIC: OFF\"", "music label updates")

    def test_music_uses_generated_web_audio_and_separate_quiet_volume(self):
        assert_html_contains(self, r"const MUSIC_VOLUME = 0\.078;", "threat music matches the previous normal pellet tick volume")
        assert_html_contains(self, r"function playMusicPulse\(", "generated music pulse helper exists")
        assert_html_contains(self, r"function previewMusic\(\)", "music preview helper exists")
        assert_html_contains(self, r"playMusicTone\([^\n]+MUSIC_VOLUME", "music uses generated soft tones")
        assert_html_contains(self, r"function startMusicLoop\(\)", "music loop start helper exists")
        assert_html_contains(self, r"function stopMusicLoop\(\)", "music loop stop helper exists")
        self.assertNotRegex(HTML, re.compile(r"\.(mp3|wav|ogg|m4a)"), "Music must not add audio assets")

    def test_music_tones_use_soft_attack_to_avoid_click_distortion(self):
        assert_html_contains(self, r"function playMusicTone\(", "music has separate soft-tone helper")
        assert_html_contains(self, r"oscillator\.type = \"triangle\"", "music avoids harsh square-wave attacks")
        assert_html_contains(self, r"const attack = 0\.028;", "music attack is long enough to avoid clicks")
        assert_html_contains(self, r"const release = 0\.035;", "music release is smoothed")
        assert_html_contains(self, r"linearRampToValueAtTime\(volume, startAt \+ attack\)", "music fades in smoothly")
        assert_html_contains(self, r"linearRampToValueAtTime\(0\.0001, endAt \+ release\)", "music fades out smoothly")

    def test_high_threat_music_pulse_rate_is_faster(self):
        assert_html_contains(self, r"function musicPulseInterval\(threat\)", "music pulse interval helper exists")
        assert_html_contains(
            self,
            r"return 0\.62 - threat \* 0\.38;",
            "high threat lowers pulse interval enough to raise beep rate",
        )

    def test_music_loop_is_state_gated_and_updated_from_game_loop(self):
        assert_html_contains(self, r"function shouldMusicPlay\(\)[\s\S]*?state === \"playing\"[\s\S]*?!paused", "music only plays during active gameplay")
        assert_html_contains(self, r"function update\(dt\)[\s\S]*?updateMusicLoop\(dt\);", "game loop updates music")
        assert_html_contains(self, r"function updateMusicLoop\(dt\)[\s\S]*?if \(!shouldMusicPlay\(\)\) \{[\s\S]*?stopMusicLoop\(\);[\s\S]*?return;[\s\S]*?\}", "music stops outside playing state")
        assert_html_contains(self, r"function toggleMusic\(\)[\s\S]*?if \(musicEnabled\) \{[\s\S]*?unlockAudio\(\);[\s\S]*?previewMusic\(\);[\s\S]*?startMusicLoop\(\);[\s\S]*?\} else \{[\s\S]*?stopMusicLoop\(\);", "music toggle previews, starts, and stops loop")

    def test_music_threat_formula_uses_gameplay_danger_inputs(self):
        assert_html_contains(self, r"function computeThreatLevel\(\)[\s\S]*?ghosts[\s\S]*?g\.state !== \"eaten\"[\s\S]*?g\.state !== \"home\"", "threat ignores inactive ghosts")
        assert_html_contains(self, r"function computeThreatLevel\(\)[\s\S]*?frightenedTimer > 0[\s\S]*?Math\.min\(1, frightenedTimer / 2\)", "frightened ending raises tension")
        assert_html_contains(self, r"function computeThreatLevel\(\)[\s\S]*?pelletsRemaining[\s\S]*?modeCycle\[modeIndex\]\.mode === \"chase\"", "pellets and chase mode affect threat")
        assert_html_contains(self, r"Math\.max\(0, Math\.min\(1, threat\)\)", "threat is clamped")


    def test_music_threat_formula_does_not_call_elroy_without_ghost(self):
        threat_body = re.search(r"function computeThreatLevel\(\) \{(?P<body>[\s\S]*?)\n    \}", HTML)
        self.assertIsNotNone(threat_body, "Missing computeThreatLevel body")
        self.assertNotRegex(
            threat_body.group("body"),
            re.compile(r"oldLikeElroyStage\(\)"),
            "Music threat must not call ghost-specific Elroy helper without a ghost",
        )
        assert_html_contains(self, r"dangerousGhosts\.some\(g => oldLikeElroyStage\(g\)\)", "Elroy pressure checks red ghost safely")

    def test_music_control_unlocks_audio_for_iphone(self):
        assert_html_contains(self, r"musicButton\.addEventListener\(\"click\"[\s\S]*?unlockAudio\(\);", "music button unlocks audio")

    def test_ios_touchend_and_click_prime_audio_output(self):
        assert_html_contains(self, r"let audioPrimed = false;", "audio prime state exists")
        assert_html_contains(self, r"function primeAudioOutput\(\)", "audio output prime helper exists")
        assert_html_contains(self, r"primeAudioOutput\(\);", "unlock path primes output")
        assert_html_contains(self, r"document\.addEventListener\(\"touchend\", unlockAudio", "iPhone touchend unlock path")
        assert_html_contains(self, r"document\.addEventListener\(\"click\", unlockAudio", "click unlock fallback path")

    def test_user_gestures_unlock_audio_before_play_actions(self):
        assert_html_contains(self, r"function setDirection\(dir\)[\s\S]*?unlockAudio\(\);[\s\S]*?newGame\(\);", "movement unlocks audio before auto-start")
        assert_html_contains(self, r"modeButton\.addEventListener\(\"click\"[\s\S]*?unlockAudio\(\);", "mode button unlocks audio")
        assert_html_contains(self, r"soundButton\.addEventListener\(\"click\"[\s\S]*?unlockAudio\(\);", "sound button unlocks audio")
        assert_html_contains(self, r"touchControls\.addEventListener\(\"pointerdown\"[\s\S]*?unlockAudio\(\);", "touch controls unlock audio")


if __name__ == "__main__":
    unittest.main()
