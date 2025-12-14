# LangChain_Env

Minimal scaffold to verify LangChain/OpenAI integration and demonstrate a smoke test using a real OpenAI API key.

## Quick start

1. Create & activate a virtual environment (recommended name: `.venv`)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key in your shell

```bash
export OPENAI_API_KEY="sk-..."
```

4. Run the smoke test

```bash
python3 smoke_test.py
```

## Docker

You can run the project in Docker (recommended if you don't want to create a local venv).

Build the image:

```bash
docker build -t langchain-env:latest .
```

Run the smoke test with your local `.env` (keeps your key out of the image and git):

```bash
docker run --rm --env-file .env langchain-env:latest python3 smoke_test.py
```

Run pytest inside Docker:

```bash
docker run --rm --env-file .env langchain-env:latest pytest -q
```

Or use docker-compose:

```bash
docker compose up --build app
# run tests
docker compose run --rm tests
```

This script first tries to use `LangChain` and falls back to the `openai` SDK if needed. The smoke test expects the model to respond with the exact phrase `smoke test OK`.

## Tests

Run the local test that verifies behavior when no API key is set:

```bash
pytest -q
```

> Note: an online smoke test that calls the OpenAI API will use your real key if present in the environment. Keep your key private.
# LangChain_Env