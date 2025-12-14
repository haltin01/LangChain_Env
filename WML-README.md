# IBM WML quick setup & test ✅

This short README documents how to recreate the environment used for the quick test, and how to run the `sample_wml_test.py` script included in the repo.

---

## Prerequisites 🔧
- macOS (you already used Homebrew-managed Python in this repo)
- Python 3.11 (the virtualenv in this project uses Python 3.11)
- (Optional) Homebrew: `brew install python@3.11`

---

## Recreate environment (copy-and-paste) 🧪

```bash
# create venv (if you don't have the provided one)
/opt/homebrew/Cellar/python@3.11/3.11.14_1/bin/python3.11 -m venv .venv311
source .venv311/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

> Note: `requirements.txt` pins the versions I used when testing (`numpy==1.26.4`, `pandas==2.1.4`, `ibm_watson_machine_learning==1.0.368`, etc.). The file is at the project root.

---

## Running the quick sample test (safe, no secrets) ▶️

The repository contains `sample_wml_test.py`, which performs a lightweight check:
- imports `ibm_watson_machine_learning`
- prints distribution info
- tries to instantiate `wml.APIClient` with a dummy config (expected to raise a validation/auth error)
- checks presence of `repository` and other module attributes

Run it like this:

```bash
source .venv311/bin/activate
python sample_wml_test.py 2>&1 | tee sample_wml_test.log
```

The test is intentionally safe: it validates importability and client object construction, but it will raise an error if you don't supply a valid WML URL/API key (expected behaviour).

---

## To run a live end-to-end test (requires real WML credentials) 🔐

Set environment variables (preferred) and then run the script. Example:

```bash
export WML_APIKEY="<your_api_key>"
export WML_URL="https://us-south.ml.cloud.ibm.com"  # replace with your instance url
python -c "from ibm_watson_machine_learning import APIClient; c=APIClient({'url':WML_URL,'apikey':WML_APIKEY}); print(c.version())"
```

If you prefer, I can re-run the `sample_wml_test.py` for you using supplied credentials (best provided via environment variables) and show the live call output.

---

## Files created/changed in the test run ✍️
- `requirements.txt` — pinned packages from the `.venv311` used for testing
- `sample_wml_test.log` (from earlier run) — captured test output

---

If you want, I can:
- add these steps to `README.md` instead of `WML-README.md`, or
- create a small `Makefile` or `dev` script to automate venv activation + setup + test run.

Tell me which of these you'd like next! ✨

---

## LangChain quick test ⚡

I added a minimal LangChain example (`sample_langchain_test.py`) that runs offline using a fake LLM (no API keys required). To run it:

```bash
source .venv311/bin/activate
python sample_langchain_test.py 2>&1 | tee sample_langchain_test.log
```

Notes:
- The example attempts to use `langchain` features if available; otherwise it falls back to a tiny fake LLM implementation so the script is deterministic and safe to run.
- The run output is saved in `sample_langchain_test.log` and a snippet of expected fallback output is included below.

Example expected output (fallback):

```
sample_langchain_test.py - starting

langchain version: 1.1.3
FakeListLLM not available; using fallback FakeLLM
Direct LLM call output:
 Hello, Hakan! (fallback)
```

If you'd like, I can also add a real-provider example (OpenAI, etc.) — I would need API credentials or env vars to run it.

### OpenAI provider example (live test) 🧪

I added `sample_langchain_openai.py`, a minimal example that calls the OpenAI Chat Completions API. It will **check** for `OPENAI_API_KEY` in your environment and exit gracefully if not set.

To run a live test with OpenAI:

```bash
# set your API key (do not share it publicly)
export OPENAI_API_KEY="sk-..."

source .venv311/bin/activate
python sample_langchain_openai.py 2>&1 | tee sample_langchain_openai.log
```

Notes:
- The script uses `openai` (installed into `.venv311`) and calls `gpt-3.5-turbo` with a short, safe prompt.
- If you want the example to use the LangChain `OpenAI` LLM wrapper instead, I can provide a variant that uses `langchain` primitives (and will prefer them if available).

#### LangChain-wrapped OpenAI example & tests ✅

I added `sample_langchain_openai_langchain.py` which attempts to use `langchain` primitives (LLM wrapper + `LLMChain` + `PromptTemplate`) where available, and otherwise falls back to a direct `openai` client call. It prints which path it used and the short response.

I also added a unit test `tests/test_langchain_example.py` that uses a `FakeListLLM` (or a small fallback fake LLM) so the test runs offline and is deterministic. To run the tests:

```bash
source .venv311/bin/activate
python -m pip install pytest  # if you haven't installed pytest
python -m pytest -q
```

The unit test ensures the sample code uses the LLM chain pattern correctly (or calls the LLM directly if chain primitives aren't available in your installed LangChain version).
