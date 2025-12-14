import sys

from smoke_test import get_langchain_llm


def test_get_langchain_llm_none_when_langchain_missing(monkeypatch):
    # Simulate langchain not installed
    monkeypatch.setitem(sys.modules, "langchain", None)

    llm, human_message_cls, desc = get_langchain_llm()
    assert llm is None
    assert human_message_cls is None
    assert desc is None


# Note: integration tests that depend on the real LangChain/OpenAI SDK are covered by smoke_test when env is present
