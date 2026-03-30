from __future__ import annotations

import json
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = PROJECT_ROOT.parents[2] if len(PROJECT_ROOT.parents) >= 3 else PROJECT_ROOT
HOME_DIR = Path.home()
DESKTOP_DIR = HOME_DIR / "Desktop"
DEFAULT_DATA_DIR = PROJECT_ROOT / ".localdata"
CONFIG_FILE_WARNING = ""


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


def _load_file_config() -> dict:
    global CONFIG_FILE_WARNING

    candidates: list[Path] = []
    env_path = os.getenv("COMMAND_AGENT_CONFIG")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    for base in [Path.cwd(), PROJECT_ROOT]:
        candidates.extend(
            [
                base / ".command_agent.json",
                base / "command_agent.json",
            ]
        )

    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        try:
            return json.loads(resolved.read_text(encoding="utf-8"))
        except Exception as exc:
            CONFIG_FILE_WARNING = f"Falha ao ler configuracao em {resolved.name}: {exc}"
            return {}
    return {}


FILE_CONFIG = _load_file_config()


def _get_config_value(env_var: str, file_key: str, default):
    env_value = os.getenv(env_var)
    if env_value not in (None, ""):
        return env_value
    return FILE_CONFIG.get(file_key, default)


def _resolve_safe_roots() -> list[Path]:
    configured = _get_config_value("COMMAND_AGENT_SAFE_ROOTS", "safe_roots", None)

    if isinstance(configured, list):
        roots = [_resolve_directory(item, PROJECT_ROOT) for item in configured]
    else:
        roots = [_resolve_directory(item, PROJECT_ROOT) for item in _split_paths(configured)]

    if not roots:
        roots = [WORKSPACE_ROOT]
        if DESKTOP_DIR.exists():
            roots.append(DESKTOP_DIR.resolve())

    unique_roots: list[Path] = []
    for root in roots:
        if root not in unique_roots:
            unique_roots.append(root)
    return unique_roots


def _resolve_default_text_dir(safe_roots: list[Path]) -> Path:
    raw_value = _get_config_value("COMMAND_AGENT_DEFAULT_TEXT_DIR", "default_text_dir", None)
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
    configured = _get_config_value(
        "COMMAND_AGENT_ALLOWED_COMMANDS",
        "allowed_commands",
        "whoami,hostname,ipconfig,tasklist",
    )

    if isinstance(configured, list):
        allowed = {item.strip().lower() for item in configured if str(item).strip()}
    else:
        allowed = {
            item.strip().lower()
            for item in str(configured).replace(";", ",").split(",")
            if item.strip()
        }
    return {name: command for name, command in base_commands.items() if name in allowed}


OLLAMA_MODEL = str(_get_config_value("COMMAND_AGENT_MODEL", "model", "qwen2.5-coder:7b")).strip() or "qwen2.5-coder:7b"
DATA_DIR = _resolve_directory(_get_config_value("COMMAND_AGENT_DATA_DIR", "data_dir", None), DEFAULT_DATA_DIR)
LOGS_DIR = DATA_DIR / "logs"
OUTPUTS_DIR = DATA_DIR / "outputs"
SAFE_ROOTS = _resolve_safe_roots()
DEFAULT_TEXT_DIR = _resolve_default_text_dir(SAFE_ROOTS)
SAFE_COMMANDS = _resolve_allowed_commands()
COMMAND_TIMEOUT_SECONDS = int(_get_config_value("COMMAND_AGENT_COMMAND_TIMEOUT", "command_timeout", 30))

LOGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def describe_runtime() -> dict:
    return {
        "model": OLLAMA_MODEL,
        "safe_roots": [str(path) for path in SAFE_ROOTS],
        "default_text_dir": str(DEFAULT_TEXT_DIR),
        "allowed_commands": sorted(SAFE_COMMANDS.keys()),
        "data_dir": str(DATA_DIR),
        "command_timeout": COMMAND_TIMEOUT_SECONDS,
        "config_warning": CONFIG_FILE_WARNING,
    }
