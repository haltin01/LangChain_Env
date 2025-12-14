#!/bin/sh
set -e

# Entrypoint validates required env vars and then execs the command
if [ -z "$OPENAI_API_KEY" ]; then
  echo "ERROR: OPENAI_API_KEY is not set. Provide it via an .env file or -e OPENAI_API_KEY=..." >&2
  echo "Note: do not commit your API key. Use repo secrets or CI variables for automation." >&2
  exit 2
fi

exec "$@"