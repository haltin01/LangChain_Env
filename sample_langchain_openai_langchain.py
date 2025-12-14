"""
LangChain-wrapped OpenAI example.
- Prefers LangChain primitives (PromptTemplate + LLMChain + OpenAI LLM wrapper) if available
- Falls back to direct OpenAI client call when LangChain wrapping isn't available

Usage:
  export OPENAI_API_KEY="sk-..."
  source .venv311/bin/activate
  python sample_langchain_openai_langchain.py

The script is defensive about different LangChain versions and will print which path it used.
"""

from __future__ import annotations
import os
import sys

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_KEY:
    print("OPENAI_API_KEY not set. Export it to run a live test. Exiting.")
    sys.exit(0)

used = None
result = None

# Try LangChain high-level approach
try:
    # Attempt common import patterns
    try:
        from langchain import LLMChain, PromptTemplate, OpenAI
        used = 'langchain_top'
    except Exception:
        try:
            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            from langchain.llms import OpenAI
            used = 'langchain_submodules'
        except Exception:
            # some installations have 'langchain_core' split; try a few more fallbacks
            try:
                from langchain_core import version as _v
                # `langchain` package seems to be installed but subpackages may be missing
                raise ImportError('langchain present but submodules not available')
            except Exception:
                raise

    # Create LLM and chain - adapt to different constructor signatures
    try:
        llm = OpenAI(temperature=0)
    except TypeError:
        # some wrappers take api_key or expect env var; ensure env is set
        llm = OpenAI()

    prompt = PromptTemplate(input_variables=['name'], template='Say hello to {name} in one sentence.')

    # LLMChain api varies; try run(), then predict()
    chain = LLMChain(llm=llm, prompt=prompt)
    try:
        # Some versions allow chain.run('Hakan')
        result = chain.run('Hakan')
    except Exception:
        try:
            result = chain.predict(name='Hakan')
        except Exception:
            # Last resort: call llm directly
            try:
                result = llm('Say hello to Hakan in one sentence.')
            except Exception as e:
                raise RuntimeError('Failed to invoke chain or llm: ' + str(e))

except Exception as e:
    used = 'fallback_openai'
    # Use direct OpenAI client (modern API)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful test assistant that responds briefly.'},
                {'role': 'user', 'content': 'Say hello to Hakan in one short sentence.'},
            ],
            max_tokens=60,
            temperature=0.0,
        )
        try:
            result = resp.choices[0].message.content.strip()
        except Exception:
            try:
                result = resp.choices[0]['message']['content'].strip()
            except Exception:
                result = str(resp)
    except Exception as e2:
        print('Fallback OpenAI call failed ->', e2)
        raise

print('Used path:', used)
print('\nResult:\n', result)
