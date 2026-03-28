from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

from .config import COMMAND_TIMEOUT_SECONDS, DEFAULT_TEXT_DIR, LOGS_DIR, OUTPUTS_DIR, SAFE_COMMANDS, SAFE_ROOTS


def is_safe_path(path_str: str | None) -> bool:
    if not path_str:
        return False
    try:
        target = Path(path_str).expanduser().resolve()
    except OSError:
        return False
    return any(target.is_relative_to(root) for root in SAFE_ROOTS)


def _ensure_safe_directory(path_str: str | None) -> Path:
    if not is_safe_path(path_str):
        raise ValueError("Caminho nao permitido")
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError("Diretorio nao encontrado")
    if not path.is_dir():
        raise NotADirectoryError("O caminho informado nao e um diretorio")
    return path


def _ensure_safe_text_file(path_str: str | None) -> Path:
    if not is_safe_path(path_str):
        raise ValueError("Caminho nao permitido")
    path = Path(path_str).expanduser().resolve()
    if path.suffix.lower() != ".txt":
        raise ValueError("Somente arquivos .txt")
    if not path.exists():
        raise FileNotFoundError("Arquivo nao encontrado")
    if not path.is_file():
        raise FileNotFoundError("Arquivo invalido")
    return path


def _sanitize_filename(filename: str | None) -> str:
    if not filename:
        raise ValueError("filename e obrigatorio")
    clean_name = Path(filename).name
    if clean_name != filename:
        raise ValueError("filename deve conter apenas o nome do arquivo")
    if Path(clean_name).suffix.lower() != ".txt":
        raise ValueError("Somente arquivos .txt")
    return clean_name


def write_log(data: dict) -> None:
    file_path = LOGS_DIR / f"log_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with file_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")


def save_output(result: dict) -> None:
    file_path = OUTPUTS_DIR / f"out_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)


def execute_action(action: str, arguments: dict | None) -> dict:
    arguments = arguments or {}
    result = {"ok": False, "action": action, "arguments": arguments, "output": None, "error": None}

    try:
        if action == "list_txt_desktop":
            result["output"] = sorted(file.name for file in DEFAULT_TEXT_DIR.glob("*.txt"))
            result["ok"] = True

        elif action == "list_files_in_path":
            path = _ensure_safe_directory(arguments.get("path"))
            result["output"] = sorted(file.name for file in path.iterdir())
            result["ok"] = True

        elif action == "create_text_file":
            directory = _ensure_safe_directory(arguments.get("path"))
            filename = _sanitize_filename(arguments.get("filename"))
            content = arguments.get("content", "")

            file_path = directory / filename
            file_path.write_text(str(content), encoding="utf-8")
            result["output"] = str(file_path)
            result["ok"] = True

        elif action == "read_text_file":
            file_path = _ensure_safe_text_file(arguments.get("path"))
            result["output"] = file_path.read_text(encoding="utf-8")
            result["ok"] = True

        elif action in ["pwd", "show_current_dir"]:
            result["output"] = str(Path.cwd())
            result["ok"] = True

        elif action == "run_safe_command":
            command_name = str(arguments.get("command", "")).strip().lower()
            if command_name not in SAFE_COMMANDS:
                raise ValueError("Comando nao permitido")

            command = SAFE_COMMANDS[command_name]
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=COMMAND_TIMEOUT_SECONDS,
                check=False,
            )
            result["output"] = {
                "command": " ".join(command),
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
                "returncode": completed.returncode,
            }
            result["ok"] = completed.returncode == 0
            if completed.returncode != 0 and not result["error"]:
                result["error"] = "Comando executado com erro"

        else:
            raise ValueError("Acao invalida")

    except Exception as exc:
        result["error"] = str(exc)

    write_log(result)
    save_output(result)
    return result

