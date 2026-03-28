from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Footer, Header, Input, Static

from .agent import ask_model
from .executor import execute_action
from .formatters import format_result


class CommandAgentApp(App):
    CSS = """
    Screen {
        background: #0b0f10;
        color: #d7e0ea;
    }

    #main_container {
        height: 100%;
        padding: 1 2;
    }

    #title {
        content-align: center middle;
        padding-bottom: 1;
        text-style: bold;
    }

    #help_text {
        padding-bottom: 1;
        color: #9fb3c8;
    }

    #output_box {
        height: 1fr;
        border: round #3a4a5a;
        padding: 1;
        background: #11161b;
        overflow-y: auto;
    }

    #input_box {
        margin-top: 1;
        border: round #3a4a5a;
        background: #11161b;
    }
    """

    BINDINGS = [("ctrl+c", "quit", "Sair")]

    def __init__(self) -> None:
        super().__init__()
        self.history_text = "Pronto.\n"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main_container"):
            with Vertical():
                yield Static("Command Agent v2", id="title")
                yield Static(
                    "Digite um comando em linguagem natural e pressione Enter.\n"
                    "Ex.: quem sou eu no sistema | mostre o hostname | liste os txt permitidos",
                    id="help_text",
                )
                yield Static(self.history_text, id="output_box")
                yield Input(placeholder="Digite sua instrucao...", id="input_box")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value.strip()
        if not user_text:
            return

        output_box = self.query_one("#output_box", Static)
        input_box = self.query_one("#input_box", Input)

        try:
            parsed = ask_model(user_text)
            action = parsed.get("action", "unsupported")
            arguments = parsed.get("arguments", {})

            if not action or action == "unsupported":
                result_text = "Comando nao suportado pelo agente."
            else:
                result = execute_action(action, arguments)
                result_text = format_result(result)
        except Exception as exc:
            result_text = f"Erro interno:\n{exc}"

        self.history_text += f"\n> {user_text}\n\n{result_text}\n\n{'-' * 70}\n"
        output_box.update(self.history_text)
        input_box.value = ""


def run() -> None:
    CommandAgentApp().run()


if __name__ == "__main__":
    run()

