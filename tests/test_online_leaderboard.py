import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HTML = (PROJECT_ROOT / "maze_muncher_browser_arcade.html").read_text(encoding="utf-8")


class OnlineLeaderboardTests(unittest.TestCase):
    def test_online_controls_stay_hidden_until_the_api_is_available(self):
        self.assertRegex(HTML, re.compile(r'data-action="leaderboard"[^>]*hidden'))
        self.assertRegex(HTML, re.compile(r'const LEADERBOARD_API_URL\s*=\s*"https://maze-muncher-leaderboard\.vercel\.app"'))
        self.assertRegex(HTML, re.compile(r'leaderboardButton\.hidden\s*=\s*!leaderboardAvailable'))
        self.assertRegex(HTML, re.compile(r'AbortSignal\.timeout\(1000\)'))

    def test_game_start_requests_a_ticket_without_waiting_for_the_api(self):
        new_game = re.search(r'function newGame\(\) \{(?P<body>[\s\S]*?)\n    \}', HTML)
        self.assertIsNotNone(new_game)
        self.assertRegex(new_game.group("body"), re.compile(r'gameLifecycle\.startNewGame\(\)'))
        self.assertRegex(new_game.group("body"), re.compile(r'requestOnlineRunTicket\(\)'))

    def test_game_over_offers_a_name_only_for_a_possible_top_100_score(self):
        self.assertRegex(HTML, re.compile(r'onlineEntries\.length\s*>=\s*100\s*&&\s*score\s*<\s*onlineEntries\[99\]\.score'))
        self.assertRegex(HTML, re.compile(r'function offerOnlineScoreEntry\(\)'))
        self.assertRegex(HTML, re.compile(r'loseLife\(\)\s*\{[\s\S]*?offerOnlineScoreEntry\(\)'))


if __name__ == "__main__":
    unittest.main()
