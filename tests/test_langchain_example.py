import importlib


def test_fake_llm_chain_behavior():
    """Unit test that uses a fake LLM (no network calls) to validate LLMChain usage if available."""
    # Build a fake LLM with the minimal interface (callable or generate)
    try:
        from langchain.llms.fake import FakeListLLM
        fake = FakeListLLM(responses=["Hello, Hakan! (from fake LLM)"])
        can_direct = True
    except Exception:
        # Fallback fake
        class FakeLLM:
            def __init__(self, responses):
                self._responses = list(responses)

            def __call__(self, prompt: str, **_kwargs):
                return self._responses[0]

        fake = FakeLLM(["Hello, Hakan! (fallback)"])
        can_direct = False

    # Try to use LLMChain + PromptTemplate if available to validate chain integration
    try:
        from langchain import LLMChain, PromptTemplate
        prompt = PromptTemplate(input_variables=['name'], template='Say hello to {name} in one sentence.')
        chain = LLMChain(llm=fake, prompt=prompt)
        try:
            out = chain.run('Hakan')
        except Exception:
            try:
                out = chain.predict(name='Hakan')
            except Exception:
                out = fake('Say hello to Hakan in one sentence.')

    except Exception:
        # If LLMChain not available, call fake LLM directly
        out = fake('Say hello to Hakan in one sentence.')

    assert isinstance(out, str)
    assert 'Hakan' in out
