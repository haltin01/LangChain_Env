"""Simple smoke test that uses LangChain (preferred) and falls back to OpenAI SDK.

It requires OPENAI_API_KEY to be set in the environment.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

PROMPT = "Say exactly: smoke test OK"


def run_test():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("ERROR: OPENAI_API_KEY is not set. Set it and re-run the test.")
        return 2

    # Try LangChain first
    try:
        from langchain.chat_models import ChatOpenAI
        from langchain.schema import HumanMessage

        print("Using LangChain.ChatOpenAI...")
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        resp = llm.predict_messages([HumanMessage(content=PROMPT)])
        text = resp.content.strip()
        print("Response:", text)
    except Exception as e:
        print("LangChain failed or not available, falling back to openai SDK. Error:", e)
        import openai

        openai.api_key = key
        resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": PROMPT}])
        text = resp.choices[0].message.content.strip()
        print("Response:", text)

    if "smoke test OK" in text.lower():
        print("SMOKE TEST OK ✅")
        return 0
    else:
        print("SMOKE TEST FAILED ❌")
        return 1


if __name__ == "__main__":
    code = run_test()
    sys.exit(code)
