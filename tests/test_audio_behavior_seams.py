import json
import re
import subprocess
import textwrap
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = PROJECT_ROOT / "maze_muncher_browser_arcade.html"
HTML = HTML_PATH.read_text(encoding="utf-8")


def find_object_method_body(object_name, method_name):
    match = re.search(
        rf"const {object_name}\s*=\s*\{{[\s\S]*?{method_name}\([^)]*\)\s*\{{(?P<body>[\s\S]*?)\n      \}}",
        HTML,
    )
    if not match:
        raise AssertionError(f"Missing {object_name}.{method_name}")
    return match.group("body")


def find_const_number(name):
    match = re.search(rf"const {name}\s*=\s*(?P<value>[0-9.]+);", HTML)
    if not match:
        raise AssertionError(f"Missing numeric constant {name}")
    value_text = match.group("value")
    return float(value_text) if "." in value_text else int(value_text)


def run_audio_behavior(script_body):
    compute_threat_level = find_object_method_body("gameAudio", "computeThreatLevel")
    music_pulse_interval = find_object_method_body("gameAudio", "musicPulseInterval")
    tile = find_const_number("TILE")

    script = textwrap.dedent(
        f"""
        const TILE = {tile};

        const gameAudio = {{
          computeThreatLevel(facts) {{
        {compute_threat_level}
          }},
          musicPulseInterval(threat, facts) {{
        {music_pulse_interval}
          }}
        }};

        function oldLikeElroyStage(ghost) {{
          return ghost.elroyStage || null;
        }}

        const result = (() => {{
        {script_body}
        }})();

        console.log(JSON.stringify(result));
        """
    )

    completed = subprocess.run(
        ["node", "-e", script],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class AudioBehaviorSeamTests(unittest.TestCase):
    def test_threat_music_scores_nearby_chase_pressure_above_far_scatter_pressure(self):
        result = run_audio_behavior(
            """
            const nearbyChase = gameAudio.computeThreatLevel({
              player: { x: 8 * TILE, y: 8 * TILE },
              ghosts: [{ x: 9 * TILE, y: 8 * TILE, state: "normal" }],
              frightenedTimer: 0,
              pelletsRemaining: 52,
              ghostMode: "chase"
            });

            const farScatter = gameAudio.computeThreatLevel({
              player: { x: 8 * TILE, y: 8 * TILE },
              ghosts: [{ x: 18 * TILE, y: 18 * TILE, state: "normal" }],
              frightenedTimer: 0,
              pelletsRemaining: 52,
              ghostMode: "scatter"
            });

            return { nearbyChase, farScatter };
            """
        )

        self.assertGreater(result["nearbyChase"], result["farScatter"])
        self.assertLessEqual(result["nearbyChase"], 1)
        self.assertGreaterEqual(result["farScatter"], 0)

    def test_frightened_time_near_expiry_keeps_threat_music_tense(self):
        result = run_audio_behavior(
            """
            const earlyFrightened = gameAudio.computeThreatLevel({
              player: { x: 8 * TILE, y: 8 * TILE },
              ghosts: [{ x: 9 * TILE, y: 8 * TILE, state: "normal" }],
              frightenedTimer: 3.5,
              pelletsRemaining: 52,
              ghostMode: "scatter"
            });

            const endingFrightened = gameAudio.computeThreatLevel({
              player: { x: 8 * TILE, y: 8 * TILE },
              ghosts: [{ x: 9 * TILE, y: 8 * TILE, state: "normal" }],
              frightenedTimer: 0.4,
              pelletsRemaining: 52,
              ghostMode: "scatter"
            });

            const endingPulse = gameAudio.musicPulseInterval(endingFrightened, {
              frightenedTimer: 0.4
            });

            return { earlyFrightened, endingFrightened, endingPulse };
            """
        )

        self.assertGreater(result["endingFrightened"], result["earlyFrightened"])
        self.assertLess(result["endingPulse"], 0.34)

    def test_cruise_elroy_adds_late_board_pressure(self):
        result = run_audio_behavior(
            """
            const withoutElroy = gameAudio.computeThreatLevel({
              player: { x: 8 * TILE, y: 8 * TILE },
              ghosts: [{ x: 12 * TILE, y: 8 * TILE, name: "red", state: "normal", elroyStage: null }],
              frightenedTimer: 0,
              pelletsRemaining: 8,
              ghostMode: "chase"
            });

            const withElroy = gameAudio.computeThreatLevel({
              player: { x: 8 * TILE, y: 8 * TILE },
              ghosts: [{ x: 12 * TILE, y: 8 * TILE, name: "red", state: "normal", elroyStage: { speedMultiplier: 1.1 } }],
              frightenedTimer: 0,
              pelletsRemaining: 8,
              ghostMode: "chase"
            });

            return { withoutElroy, withElroy };
            """
        )

        self.assertGreater(result["withElroy"], result["withoutElroy"])


if __name__ == "__main__":
    unittest.main()
