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


def process_instruction(text: str) -> dict:
    parsed = ask_model(text)
    if parsed.get("action") == "unsupported":
        return {
            "ok": False,
            "action": "unsupported",
            "arguments": {},
            "output": None,
            "error": "Comando nao suportado pelo agente.",
        }
    return execute_action(parsed["action"], parsed.get("arguments", {}))


def main() -> None:
    text = " ".join(sys.argv[1:]).strip()
    if not text:
        from .terminal import run_terminal

        run_terminal()
        return

    result = process_instruction(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))

