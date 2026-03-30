from command_agent.terminal import build_history_preview, handle_session_command


def test_history_preview_limits_items():
    history = [f"item {index}" for index in range(12)]
    preview = build_history_preview(history, limit=3)

    assert "10. item 9" in preview
    assert "12. item 11" in preview
    assert "1. item 0" not in preview


def test_handle_session_command_returns_exit_for_exit():
    assert handle_session_command("/exit", []) is True
