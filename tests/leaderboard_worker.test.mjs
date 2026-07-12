import assert from "node:assert/strict";
import test from "node:test";

import worker from "../src/leaderboard.mjs";

test("accepts the browser CORS preflight from GitHub Pages", async () => {
  const response = await worker.fetch(
    new Request("https://maze-muncher-leaderboard.example.workers.dev/api/leaderboard", {
      method: "OPTIONS",
      headers: { Origin: "https://eduard-keilmann.github.io" }
    }),
    {}
  );

  assert.equal(response.status, 204);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), "https://eduard-keilmann.github.io");
  assert.match(response.headers.get("Access-Control-Allow-Methods"), /POST/);
});

test("returns the selected mode's top scores to the GitHub Pages origin", async () => {
  const response = await worker.fetch(
    new Request("https://maze-muncher-leaderboard.example.workers.dev/api/leaderboard?mode=old-like", {
      headers: { Origin: "https://eduard-keilmann.github.io" }
    }),
    {
      LEADERBOARD_DB: {
        prepare(sql) {
          assert.match(sql, /FROM leaderboard_entries/);
          return {
            bind(mode) {
              assert.equal(mode, "old-like");
              return {
                all: async () => ({
                  results: [{
                    id: "entry-1",
                    name: "Maze",
                    score: 1200,
                    created_at: "2026-07-13T10:00:00.000Z"
                  }]
                })
              };
            }
          };
        }
      },
      LEADERBOARD_RATE_LIMIT_SALT: "test-salt"
    }
  );

  assert.equal(response.status, 200);
  assert.equal(response.headers.get("Access-Control-Allow-Origin"), "https://eduard-keilmann.github.io");
  assert.deepEqual(await response.json(), {
    entries: [{
      id: "entry-1",
      name: "Maze",
      score: 1200,
      mode: "old-like",
      createdAt: "2026-07-13T10:00:00.000Z"
    }]
  });
});

test("starts one rate-limited run for a known mode without storing the visitor IP", async () => {
  const statements = [];
  const database = {
    prepare(sql) {
      return {
        bind(...values) {
          const statement = {
            sql,
            values,
            async first() {
              if (sql.includes("INSERT INTO leaderboard_rate_limits")) {
                return { count: 1 };
              }
              throw new Error(`Unexpected first query: ${sql}`);
            }
          };
          statements.push(statement);
          return statement;
        }
      };
    },
    async batch(batch) {
      statements.push(...batch);
      return [];
    }
  };

  const response = await worker.fetch(
    new Request("https://maze-muncher-leaderboard.example.workers.dev/api/leaderboard", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Origin: "https://eduard-keilmann.github.io",
        "CF-Connecting-IP": "203.0.113.5"
      },
      body: JSON.stringify({ action: "start", mode: "old-like" })
    }),
    { LEADERBOARD_DB: database, LEADERBOARD_RATE_LIMIT_SALT: "test-salt" }
  );

  assert.equal(response.status, 201);
  const body = await response.json();
  assert.match(body.runId, /^[0-9a-f-]{36}$/);
  assert.equal(body.mode, "old-like");
  assert.doesNotMatch(JSON.stringify(statements), /203\.0\.113\.5/);
  assert.match(
    statements.find(statement => statement.sql.includes("INSERT INTO leaderboard_runs")).sql,
    /mode/
  );
});

test("stores one plausible score in the ticket's gameplay mode and reports its rank", async () => {
  const statements = [];
  const database = {
    prepare(sql) {
      return {
        bind(...values) {
          const statement = {
            sql,
            values,
            async first() {
              if (sql.includes("SELECT started_at, mode FROM leaderboard_runs")) {
                return { started_at: Date.now() - 30_000, mode: "old-like" };
              }
              if (sql.includes("SELECT id FROM leaderboard_entries")) {
                return { id: values[0] };
              }
              if (sql.includes("SELECT COUNT(*) AS rank")) {
                return { rank: 0 };
              }
              throw new Error(`Unexpected first query: ${sql}`);
            },
            async run() {
              if (sql.includes("DELETE FROM leaderboard_runs")) {
                return { meta: { changes: 1 } };
              }
              throw new Error(`Unexpected write query: ${sql}`);
            }
          };
          statements.push(statement);
          return statement;
        }
      };
    },
    async batch(batch) {
      statements.push(...batch);
      return [];
    }
  };

  const response = await worker.fetch(
    new Request("https://maze-muncher-leaderboard.example.workers.dev/api/leaderboard", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "submit",
        runId: "run-1",
        name: " Maze ",
        score: 1200
      })
    }),
    { LEADERBOARD_DB: database, LEADERBOARD_RATE_LIMIT_SALT: "test-salt" }
  );

  assert.equal(response.status, 201);
  assert.deepEqual(await response.json(), { accepted: true, rank: 1 });
  assert.ok(
    statements.some(statement =>
      statement.sql.includes("INSERT INTO leaderboard_entries") &&
      statement.values.includes("Maze") &&
      statement.values.includes("old-like")
    )
  );
});

test("rejects a score that cannot fit within the ticket's run duration", async () => {
  const database = {
    prepare(sql) {
      return {
        bind() {
          return {
            async first() {
              if (sql.includes("SELECT started_at, mode FROM leaderboard_runs")) {
                return { started_at: Date.now() - 1_000, mode: "old-like" };
              }
              throw new Error(`Unexpected first query: ${sql}`);
            },
            async run() {
              if (sql.includes("DELETE FROM leaderboard_runs")) {
                return { meta: { changes: 1 } };
              }
              throw new Error(`Unexpected write query: ${sql}`);
            }
          };
        }
      };
    }
  };

  const response = await worker.fetch(
    new Request("https://maze-muncher-leaderboard.example.workers.dev/api/leaderboard", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "submit",
        runId: "run-1",
        name: "Maze",
        score: 100_000
      })
    }),
    { LEADERBOARD_DB: database, LEADERBOARD_RATE_LIMIT_SALT: "test-salt" }
  );

  assert.equal(response.status, 422);
  assert.deepEqual(await response.json(), { error: "Score is not plausible for this run" });
});
