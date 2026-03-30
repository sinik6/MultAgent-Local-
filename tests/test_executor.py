from pathlib import Path

from command_agent import executor


def test_is_safe_path_accepts_file_inside_safe_root(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(executor, "SAFE_ROOTS", [tmp_path.resolve()])
    inside_file = tmp_path / "sample.txt"
    inside_file.write_text("ok", encoding="utf-8")

    assert executor.is_safe_path(str(inside_file)) is True


def test_is_safe_path_rejects_path_outside_safe_root(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(executor, "SAFE_ROOTS", [tmp_path.resolve()])
    outside_file = tmp_path.parent / "outside.txt"
    outside_file.write_text("no", encoding="utf-8")

    assert executor.is_safe_path(str(outside_file)) is False


def test_create_and_read_text_file(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(executor, "SAFE_ROOTS", [tmp_path.resolve()])
    monkeypatch.setattr(executor, "DEFAULT_TEXT_DIR", tmp_path.resolve())
    monkeypatch.setattr(executor, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(executor, "OUTPUTS_DIR", tmp_path / "outputs")
    executor.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    executor.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    created = executor.execute_action(
        "create_text_file",
        {"path": str(tmp_path), "filename": "note.txt", "content": "conteudo"},
    )
    read = executor.execute_action("read_text_file", {"path": str(tmp_path / "note.txt")})

    assert created["ok"] is True
    assert read["ok"] is True
    assert read["output"] == "conteudo"


def test_list_files_in_path_inside_safe_root(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(executor, "SAFE_ROOTS", [tmp_path.resolve()])
    monkeypatch.setattr(executor, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(executor, "OUTPUTS_DIR", tmp_path / "outputs")
    executor.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    executor.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")

    listed = executor.execute_action("list_files_in_path", {"path": str(tmp_path)})

    assert listed["ok"] is True
    assert "a.txt" in listed["output"]
    assert "b.txt" in listed["output"]


def test_run_safe_command_returns_structured_output():
    result = executor.execute_action("run_safe_command", {"command": "hostname"})

    assert result["action"] == "run_safe_command"
    assert isinstance(result["output"], dict)
    assert "stdout" in result["output"]
    assert "returncode" in result["output"]
