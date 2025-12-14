import os
import subprocess


def test_smoke_runs_without_key():
    # When OPENAI_API_KEY is not set, the script should exit with code 2
    env = dict(os.environ)
    env.pop("OPENAI_API_KEY", None)
    res = subprocess.run(["python3", "smoke_test.py"], env=env)
    assert res.returncode == 2


# Note: a full online test that hits OpenAI requires a valid key and is skipped by default.
