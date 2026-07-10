# Vercel Function and Upstash Redis for online leaderboard

GitHub Pages remains the static game host. An optional Vercel Function provides the public leaderboard API and accesses Upstash Redis through private REST credentials, avoiding a browser-to-Redis connection and server maintenance while retaining a free small-project deployment path.
