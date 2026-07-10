const ALLOWED_ORIGIN = "https://eduard-keilmann.github.io";
const GAMEPLAY_MODES = new Set(["maze-muncher", "old-like"]);
const { createHash, randomUUID } = require("node:crypto");

async function redis(commands) {
  const response = await fetch(`${process.env.UPSTASH_REDIS_REST_URL}/pipeline`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.UPSTASH_REDIS_REST_TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(commands)
  });

  if (!response.ok) throw new Error("Redis request failed");
  return response.json();
}

module.exports = async function leaderboard(req, res) {
  const origin = req.headers.origin;
  if (origin === ALLOWED_ORIGIN || /^http:\/\/localhost:\d+$/.test(origin || "")) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  }

  if (req.method === "OPTIONS") return res.status(204).end();

  if (req.method === "POST") {
    const { action, mode, runId, name, score } = req.body || {};

    if (action === "submit") {
      const leaderboardName = typeof name === "string" ? name.trim() : "";
      if (
        typeof runId !== "string" ||
        !Number.isSafeInteger(score) ||
        score < 0 ||
        !leaderboardName ||
        Array.from(leaderboardName).length > 20 ||
        /[\u0000-\u001F\u007F]/.test(leaderboardName)
      ) {
        return res.status(400).json({ error: "Invalid leaderboard score" });
      }

      if (!process.env.UPSTASH_REDIS_REST_URL || !process.env.UPSTASH_REDIS_REST_TOKEN) {
        return res.status(503).json({ error: "Leaderboard unavailable" });
      }

      try {
        const [storedRun] = await redis([["GETDEL", `maze-muncher:leaderboard:run:${runId}`]]);
        if (!storedRun.result) {
          return res.status(409).json({ error: "Run ticket is missing or already used" });
        }

        const run = JSON.parse(Buffer.from(storedRun.result, "base64url").toString("utf8"));
        const elapsedSeconds = (Date.now() - run.startedAt) / 1000;
        if (
          !GAMEPLAY_MODES.has(run.mode) ||
          !Number.isFinite(elapsedSeconds) ||
          elapsedSeconds < 0 ||
          elapsedSeconds > 14400 ||
          score > 10000 + Math.floor(elapsedSeconds * 500)
        ) {
          return res.status(422).json({ error: "Score is not plausible for this run" });
        }

        const entry = Buffer.from(JSON.stringify({
          id: randomUUID(),
          name: leaderboardName,
          createdAt: new Date().toISOString()
        })).toString("base64url");
        const leaderboardKey = `maze-muncher:leaderboard:${run.mode}`;
        const [, , rank] = await redis([
          ["ZADD", leaderboardKey, score, entry],
          ["ZREMRANGEBYRANK", leaderboardKey, 0, -101],
          ["ZREVRANK", leaderboardKey, entry]
        ]);

        if (rank.result === null) {
          return res.status(200).json({ accepted: false });
        }

        return res.status(201).json({ accepted: true, rank: Number(rank.result) + 1 });
      } catch (_) {
        return res.status(503).json({ error: "Leaderboard unavailable" });
      }
    }

    if (action !== "start" || !GAMEPLAY_MODES.has(mode)) {
      return res.status(400).json({ error: "Unknown leaderboard action or gameplay mode" });
    }

    if (!process.env.UPSTASH_REDIS_REST_URL || !process.env.UPSTASH_REDIS_REST_TOKEN || !process.env.LEADERBOARD_RATE_LIMIT_SALT) {
      return res.status(503).json({ error: "Leaderboard unavailable" });
    }

    const ipAddress = (req.headers["x-forwarded-for"] || "").split(",")[0].trim();
    const today = new Date().toISOString().slice(0, 10);
    const rateKey = createHash("sha256")
      .update(`${today}:${ipAddress}:${process.env.LEADERBOARD_RATE_LIMIT_SALT}`)
      .digest("hex");
    const newRunId = randomUUID();

    try {
      const [rate] = await redis([
        ["INCR", `maze-muncher:leaderboard:rate:${today}:${rateKey}`],
        ["EXPIRE", `maze-muncher:leaderboard:rate:${today}:${rateKey}`, 86400]
      ]);
      if (Number(rate.result) > 30) {
        return res.status(429).json({ error: "Too many leaderboard runs today" });
      }

      const run = Buffer.from(JSON.stringify({ mode, startedAt: Date.now() })).toString("base64url");
      const [storedRun] = await redis([[
        "SET",
        `maze-muncher:leaderboard:run:${newRunId}`,
        run,
        "EX",
        14400,
        "NX"
      ]]);
      if (storedRun.result !== "OK") throw new Error("Run ticket was not stored");

      return res.status(201).json({ runId: newRunId, mode });
    } catch (_) {
      return res.status(503).json({ error: "Leaderboard unavailable" });
    }
  }

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const mode = req.query.mode;
  if (!GAMEPLAY_MODES.has(mode)) {
    return res.status(400).json({ error: "Unknown gameplay mode" });
  }

  if (!process.env.UPSTASH_REDIS_REST_URL || !process.env.UPSTASH_REDIS_REST_TOKEN) {
    return res.status(503).json({ error: "Leaderboard unavailable" });
  }

  try {
    const [entries] = await redis([[
      "ZREVRANGE",
      `maze-muncher:leaderboard:${mode}`,
      0,
      99,
      "WITHSCORES"
    ]]);
    const rows = entries.result || [];
    const leaderboardEntries = [];

    for (let index = 0; index < rows.length; index += 2) {
      const entry = JSON.parse(Buffer.from(rows[index], "base64url").toString("utf8"));
      leaderboardEntries.push({ ...entry, score: Number(rows[index + 1]), mode });
    }

    return res.status(200).json({ entries: leaderboardEntries });
  } catch (_) {
    return res.status(503).json({ error: "Leaderboard unavailable" });
  }
};
