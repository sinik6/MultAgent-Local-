# MultAgent-Local

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111111)](https://ollama.com/)
[![Textual](https://img.shields.io/badge/UI-Textual-5E5CE6)](https://textual.textualize.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

Agente local para comandos em linguagem natural com interface terminal, regras claras e execucao restrita.

## Highlights

- CLI e interface Textual
- integracao com Ollama
- leitura e criacao segura de `.txt`
- whitelist de comandos do sistema
- logs e outputs fora do Git
- estrutura pronta para publicar no GitHub

## Preview

```text
+--------------------------------------------------------------+
| Command Agent v2                                             |
| Digite um comando em linguagem natural e pressione Enter     |
|--------------------------------------------------------------|
| > mostre o hostname                                          |
|                                                              |
| Status: OK                                                   |
| Acao: run_safe_command                                       |
|                                                              |
| Saida:                                                       |
| - comando: hostname                                          |
| - returncode: 0                                              |
|                                                              |
| [stdout]                                                     |
| MEU-PC                                                       |
+--------------------------------------------------------------+
```

## Instalacao

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull qwen2.5-coder:7b
```

## Uso

### CLI

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python run_cli.py "mostre o hostname"
```

### Interface

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python run_app.py
```

## Configuracao

O projeto usa variaveis de ambiente. Veja `.env.example`.

Principais opcoes:

- `COMMAND_AGENT_MODEL`
- `COMMAND_AGENT_SAFE_ROOTS`
- `COMMAND_AGENT_DEFAULT_TEXT_DIR`
- `COMMAND_AGENT_ALLOWED_COMMANDS`
- `COMMAND_AGENT_DATA_DIR`
- `COMMAND_AGENT_COMMAND_TIMEOUT`

Exemplo minimo:

```powershell
$env:COMMAND_AGENT_SAFE_ROOTS = (Resolve-Path .).Path
$env:COMMAND_AGENT_DEFAULT_TEXT_DIR = (Resolve-Path .).Path
```

## Acoes suportadas

- `list_txt_desktop`
- `list_files_in_path`
- `create_text_file`
- `read_text_file`
- `show_current_dir`
- `pwd`
- `run_safe_command`

Comandos liberados por padrao:

- `whoami`
- `hostname`
- `ipconfig`
- `tasklist`

## Exemplos

```powershell
python run_cli.py "mostre o diretorio atual"
python run_cli.py "liste os arquivos da pasta atual"
python run_cli.py "crie um arquivo chamado nota.txt com o conteudo teste"
python run_cli.py "leia o arquivo nota.txt"
```

## Seguranca

- aceita apenas acoes conhecidas
- executa apenas comandos em whitelist
- limita leitura e escrita a caminhos permitidos
- trabalha apenas com arquivos `.txt`
- salva artefatos locais em `.localdata/`

## Testes

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m pytest -q
```

## Estrutura

```text
src/command_agent/
tests/
run_app.py
run_cli.py
requirements.txt
pyproject.toml
```

## Licenca

[MIT](./LICENSE)
