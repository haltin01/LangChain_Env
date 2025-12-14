import os
import subprocess


def test_smoke_runs_without_key(tmp_path):
    # When OPENAI_API_KEY is not set and no .env exists in cwd, the script should exit with code 2
    env = dict(os.environ)
    env.pop("OPENAI_API_KEY", None)
    # run in an empty temporary directory so load_dotenv() won't find .env
    res = subprocess.run(["python3", str((tmp_path / "../smoke_test.py").resolve())], env=env, cwd=str(tmp_path))
    assert res.returncode == 2


# Note: a full online test that hits OpenAI requires a valid key and is skipped by default.
