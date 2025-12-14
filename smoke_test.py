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
    text = None
    # Make LangChain import robust across versions and try multiple known import paths.
    llm = None
    human_message_cls = None
    try_imports = [
        ("langchain.chat_models", "ChatOpenAI"),
        ("langchain.chat_models.openai", "ChatOpenAI"),
        ("langchain.llms", "OpenAI"),
    ]

    for module_name, cls_name in try_imports:
        try:
            module = __import__(module_name, fromlist=[cls_name])
            cls = getattr(module, cls_name)
            print(f"Using {module_name}.{cls_name} for LangChain")
            # instantiate with chat-like params where possible
            try:
                llm = cls(temperature=0, model_name="gpt-3.5-turbo")
            except TypeError:
                try:
                    llm = cls(temperature=0)
                except Exception:
                    llm = cls()

            # human message class for predict_messages
            try:
                from langchain.schema import HumanMessage

                human_message_cls = HumanMessage
            except Exception:
                human_message_cls = None

            break
        except Exception:
            continue

    if llm is not None:
        try:
            # Prefer chat-style interface if available
            if human_message_cls and hasattr(llm, "predict_messages"):
                resp = llm.predict_messages([human_message_cls(content=PROMPT)])
                # Many LangChain responses have .content
                text = getattr(resp, "content", None) or str(resp)
            elif hasattr(llm, "predict"):
                text = llm.predict(PROMPT)
            else:
                # fallback to calling the object
                text = llm(PROMPT)

            text = text.strip() if isinstance(text, str) else str(text).strip()
            print("Response (LangChain):", text)
        except Exception as e:
            print("LangChain invocation failed, falling back to OpenAI SDK. Error:", e)

    if not text:
        # fallback to OpenAI SDK
        print("Falling back to OpenAI SDK...")
        try:
            from openai import OpenAI

            client = OpenAI()
            resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": PROMPT}])

            # Response shape may vary; handle object or dict
            message = resp.choices[0].message
            if hasattr(message, "content"):
                text = message.content.strip()
            elif isinstance(message, dict):
                text = message.get("content", "").strip()
            else:
                text = str(message).strip()

            print("Response (OpenAI SDK):", text)
        except Exception as e2:
            print("OpenAI SDK failed:", e2)
            raise

    if "smoke test ok" in text.lower():
        print("SMOKE TEST OK ✅")
        return 0
    else:
        print("SMOKE TEST FAILED ❌")
        return 1


if __name__ == "__main__":
    code = run_test()
    sys.exit(code)
