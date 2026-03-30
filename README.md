# MultAgent-Local

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111111)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

Agente local para comandos em linguagem natural com foco em terminal, execucao restrita e configuracao segura.

## Highlights

- modo terminal leve para Windows
- integracao com Ollama
- leitura e criacao segura de arquivos `.txt`
- comandos do sistema via whitelist
- configuracao por env vars ou arquivo JSON
- logs e saidas fora do Git

## Como rodar

Instalacao:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull qwen2.5-coder:7b
```

Modo interativo:

```powershell
python run_app.py
```

Atalhos para Windows:

```powershell
.\run.bat
```

ou

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

Modo direto:

```powershell
python run_cli.py "mostre o hostname"
```

## Comandos da sessao

- `/help`
- `/clear`
- `/exit`
- `/model`
- `/roots`
- `/commands`
- `/history`

## Exemplo de terminal

```text
Digite uma instrucao em linguagem natural.
Comandos da sessao: /help /clear /exit /model /roots /commands /history

Exemplos:
- mostre o hostname
- liste os arquivos da pasta atual
- leia um arquivo txt permitido
========================================================================

> mostre o hostname
usuario
mostre o hostname

llm  thinking...

llm
Status: OK
Modo: run_safe_command

Argumentos:
- command: hostname

Saida:
- comando: hostname
- returncode: 0
```

## Configuracao

O projeto aceita configuracao por variaveis de ambiente ou por um dos arquivos:

- `.command_agent.json`
- `command_agent.json`

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

Exemplo de arquivo JSON:

```json
{
  "model": "qwen2.5-coder:7b",
  "safe_roots": ["."],
  "default_text_dir": ".",
  "allowed_commands": ["whoami", "hostname"],
  "data_dir": ".localdata",
  "command_timeout": 30
}
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

## Seguranca

- aceita apenas acoes conhecidas
- executa apenas comandos em whitelist
- limita leitura e escrita a caminhos permitidos
- trabalha apenas com arquivos `.txt`
- salva artefatos locais em `.localdata/`

## Testes

```powershell
python -m pytest -q
```

## Estrutura

```text
src/command_agent/
tests/
run_app.py
run_cli.py
run.bat
run.ps1
requirements.txt
pyproject.toml
```

## Licenca

[MIT](./LICENSE)
