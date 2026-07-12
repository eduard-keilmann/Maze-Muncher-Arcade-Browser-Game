# Cloudflare Worker and D1 as a standby leaderboard path

The active production leaderboard remains the Vercel Function backed by Upstash Redis. A Cloudflare Worker and D1 schema are kept in this repository as a prepared alternative, not a second active system.

The Worker exposes the same browser contract at `/api/leaderboard`: top 100 entries per gameplay mode, server-issued four-hour run tickets, one submission per ticket, daily hashed-IP rate limiting, name validation, and the existing elapsed-time score plausibility rule. Therefore a future browser cutover changes only the production host in `LEADERBOARD_API_URL`.

There is deliberately no dual write and no automatic Redis-to-D1 synchronization. Dual write would create two sources of truth and failure cases while Vercel/Upstash is still the chosen production path. At a later cutover, copy the public top 100 of each mode once, verify the deployed Worker, then change the browser host. Reverting consists of restoring the Vercel host; D1-only entries are not merged back automatically.
