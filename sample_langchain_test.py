"""
Minimal LangChain example for local testing (no API keys required).
Uses FakeListLLM (if available) or a small fallback stub LLM.
Run with: source .venv311/bin/activate && python sample_langchain_test.py
"""

from __future__ import annotations

import sys


def main():
    print("sample_langchain_test.py - starting\n")

    # Print package/version info
    try:
        import langchain
        print("langchain version:", getattr(langchain, "__version__", "unknown"))
    except Exception as e:
        print("langchain import FAILED ->", e)
        sys.exit(1)

    # Try to use a Fake LLM provided by LangChain for deterministic testing
    try:
        from langchain.llms.fake import FakeListLLM

        llm = FakeListLLM(responses=["Hello, Hakan! This is a fake LLM response for testing."])
        print("Using langchain.llms.fake.FakeListLLM")
    except Exception:
        # Fallback: tiny LLM-like object with the minimal interface used by LLMChain
        print("FakeListLLM not available; using fallback FakeLLM")

        class FakeLLM:
            def __init__(self, responses):
                self._responses = list(responses)

            def __call__(self, prompt: str, **_kwargs) -> str:
                # Very naive: always return the first response
                return self._responses[0]

        llm = FakeLLM(["Hello, Hakan! (fallback)"])

    # Use a PromptTemplate + LLMChain to demonstrate typical usage
    try:
        from langchain import LLMChain
        from langchain.prompts import PromptTemplate

        prompt = PromptTemplate(input_variables=["name"], template="Say hello to {name} in one sentence.")
        chain = LLMChain(llm=llm, prompt=prompt)

        # When using LLMChain.run you can pass a single str or named inputs depending on your version
        out = chain.run("Hakan")
        print("\nChain output:\n", out)

    except Exception as e:
        print("LLMChain example failed ->", e)
        # Try a direct LLM call as a last resort
        try:
            result = llm("Say hello to Hakan in one sentence.")
            print("\nDirect LLM call output:\n", result)
        except Exception as e2:
            print("Direct LLM call also failed ->", e2)
            raise


if __name__ == "__main__":
    main()
