import json


def format_result(result: dict) -> str:
    lines = []

    status = "OK" if result.get("ok") else "ERRO"
    lines.append(f"Status: {status}")
    lines.append(f"Modo: {result.get('action')}")
    lines.append("")

    arguments = result.get("arguments") or {}
    lines.append("Argumentos:")
    if arguments:
        for key, value in arguments.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- nenhum")
    lines.append("")

    output = result.get("output")
    error = result.get("error")

    if output is not None:
        lines.append("Saida:")
        if isinstance(output, dict):
            stdout = output.get("stdout", "")
            stderr = output.get("stderr", "")
            command = output.get("command", "")
            returncode = output.get("returncode", "")

            lines.append(f"- comando: {command}")
            lines.append(f"- returncode: {returncode}")
            lines.append("")

            if stdout:
                lines.append("[stdout]")
                lines.append(stdout)
                lines.append("")

            if stderr:
                lines.append("[stderr]")
                lines.append(stderr)
                lines.append("")
        elif isinstance(output, list):
            for item in output:
                lines.append(f"- {item}")
        else:
            lines.append(str(output))
        lines.append("")

    if error:
        lines.append("Erro:")
        lines.append(str(error))
        lines.append("")

    return "\n".join(lines).strip()


def format_raw_json(result: dict) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)

