# Maze Muncher

A fast little browser arcade game inspired by classic maze chases. Eat every pellet, grab power pellets, turn the chase around, and survive the ghosts long enough to clear the maze.

No install. No build. Open one HTML file and play.

## Play

Open the actual game file in a browser:

```text
maze_muncher_browser_arcade.html
```

Or play online:

- Gameplay instructions: https://eduard-keilmann.github.io/Maze-Muncher-Arcade-Browser-Game/
- Play the game: https://eduard-keilmann.github.io/Maze-Muncher-Arcade-Browser-Game/maze_muncher_browser_arcade.html

The game runs directly in a modern browser.

## Why Try It

- Classic pellet-chasing tension in a compact browser game.
- Smooth grid movement with buffered turns.
- Two gameplay modes: `MODE: OLD-LIKE` is the default, and `MODE: MAZE MUNCHER` remains selectable.
- Four ghosts with chase, scatter, frightened, home, and eaten states.
- Power pellets turn chase pressure around. In late Old-like levels they can reverse ghosts without making them edible.
- Score, high score, lives, levels, pause, ready, death, game-over states, generated arcade-style sound effects, and quiet threat-reactive music.
- Optional online high scores: when API and Redis are configured, each gameplay mode has its own public top 100. Without that API, the game keeps its existing local high-score behavior.
- Works on desktop and touch screens.

## Controls

Desktop:

- Move: Arrow keys or WASD
- Start: Space, Enter, a movement key, or canvas tap/swipe
- Pause/resume: Space or P
- Sound: use SOUND: ON/OFF toggle
- Music: use MUSIC: ON/OFF toggle
- Restart from title/game-over: Enter

Touch/mobile:

- Move: continuous swipe anywhere on the game page, tap the canvas near the desired turn direction, or use the on-screen D-pad
- Hold a D-pad direction to keep that turn queued
- Pause: tap Pause
- Restart: hold Restart
- Sound: use SOUND: ON/OFF toggle
- Music: use MUSIC: ON/OFF toggle

## Mobile-Friendly

Maze Muncher includes thumb-friendly controls for phones and tablets:

- large on-screen D-pad
- whole-page continuous swipe steering
- canvas tap-to-turn steering relative to Maze Muncher
- press-and-hold direction input
- visible held-button feedback
- haptic feedback where the browser supports `navigator.vibrate`
- compact short-phone portrait layout
- side-by-side short landscape layout
- safer long-press restart to avoid accidental resets

## Run Tests

The repo uses dependency-free Python tests for the static HTML contract:

```sh
python -B -m unittest discover tests
```

The Redis-backed API tests use Node's built-in test runner:

```sh
node --test tests/leaderboard_api.test.cjs
```

The prepared Cloudflare Worker contract is covered separately:

```sh
node --test tests/leaderboard_worker.test.mjs
python3 -B tests/test_leaderboard_schema.py -q
```

## Optional Online High Scores

The static game remains deployable on GitHub Pages. The optional API lives in `api/leaderboard.js` and is deployed as the separate Vercel project `maze-muncher-leaderboard`.

1. Create an Upstash Redis database and copy its REST URL and standard REST token.
2. Import this repository as a Vercel project named `maze-muncher-leaderboard`; leave its root directory at the repository root.
3. Add these Vercel environment variables:
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`
   - `LEADERBOARD_RATE_LIMIT_SALT` — a private random value used only for daily rate-limit hashes.
4. Deploy. The game calls `https://maze-muncher-leaderboard.vercel.app/api/leaderboard`.

The endpoint permits requests from the GitHub Pages origin and exactly `http://localhost:8080` for local development. Run `npx vercel dev` when testing the API locally; no Redis, Docker, or project dependency is required on the development machine when using the Upstash development database.

For an end-to-end local check, create an ignored `.env.local` with the three variables above, start `npx vercel dev`, then serve this repository with `python3 -m http.server 8080`. Open `http://localhost:8080/maze_muncher_browser_arcade.html`; the game automatically uses `http://localhost:3000` for its leaderboard API.

### Prepared Cloudflare D1 Alternative

Vercel and Upstash remain the active production path. `src/leaderboard.mjs`, `migrations/0001_create_leaderboard.sql`, and `wrangler.toml` are a prepared, currently unused Cloudflare Worker + D1 equivalent. Its endpoint is deliberately the same `/api/leaderboard` contract, so the later browser change is only the production host in `LEADERBOARD_API_URL` inside `maze_muncher_browser_arcade.html`.

When a migration is wanted:

1. Create the D1 database: `npx wrangler d1 create maze-muncher-leaderboard`.
2. Replace the placeholder `database_id` in `wrangler.toml` with the returned ID.
3. Apply the schema: `npx wrangler d1 execute maze-muncher-leaderboard --remote --file=migrations/0001_create_leaderboard.sql`.
4. Set a new private salt: `npx wrangler secret put LEADERBOARD_RATE_LIMIT_SALT`.
5. Deploy the Worker: `npx wrangler deploy`.
6. Copy the current public top 100 of both modes from Vercel/Upstash into D1, verify `https://<worker>.workers.dev/api/leaderboard?mode=old-like`, then replace only the production host in `LEADERBOARD_API_URL`.

D1 does not synchronize with Upstash automatically. Do not switch the browser URL before the one-time data copy and Worker check. Rollback is simply restoring the existing Vercel host; entries written only to D1 are not copied back automatically.

## Project Notes

- Main game file: `maze_muncher_browser_arcade.html`
- Product notes: `specs_product.md`
- Architecture notes: `specs_architecture.md`
- Mobile QA checklist: `issues/mobile-qa-checklist.md`
- Remaining human/device validation: `issues/hitl-remaining.md`
