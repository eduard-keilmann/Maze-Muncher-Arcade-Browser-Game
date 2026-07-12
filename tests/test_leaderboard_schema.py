from pathlib import Path
import sqlite3
import unittest


class LeaderboardSchemaTest(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        migration = Path("migrations/0001_create_leaderboard.sql").read_text(encoding="utf-8")
        self.connection.executescript(migration)

    def tearDown(self):
        self.connection.close()

    def test_keeps_duplicate_names_and_separate_mode_leaderboards(self):
        self.connection.executemany(
            "INSERT INTO leaderboard_entries (id, mode, name, score, created_at) VALUES (?, ?, ?, ?, ?)",
            [
                ("first", "old-like", "Maze", 1200, "2026-07-13T10:00:00.000Z"),
                ("second", "old-like", "Maze", 2400, "2026-07-13T10:01:00.000Z"),
                ("third", "maze-muncher", "Maze", 3600, "2026-07-13T10:02:00.000Z"),
            ],
        )

        old_like_rows = self.connection.execute(
            "SELECT name, score FROM leaderboard_entries WHERE mode = ? ORDER BY score DESC",
            ("old-like",),
        ).fetchall()
        self.assertEqual(old_like_rows, [("Maze", 2400), ("Maze", 1200)])

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO leaderboard_entries (id, mode, name, score, created_at) VALUES (?, ?, ?, ?, ?)",
                ("invalid", "unknown", "Maze", 1, "2026-07-13T10:03:00.000Z"),
            )

    def test_pruning_keeps_the_top_100_of_one_mode_only(self):
        self.connection.executemany(
            "INSERT INTO leaderboard_entries (id, mode, name, score, created_at) VALUES (?, ?, ?, ?, ?)",
            [
                (f"old-{score}", "old-like", "Maze", score, "2026-07-13T10:00:00.000Z")
                for score in range(101)
            ]
            + [("maze-entry", "maze-muncher", "Maze", 9999, "2026-07-13T10:00:00.000Z")],
        )

        self.connection.execute(
            """DELETE FROM leaderboard_entries
               WHERE mode = ? AND id NOT IN (
                 SELECT id FROM leaderboard_entries
                 WHERE mode = ?
                 ORDER BY score DESC, created_at ASC, id ASC
                 LIMIT ?
               )""",
            ("old-like", "old-like", 100),
        )

        old_like_scores = self.connection.execute(
            "SELECT score FROM leaderboard_entries WHERE mode = ? ORDER BY score ASC",
            ("old-like",),
        ).fetchall()
        maze_count = self.connection.execute(
            "SELECT COUNT(*) FROM leaderboard_entries WHERE mode = ?",
            ("maze-muncher",),
        ).fetchone()[0]
        self.assertEqual(len(old_like_scores), 100)
        self.assertEqual(old_like_scores[0], (1,))
        self.assertEqual(maze_count, 1)


if __name__ == "__main__":
    unittest.main()
