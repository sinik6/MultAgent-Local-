# MultAgent-Local

## Command Agent v2

Versao organizada para publicacao no GitHub do agente local com Ollama e Textual.

## O que mudou

- remove caminhos absolutos da maquina do autor
- move logs e saidas para `.localdata/`, que fica ignorado no Git
- usa configuracao por variaveis de ambiente com defaults seguros
- limita leitura/escrita a pastas explicitamente permitidas
- preserva o projeto original intacto; esta pasta e a segunda versao

## Estrutura

```text
command_agent_v2/
  src/command_agent/
  tests/
  .env.example
  .gitignore
  pyproject.toml
  requirements.txt
  README.md
```

## Requisitos

- Python 3.11+
- Ollama rodando localmente

## Instalacao

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuracao

Copie `.env.example` para `.env` se quiser customizar. O projeto nao depende de bibliotecas de dotenv; o arquivo serve como referencia.

Variaveis principais:

- `COMMAND_AGENT_MODEL`: modelo usado no Ollama
- `COMMAND_AGENT_SAFE_ROOTS`: lista de pastas permitidas, separadas por `;` ou `,`
- `COMMAND_AGENT_DEFAULT_TEXT_DIR`: pasta padrao para a acao `list_txt_desktop` por compatibilidade
- `COMMAND_AGENT_DATA_DIR`: onde logs e saidas serao gravados

Exemplo seguro para uso local no proprio projeto:

```powershell
$env:COMMAND_AGENT_SAFE_ROOTS = (Resolve-Path .).Path
$env:COMMAND_AGENT_DEFAULT_TEXT_DIR = (Resolve-Path .).Path
```

## Uso

CLI:

```powershell
python -m command_agent "mostre o hostname"
```

Interface Textual:

```powershell
python -m command_agent.app
```

## Publicacao no GitHub

Publique somente esta pasta `command_agent_v2/`. A raiz antiga do workspace contem ambientes virtuais, logs e artefatos locais que nao devem subir para o repositrio.
