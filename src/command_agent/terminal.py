from __future__ import annotations

import ctypes
import itertools
import os
import sys
import threading

from .agent import process_instruction
from .config import describe_runtime
from .formatters import format_result


SEPARATOR = "=" * 72

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

USER = "\033[96m"
LLM = "\033[38;5;224m"
LOAD = "\033[38;5;151m"
ACCENT = "\033[38;5;183m"
MUTED = "\033[38;5;247m"
LINE = "\033[38;5;111m"
OK = "\033[38;5;151m"
ERR = "\033[38;5;217m"


def enable_ansi() -> None:
    if os.name != "nt":
        return
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        pass


def clear_screen() -> None:
    os.system("cls")


def styled(text: str, *styles: str) -> str:
    return "".join(styles) + text + RESET


def build_history_preview(history: list[str], limit: int = 8) -> str:
    if not history:
        return "(sem historico)"
    start = max(0, len(history) - limit)
    return "\n".join(f"{index + 1}. {item}" for index, item in enumerate(history[start:], start=start))


def print_header() -> None:
    print(styled("Digite uma instrucao em linguagem natural.", BOLD))
    print(styled("Comandos da sessao: /help  /clear  /exit  /model  /roots  /commands  /history", MUTED))
    print("")
    print(styled("Exemplos:", ACCENT, BOLD))
    print("- mostre o hostname")
    print("- quem sou eu no sistema")
    print("- liste os arquivos da pasta atual")
    print("- leia o arquivo teste.txt")
    print(styled(SEPARATOR, LINE))


def print_help() -> None:
    print("")
    print(styled("Ajuda rapida", ACCENT, BOLD))
    print("- /help     : mostra esta ajuda")
    print("- /clear    : limpa o terminal")
    print("- /exit     : encerra a sessao")
    print("- /model    : mostra o modelo atual")
    print("- /roots    : mostra as pastas seguras")
    print("- /commands : mostra os comandos permitidos")
    print("- /history  : mostra o historico da sessao")
    print(styled(SEPARATOR, LINE))


def run_with_spinner(func, *args, **kwargs):
    done = threading.Event()
    result = {"value": None, "error": None}

    def target():
        try:
            result["value"] = func(*args, **kwargs)
        except Exception as exc:
            result["error"] = exc
        finally:
            done.set()

    threading.Thread(target=target, daemon=True).start()

    frames = [
        "llm  thinking",
        "llm  thinking.",
        "llm  thinking..",
        "llm  thinking...",
        "llm  thinking   .",
        "llm  thinking  ..",
        "llm  thinking ...",
    ]

    for frame in itertools.cycle(frames):
        if done.wait(0.15):
            break
        sys.stdout.write("\r" + styled(frame, LOAD, BOLD))
        sys.stdout.flush()

    sys.stdout.write("\r" + (" " * 32) + "\r")
    sys.stdout.flush()

    if result["error"] is not None:
        raise result["error"]
    return result["value"]


def print_result(result_text: str) -> None:
    lines = result_text.splitlines()
    print(styled("llm", LLM, BOLD))
    for line in lines:
        if line.startswith("Status: OK"):
            print(styled(line, OK, BOLD))
        elif line.startswith("Status: ERRO"):
            print(styled(line, ERR, BOLD))
        elif line.startswith("Modo:"):
            print(styled(line, ACCENT, BOLD))
        elif line in {"Argumentos:", "Saida:", "Erro:"}:
            print(styled(line, LLM, BOLD))
        else:
            print(line)
    print(styled(SEPARATOR, LINE))


def handle_session_command(user_text: str, history: list[str]) -> bool:
    runtime = describe_runtime()
    command = user_text.lower()

    if command == "/exit":
        print("\nSessao encerrada.")
        return True

    if command == "/clear":
        clear_screen()
        print_header()
        return False

    if command == "/help":
        print_help()
        return False

    if command == "/model":
        print("")
        print(styled("modelo atual", ACCENT, BOLD))
        print(runtime["model"])
        print(styled(SEPARATOR, LINE))
        return False

    if command == "/roots":
        print("")
        print(styled("pastas seguras", ACCENT, BOLD))
        for root in runtime["safe_roots"]:
            print(f"- {root}")
        print(styled(SEPARATOR, LINE))
        return False

    if command == "/commands":
        print("")
        print(styled("comandos permitidos", ACCENT, BOLD))
        for name in runtime["allowed_commands"]:
            print(f"- {name}")
        print(styled(SEPARATOR, LINE))
        return False

    if command == "/history":
        print("")
        print(styled("historico da sessao", ACCENT, BOLD))
        print(build_history_preview(history))
        print(styled(SEPARATOR, LINE))
        return False

    return None


def run_terminal() -> None:
    enable_ansi()
    clear_screen()
    print_header()

    runtime = describe_runtime()
    if runtime["config_warning"]:
        print(styled(runtime["config_warning"], ERR, BOLD))
        print(styled(SEPARATOR, LINE))

    history: list[str] = []

    while True:
        try:
            user_text = input(styled("\n> ", USER, BOLD)).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSessao encerrada.")
            break

        if not user_text:
            continue

        session_result = handle_session_command(user_text, history)
        if session_result is True:
            break
        if session_result is False:
            continue

        history.append(user_text)
        print(styled("usuario", USER, BOLD))
        print(user_text)
        print("")

        try:
            result = run_with_spinner(process_instruction, user_text)
            result_text = format_result(result)
        except Exception as exc:
            result_text = f"Erro interno:\n{exc}"

        print("")
        print_result(result_text)
