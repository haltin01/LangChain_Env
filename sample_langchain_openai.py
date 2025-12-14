"""
Minimal OpenAI usage example for LangChain-compatible testing.
This script will:
- check for OPENAI_API_KEY in the environment
- call the OpenAI Chat Completions API with a short prompt (model default: gpt-3.5-turbo)
- print the response

Usage:
  export OPENAI_API_KEY="sk-..."
  source .venv311/bin/activate
  python sample_langchain_openai.py

If the key isn't set, the script exits gracefully with a message.
"""

from __future__ import annotations
import os
import sys

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_KEY:
    print("OPENAI_API_KEY not set. To run a live test, set it and re-run. Exiting.")
    sys.exit(0)

# We use the OpenAI SDK directly for a minimal example. Newer openai versions
# (>=1.0.0) use the `OpenAI` client class and `client.chat.completions.create(...)`.
# Fall back to the legacy `openai.ChatCompletion.create(...)` if needed.
try:
    # Preferred modern interface (openai>=1.0.0)
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful test assistant that responds briefly."},
            {"role": "user", "content": "Say hello to Hakan in one short sentence."},
        ],
        max_tokens=60,
        n=1,
        temperature=0.0,
    )

    # Try to access the content in a robust way
    choice = None
    try:
        choice = response.choices[0].message.content.strip()
    except Exception:
        try:
            choice = response.choices[0]["message"]["content"].strip()
        except Exception:
            choice = str(response)

    print("OpenAI response:\n", choice)

except Exception as e:
    # Fallback for older openai versions (<1.0.0)
    try:
        import openai
        openai.api_key = OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful test assistant that responds briefly."},
                {"role": "user", "content": "Say hello to Hakan in one short sentence."},
            ],
            max_tokens=60,
            n=1,
            temperature=0.0,
        )
        try:
            choice = response.choices[0].message.content.strip()
        except Exception:
            choice = str(response)
        print("OpenAI response:\n", choice)
    except Exception as e2:
        print('OpenAI API call failed ->', e2)
        sys.exit(1)
