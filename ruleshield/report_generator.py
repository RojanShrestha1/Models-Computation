from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_report(data: dict[str, Any], input_text: str, output_path: str | Path = "output/validation_report.md", test_summary: str = "Run pytest -v for the current test summary.") -> str:
    lines: list[str] = ["# RuleShield Validation Report", "", "## Input Configuration", "```nginx", input_text.strip(), "```", ""]
    lines.extend(["## Tokens", "| Type | Value | Line | Column |", "| --- | --- | ---: | ---: |"])
    for token in data["tokens"]:
        lines.append(f"| {token.type} | `{token.value}` | {token.line} | {token.column} |")
    lines.append("")
    for result in data["results"] + [data["final"]]:
        lines.extend([f"## {result.model_name}", f"Accepted: `{result.accepted}`"])
        if result.error_code:
            lines.append(f"Error: `{result.error_code}` at {result.line}:{result.column}")
        lines.append(result.message)
        if result.trace:
            lines.extend(["", "<details><summary>Trace</summary>", "", "```text", *[str(x) for x in result.trace[:200]], "```", "</details>"])
        lines.append("")
    ambiguity = data["ambiguity"]
    lines.extend(["## Ambiguity Example", ambiguity.message, "```text", *ambiguity.trace, "```", ""])
    if data.get("ast"):
        lines.extend(["## AST", "```text", repr(data["ast"]), "```", ""])
    if data.get("policy"):
        policy = data["policy"]
        lines.extend(["## Policy Decision", policy.message, "```text", *policy.trace, "```", ""])
    lines.extend(["## Runtime", "| Stage | Seconds |", "| --- | ---: |"])
    for key, value in data["timings"].items():
        lines.append(f"| {key} | {value:.6f} |")
    lines.extend(["", "## Test Summary", test_summary, "", "## Errors", "Errors are shown in each model section above."])
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines) + "\n"
    path.write_text(content, encoding="utf-8")
    return content
