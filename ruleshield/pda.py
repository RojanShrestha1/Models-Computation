from __future__ import annotations

from .errors import PDA_STACK_UNDERFLOW, PDA_UNCLOSED_BLOCK
from .models import Token, ValidationResult

FORMAL_MODEL = {
    "Q": ["q0", "q_read", "q_accept", "q_reject"],
    "Sigma": ["SERVER", "LOCATION", "PATH", "LBRACE", "RBRACE", "EOF"],
    "Gamma": ["$", "SERVER", "LOCATION"],
    "q0": "q0",
    "Z0": "$",
    "F": ["q_accept"],
    "delta": [
        "server { / top -> push SERVER",
        "location PATH { / top -> push LOCATION",
        "} / SERVER -> pop SERVER",
        "} / LOCATION -> pop LOCATION",
        "EOF / $ -> accept",
    ],
}


def validate_tokens(tokens: list[Token]) -> ValidationResult:
    stack = ["$"]
    trace: list[str] = ["Start stack: [$]"]
    ids: list[str] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.type == "SERVER" and i + 1 < len(tokens) and tokens[i + 1].type == "LBRACE":
            stack.append("SERVER")
            trace.append("Read: server {")
            trace.append("Operation: push SERVER")
            trace.append(f"Stack: {stack}")
            ids.append(f"(q_read, token={i}, stack={stack})")
            i += 2
            continue
        if t.type == "LOCATION" and i + 2 < len(tokens) and tokens[i + 1].type == "PATH" and tokens[i + 2].type == "LBRACE":
            stack.append("LOCATION")
            trace.append(f"Read: location {tokens[i + 1].value} {{")
            trace.append("Operation: push LOCATION")
            trace.append(f"Stack: {stack}")
            ids.append(f"(q_read, token={i}, stack={stack})")
            i += 3
            continue
        if t.type == "RBRACE":
            if stack == ["$"]:
                trace.append("Read: }")
                trace.append("Operation: reject; stack contains only bottom marker")
                return ValidationResult("PDA", False, PDA_STACK_UNDERFLOW, "A closing brace appeared before a matching open block.", t.line, t.column, trace, {"formal_model": FORMAL_MODEL, "instantaneous_descriptions": ids})
            popped = stack.pop()
            trace.append("Read: }")
            trace.append(f"Operation: pop {popped}")
            trace.append(f"Stack: {stack}")
            ids.append(f"(q_read, token={i}, stack={stack})")
        if t.type == "EOF":
            break
        i += 1
    if stack != ["$"]:
        return ValidationResult("PDA", False, PDA_UNCLOSED_BLOCK, "Input ended while one or more blocks were still open.", tokens[-1].line, tokens[-1].column, trace, {"formal_model": FORMAL_MODEL, "instantaneous_descriptions": ids, "final_stack": stack})
    trace.append("Accept: input ended and stack returned to [$].")
    return ValidationResult("PDA", True, message="Nested block structure accepted.", trace=trace, metadata={"formal_model": FORMAL_MODEL, "instantaneous_descriptions": ids, "final_stack": stack})
