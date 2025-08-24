import os, ast
from dotenv import load_dotenv
from openai import OpenAI
from poml import poml

load_dotenv()  # reads .env if present

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise SystemExit("Missing OPENAI_API_KEY (set in .env or environment)")

MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=API_KEY)

# 1) Render POML. chat=True requests chat-style output from the renderer.
rendered = poml("example.poml", chat=True)

# 2) VS Code–style normalization: accept dict/list/str; produce [{role, content}]
def to_openai_messages(x):
    if isinstance(x, dict) and "messages" in x:
        x = x["messages"]
    if isinstance(x, list):
        out = []
        for it in x:
            if isinstance(it, dict) and "role" in it and "content" in it:
                out.append({"role": it["role"], "content": it["content"]})
            elif isinstance(it, str):
                try:
                    d = ast.literal_eval(it)
                    if isinstance(d, dict) and "speaker" in d and "content" in d:
                        role = {
                            "human": "user",
                            "user": "user",
                            "assistant": "assistant",
                            "ai": "assistant",
                            "system": "system",
                        }.get(str(d["speaker"]).lower(), "user")
                        out.append({"role": role, "content": d["content"]})
                    else:
                        out.append({"role": "user", "content": it})
                except Exception:
                    out.append({"role": "user", "content": it})
            else:
                out.append({"role": "user", "content": str(it)})
        return out
    if isinstance(x, str):
        try:
            d = ast.literal_eval(x)
            if isinstance(d, dict) and "speaker" in d and "content" in d:
                role = {
                    "human": "user",
                    "user": "user",
                    "assistant": "assistant",
                    "ai": "assistant",
                    "system": "system",
                }.get(str(d["speaker"]).lower(), "user")
                return [{"role": role, "content": d["content"]}]
        except Exception:
            pass
        return [{"role": "user", "content": x}]
    return [{"role": "user", "content": str(x)}]

messages = to_openai_messages(rendered)

resp = client.chat.completions.create(model=MODEL, messages=messages)
print(resp.choices[0].message.content)
