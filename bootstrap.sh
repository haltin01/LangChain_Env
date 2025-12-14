#!/usr/bin/env bash
set -euo pipefail

# bootstrap.sh
# Build the Docker image, run tests, and run the smoke test (if .env exists).
# Usage:
#   ./bootstrap.sh        # build + tests (+ smoke if .env present)
#   ./bootstrap.sh --start # build + tests + start app service detached

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT_DIR"

echo "Bootstrap: building Docker images..."
docker compose build --parallel

echo "Running tests in container (pytest)..."
docker compose run --rm tests

if [ -f ".env" ]; then
  echo ".env found — running smoke test in container..."
  docker compose run --rm app || { echo "Smoke test failed"; exit 1; }
else
  echo ".env not found — skipping online smoke test. Create a .env with OPENAI_API_KEY to run it."
fi

if [ "${1-}" = "--start" ]; then
  echo "Starting app service in detached mode (docker compose up -d)..."
  docker compose up -d app
  echo "App service started. Use 'docker compose logs -f app' to follow logs or 'docker compose down' to stop." 
fi

echo "Bootstrap complete."