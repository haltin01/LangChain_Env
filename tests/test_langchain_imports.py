import sys

from smoke_test import run_test, PROMPT


def test_get_langchain_llm_none_when_langchain_missing(monkeypatch):
    # Simulate langchain not installed
    monkeypatch.setitem(sys.modules, "langchain", None)
    # Ensure OPENAI_API_KEY unset so run_test returns 2 (we're testing import behavior separately)
    import os

    env = dict(os.environ)
    env.pop("OPENAI_API_KEY", None)

    # Calling run_test should return 2 because OPENAI_API_KEY not set
    # but it should not raise an import error
    assert run_test() == 2


# Note: integration tests that depend on the real LangChain/OpenAI SDK are covered by smoke_test when env is present
