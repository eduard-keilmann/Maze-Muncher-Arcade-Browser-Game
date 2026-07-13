const assert = require("node:assert/strict");
const test = require("node:test");

const leaderboard = require("../api/leaderboard.js");

function response() {
  return {
    headers: {},
    statusCode: 200,
    setHeader(name, value) {
      this.headers[name] = value;
    },
    status(statusCode) {
      this.statusCode = statusCode;
      return this;
    },
    json(body) {
      this.body = body;
    },
    end() {
      this.ended = true;
    }
  };
}

test("accepts the browser CORS preflight from GitHub Pages", async () => {
  const res = response();
  await leaderboard({
    method: "OPTIONS",
    headers: { origin: "https://eduard-keilmann.github.io" }
  }, res);

  assert.equal(res.statusCode, 204);
  assert.equal(res.headers["Access-Control-Allow-Origin"], "https://eduard-keilmann.github.io");
  assert.match(res.headers["Access-Control-Allow-Methods"], /POST/);
});

test("does not allow an unconfigured localhost origin", async () => {
  const res = response();
  await leaderboard({
    method: "OPTIONS",
    headers: { origin: "http://localhost:4173" }
  }, res);

  assert.equal(res.statusCode, 204);
  assert.equal(res.headers["Access-Control-Allow-Origin"], undefined);
});

test("allows the documented localhost origin", async () => {
  const res = response();
  await leaderboard({
    method: "OPTIONS",
    headers: { origin: "http://localhost:8080" }
  }, res);

  assert.equal(res.statusCode, 204);
  assert.equal(res.headers["Access-Control-Allow-Origin"], "http://localhost:8080");
});

test("returns the top leaderboard entries for an allowed gameplay mode", async () => {
  const originalFetch = global.fetch;
  const originalEnv = { ...process.env };
  process.env.UPSTASH_REDIS_REST_URL = "https://redis.example.test";
  process.env.UPSTASH_REDIS_REST_TOKEN = "test-token";

  global.fetch = async (url, options) => {
    assert.equal(url, "https://redis.example.test/pipeline");
    assert.equal(options.headers.Authorization, "Bearer test-token");
    return {
      ok: true,
      async json() {
        return [{ result: ["eyJuYW1lIjoiTWF6ZSIsImNyZWF0ZWRBdCI6IjIwMjYtMDctMTFUMDA6MDA6MDBaIn0=", "1200"] }];
      }
    };
  };

  const res = response();
  await leaderboard({
    method: "GET",
    query: { mode: "old-like" },
    headers: { origin: "https://eduard-keilmann.github.io" }
  }, res);

  global.fetch = originalFetch;
  process.env = originalEnv;

  assert.equal(res.statusCode, 200);
  assert.deepEqual(res.body, {
    entries: [{ name: "Maze", score: 1200, mode: "old-like", createdAt: "2026-07-11T00:00:00Z" }]
  });
});

test("issues one run ticket for a known gameplay mode", async () => {
  const originalFetch = global.fetch;
  const originalEnv = { ...process.env };
  process.env.UPSTASH_REDIS_REST_URL = "https://redis.example.test";
  process.env.UPSTASH_REDIS_REST_TOKEN = "test-token";
  process.env.LEADERBOARD_RATE_LIMIT_SALT = "test-salt";
  let requestCount = 0;

  global.fetch = async () => {
    requestCount++;
    return {
      ok: true,
      async json() {
        return requestCount === 1
          ? [{ result: 1 }, { result: 1 }]
          : [{ result: "OK" }];
      }
    };
  };

  const res = response();
  await leaderboard({
    method: "POST",
    body: { action: "start", mode: "old-like" },
    headers: {
      origin: "https://eduard-keilmann.github.io",
      "x-forwarded-for": "203.0.113.5"
    }
  }, res);

  global.fetch = originalFetch;
  process.env = originalEnv;

  assert.equal(res.statusCode, 201);
  assert.equal(res.body.mode, "old-like");
  assert.match(res.body.runId, /^[0-9a-f-]{36}$/);
});

test("accepts one plausible named score and returns its rank", async () => {
  const originalFetch = global.fetch;
  const originalEnv = { ...process.env };
  process.env.UPSTASH_REDIS_REST_URL = "https://redis.example.test";
  process.env.UPSTASH_REDIS_REST_TOKEN = "test-token";
  const run = Buffer.from(JSON.stringify({
    mode: "old-like",
    startedAt: Date.now() - 30_000
  })).toString("base64url");
  let requestCount = 0;

  global.fetch = async () => {
    requestCount++;
    return {
      ok: true,
      async json() {
        return requestCount === 1
          ? [{ result: run }]
          : [{ result: 1 }, { result: 0 }, { result: 0 }];
      }
    };
  };

  const res = response();
  await leaderboard({
    method: "POST",
    body: { action: "submit", runId: "run-1", name: " Maze ", score: 1200 },
    headers: { origin: "https://eduard-keilmann.github.io" }
  }, res);

  global.fetch = originalFetch;
  process.env = originalEnv;

  assert.equal(res.statusCode, 201);
  assert.equal(res.body.accepted, true);
  assert.equal(res.body.rank, 1);
});

test("rejects a score that cannot fit within the run duration", async () => {
  const originalFetch = global.fetch;
  const originalEnv = { ...process.env };
  process.env.UPSTASH_REDIS_REST_URL = "https://redis.example.test";
  process.env.UPSTASH_REDIS_REST_TOKEN = "test-token";
  const run = Buffer.from(JSON.stringify({
    mode: "old-like",
    startedAt: Date.now() - 30_000
  })).toString("base64url");

  global.fetch = async () => ({
    ok: true,
    async json() {
      return [{ result: run }];
    }
  });

  const res = response();
  await leaderboard({
    method: "POST",
    body: { action: "submit", runId: "run-1", name: "Maze", score: 100_000 },
    headers: { origin: "https://eduard-keilmann.github.io" }
  }, res);

  global.fetch = originalFetch;
  process.env = originalEnv;

  assert.equal(res.statusCode, 422);
  assert.equal(res.body.error, "Score is not plausible for this run");
});
