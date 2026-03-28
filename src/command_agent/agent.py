from __future__ import annotations

import json
import sys

import ollama

from .config import OLLAMA_MODEL
from .executor import execute_action
from .prompts import SYSTEM_PROMPT


def ask_model(text: str) -> dict:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        options={"temperature": 0},
    )

    try:
        return json.loads(response["message"]["content"])
    except (KeyError, TypeError, json.JSONDecodeError):
        return {"action": "unsupported", "arguments": {}}


def main() -> None:
    text = " ".join(sys.argv[1:]).strip()
    if not text:
        print("Uso: python -m command_agent \"sua instrucao\"")
        raise SystemExit(1)

    parsed = ask_model(text)
    if parsed.get("action") == "unsupported":
        print("nao suportado")
        return

    result = execute_action(parsed["action"], parsed.get("arguments", {}))
    print(json.dumps(result, indent=2, ensure_ascii=False))

