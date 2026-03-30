import importlib
import json
import sys
from pathlib import Path


def test_loads_json_config(monkeypatch, tmp_path: Path):
    config_file = tmp_path / ".command_agent.json"
    config_file.write_text(
        json.dumps(
            {
                "model": "qwen2.5-coder:7b",
                "safe_roots": [str(tmp_path)],
                "default_text_dir": str(tmp_path),
                "allowed_commands": ["hostname"],
                "command_timeout": 12,
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("COMMAND_AGENT_CONFIG", str(config_file))
    sys.modules.pop("command_agent.config", None)
    config = importlib.import_module("command_agent.config")
    config = importlib.reload(config)

    assert config.OLLAMA_MODEL == "qwen2.5-coder:7b"
    assert config.SAFE_ROOTS == [tmp_path.resolve()]
    assert config.DEFAULT_TEXT_DIR == tmp_path.resolve()
    assert list(config.SAFE_COMMANDS.keys()) == ["hostname"]
    assert config.COMMAND_TIMEOUT_SECONDS == 12
