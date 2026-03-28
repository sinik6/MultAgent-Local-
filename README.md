# MultAgent-Local

## Command Agent v2

Um agente local com interface terminal bonita, execucao restrita e foco em seguranca pratica.

Ele interpreta instrucoes em linguagem natural, transforma isso em acoes controladas e executa apenas operacoes permitidas no seu computador. A ideia aqui nao e "dar acesso total para a IA". E o contrario: dar utilidade real com limites claros.

---

## Visao Geral

O `Command Agent v2` foi reorganizado para ficar pronto para GitHub, mais facil de entender, mais seguro para compartilhar e mais simples de rodar em outra maquina.

### O que ele faz

- entende comandos em linguagem natural via Ollama
- executa acoes locais restritas e auditaveis
- oferece modo CLI e interface Textual
- grava logs e saidas locais fora do versionamento
- limita operacoes a pastas e comandos explicitamente permitidos

### O que ele nao faz

- nao executa qualquer comando arbitrario
- nao varre o sistema inteiro sem restricao
- nao expoe segredos no codigo
- nao depende de caminhos absolutos da maquina do autor

---

## Destaques

- Estrutura limpa para publicacao
- Configuracao por variaveis de ambiente
- Logs e resultados em `.localdata/`
- Whitelist de comandos do sistema
- Leitura e criacao apenas de arquivos `.txt`
- Testes automatizados do executor
- Projeto original preservado, sem quebrar o fluxo que ja funcionava

---

## Estrutura do Projeto

```text
command_agent_v2/
  src/
    command_agent/
      agent.py
      app.py
      config.py
      executor.py
      formatters.py
      prompts.py
  tests/
    test_executor.py
  .env.example
  .gitignore
  pyproject.toml
  requirements.txt
  run_app.py
  run_cli.py
  README.md
```

### Arquivos principais

- `src/command_agent/agent.py`: conversa com o modelo e resolve a acao
- `src/command_agent/executor.py`: aplica as regras de seguranca e executa a acao
- `src/command_agent/config.py`: concentra configuracao, diretivos seguros e pastas permitidas
- `src/command_agent/app.py`: interface terminal com Textual
- `tests/test_executor.py`: testes do nucleo de execucao

---

## Requisitos

- Python 3.11+
- [Ollama](https://ollama.com/) instalado e rodando
- um modelo local disponivel, por exemplo `qwen2.5-coder:7b`

---

## Instalacao Rapida

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se ainda nao tiver o modelo no Ollama:

```powershell
ollama pull qwen2.5-coder:7b
```

---

## Configuracao

O projeto usa variaveis de ambiente. O arquivo [`.env.example`](C:\Users\Administrator\agentes\projects\agents\command_agent_v2\.env.example) serve como referencia.

### Variaveis principais

- `COMMAND_AGENT_MODEL`: modelo usado pelo Ollama
- `COMMAND_AGENT_SAFE_ROOTS`: pastas permitidas para leitura e criacao
- `COMMAND_AGENT_DEFAULT_TEXT_DIR`: pasta padrao da acao `list_txt_desktop`
- `COMMAND_AGENT_ALLOWED_COMMANDS`: comandos de sistema liberados
- `COMMAND_AGENT_DATA_DIR`: onde ficam logs e saidas
- `COMMAND_AGENT_COMMAND_TIMEOUT`: timeout dos comandos permitidos

### Exemplo de configuracao segura

Permitir somente a pasta atual:

```powershell
$env:COMMAND_AGENT_SAFE_ROOTS = (Resolve-Path .).Path
$env:COMMAND_AGENT_DEFAULT_TEXT_DIR = (Resolve-Path .).Path
```

Permitir duas pastas:

```powershell
$env:COMMAND_AGENT_SAFE_ROOTS = "C:\Users\Administrator\agentes;C:\Users\Administrator\Desktop"
```

---

## Como Rodar

### 1. Modo CLI

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python run_cli.py "mostre o hostname"
```

Exemplo:

```json
{
  "ok": true,
  "action": "run_safe_command",
  "arguments": {
    "command": "hostname"
  },
  "output": {
    "command": "hostname",
    "stdout": "MEU-PC",
    "stderr": "",
    "returncode": 0
  },
  "error": null
}
```

### 2. Interface Textual

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python run_app.py
```

Na interface, voce pode digitar coisas como:

- `quem sou eu no sistema`
- `mostre o hostname`
- `liste os txt da area permitida`
- `leia o arquivo C:\caminho\arquivo.txt`

---

## Acoes Suportadas

Hoje o agente suporta estas acoes internas:

- `list_txt_desktop`
- `list_files_in_path`
- `create_text_file`
- `read_text_file`
- `show_current_dir`
- `pwd`
- `run_safe_command`

### Comandos do sistema permitidos por padrao

- `whoami`
- `hostname`
- `ipconfig`
- `tasklist`

Se um pedido sair dessas regras, o agente responde como `unsupported`.

---

## Exemplos Reais

### Mostrar diretorio atual

```powershell
python run_cli.py "mostre o diretorio atual"
```

### Listar arquivos de uma pasta permitida

```powershell
python run_cli.py "liste os arquivos da pasta C:\Users\Administrator\agentes"
```

### Criar um arquivo de texto

```powershell
python run_cli.py "crie um arquivo chamado nota.txt na pasta C:\Users\Administrator\agentes com o conteudo teste"
```

### Ler um `.txt`

```powershell
python run_cli.py "leia o arquivo C:\Users\Administrator\agentes\teste.txt"
```

---

## Seguranca

Esse projeto foi desenhado para ser util sem virar uma porta aberta.

### Camadas de protecao

- apenas acoes conhecidas sao aceitas
- apenas comandos em whitelist podem ser executados
- apenas arquivos `.txt` podem ser lidos ou criados
- apenas caminhos dentro de `SAFE_ROOTS` sao aceitos
- logs e resultados ficam fora do Git
- configuracao sensivel saiu do codigo fixo da maquina original

### Onde ficam os artefatos locais

- `.localdata/logs/`
- `.localdata/outputs/`

Esses arquivos sao ignorados pelo Git via [`.gitignore`](C:\Users\Administrator\agentes\projects\agents\command_agent_v2\.gitignore).

---

## Testes

Rodar os testes:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m pytest -q
```

Os testes atuais validam:

- restricao de caminhos seguros
- bloqueio de caminhos fora da whitelist
- criacao e leitura de arquivos `.txt`
- listagem de arquivos em diretorio permitido

---

## Publicacao no GitHub

Se voce for subir este projeto, publique esta pasta e nao a raiz inteira do workspace antigo.

Pasta correta:

```text
command_agent_v2/
```

Motivo:

- a raiz anterior mistura ambientes virtuais
- ha logs e artefatos locais
- existem arquivos experimentais que nao fazem parte da versao pronta para publicar

---

## Roadmap

- melhorar o prompt para reconhecer mais instrucoes validas
- adicionar mais acoes seguras
- criar configuracao opcional por arquivo `.env`
- expandir a cobertura de testes
- melhorar o visual da interface
- adicionar exemplos guiados dentro do app

---

## Filosofia do Projeto

Menos permissao, mais previsibilidade.

Menos magia, mais controle.

Menos "a IA pode tudo", mais "a IA ajuda sem quebrar sua maquina".

---

## Licenca

Este repositorio usa a licenca MIT. Veja [LICENSE](C:\Users\Administrator\agentes\projects\agents\command_agent_v2\LICENSE).
