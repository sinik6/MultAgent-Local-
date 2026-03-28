from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = PROJECT_ROOT.parents[2] if len(PROJECT_ROOT.parents) >= 3 else PROJECT_ROOT
HOME_DIR = Path.home()
DESKTOP_DIR = HOME_DIR / "Desktop"
DEFAULT_DATA_DIR = PROJECT_ROOT / ".localdata"


def _split_paths(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    normalized = raw_value.replace(";", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def _resolve_directory(raw_value: str | Path, fallback: Path) -> Path:
    candidate = Path(raw_value).expanduser() if raw_value else fallback
    if not candidate.is_absolute():
        candidate = (PROJECT_ROOT / candidate).resolve()
    return candidate.resolve()


def _resolve_safe_roots() -> list[Path]:
    configured = _split_paths(os.getenv("COMMAND_AGENT_SAFE_ROOTS"))
    if configured:
        roots = [_resolve_directory(item, PROJECT_ROOT) for item in configured]
    else:
        roots = [WORKSPACE_ROOT]
        if DESKTOP_DIR.exists():
            roots.append(DESKTOP_DIR.resolve())
    unique_roots: list[Path] = []
    for root in roots:
        if root not in unique_roots:
            unique_roots.append(root)
    return unique_roots


def _resolve_default_text_dir(safe_roots: list[Path]) -> Path:
    raw_value = os.getenv("COMMAND_AGENT_DEFAULT_TEXT_DIR")
    if not raw_value and DESKTOP_DIR.exists():
        raw_value = str(DESKTOP_DIR)
    candidate = _resolve_directory(raw_value, safe_roots[0])
    for safe_root in safe_roots:
        if candidate.is_relative_to(safe_root):
            return candidate
    return safe_roots[0]


def _resolve_allowed_commands() -> dict[str, list[str]]:
    base_commands = {
        "whoami": ["whoami"],
        "hostname": ["hostname"],
        "ipconfig": ["ipconfig"],
        "tasklist": ["tasklist"],
    }
    allowed = set(
        item.strip().lower()
        for item in os.getenv("COMMAND_AGENT_ALLOWED_COMMANDS", "whoami,hostname,ipconfig,tasklist").replace(";", ",").split(",")
        if item.strip()
    )
    return {name: command for name, command in base_commands.items() if name in allowed}


OLLAMA_MODEL = os.getenv("COMMAND_AGENT_MODEL", "qwen2.5-coder:7b").strip() or "qwen2.5-coder:7b"
DATA_DIR = _resolve_directory(os.getenv("COMMAND_AGENT_DATA_DIR"), DEFAULT_DATA_DIR)
LOGS_DIR = DATA_DIR / "logs"
OUTPUTS_DIR = DATA_DIR / "outputs"
SAFE_ROOTS = _resolve_safe_roots()
DEFAULT_TEXT_DIR = _resolve_default_text_dir(SAFE_ROOTS)
SAFE_COMMANDS = _resolve_allowed_commands()
COMMAND_TIMEOUT_SECONDS = int(os.getenv("COMMAND_AGENT_COMMAND_TIMEOUT", "30"))

LOGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
