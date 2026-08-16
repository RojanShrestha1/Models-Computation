from __future__ import annotations

from .errors import DFA_PATTERN_ERROR, UNKNOWN_DIRECTIVE
from .models import Token, ValidationResult

FORMAL_MODEL = {
    "Q": ["q0", "q_server", "q_location", "q_path", "q_listen", "q_number", "q_action", "q_target", "q_accept", "q_dead"],
    "Sigma": ["SERVER", "LOCATION", "PATH", "LISTEN", "NUMBER", "ALLOW", "DENY", "IPV4", "ALL", "LBRACE", "RBRACE", "SEMICOLON"],
    "q0": "q0",
    "F": ["q_accept"],
    "dead_state": "q_dead",
}

TRANSITIONS = {
    ("q0", "SERVER"): "q_server",
    ("q_server", "LBRACE"): "q_accept",
    ("q0", "LOCATION"): "q_location",
    ("q_location", "PATH"): "q_path",
    ("q_path", "LBRACE"): "q_accept",
    ("q0", "LISTEN"): "q_listen",
    ("q_listen", "NUMBER"): "q_number",
    ("q_number", "SEMICOLON"): "q_accept",
    ("q0", "ALLOW"): "q_action",
    ("q0", "DENY"): "q_action",
    ("q_action", "IPV4"): "q_target",
    ("q_action", "ALL"): "q_target",
    ("q_target", "SEMICOLON"): "q_accept",
    ("q0", "RBRACE"): "q_accept",
}


def run_pattern(types: list[str]) -> tuple[bool, list[str]]:
    state = "q0"
    trace: list[str] = []
    for typ in types:
        nxt = TRANSITIONS.get((state, typ), "q_dead")
        trace.append(f"{state} --{typ}--> {nxt}")
        state = nxt
    return state == "q_accept", trace


def validate_tokens(tokens: list[Token]) -> ValidationResult:
    i = 0
    trace: list[str] = []
    body = [t for t in tokens if t.type != "EOF"]
    while i < len(body):
        token = body[i]
        if token.type == "UNKNOWN":
            return ValidationResult("DFA", False, UNKNOWN_DIRECTIVE, f"Unknown directive or token {token.value!r}.", token.line, token.column, trace, FORMAL_MODEL)
        if token.type == "SERVER":
            unit = body[i : i + 2]
            pattern = ["SERVER", "LBRACE"]
        elif token.type == "LOCATION":
            unit = body[i : i + 3]
            pattern = ["LOCATION", "PATH", "LBRACE"]
        elif token.type == "LISTEN":
            unit = body[i : i + 3]
            pattern = ["LISTEN", "NUMBER", "SEMICOLON"]
        elif token.type in {"ALLOW", "DENY"}:
            unit = body[i : i + 3]
            pattern = [token.type, unit[1].type if len(unit) > 1 else "EOF", unit[2].type if len(unit) > 2 else "EOF"]
        elif token.type == "RBRACE":
            unit = [token]
            pattern = ["RBRACE"]
        else:
            return ValidationResult("DFA", False, DFA_PATTERN_ERROR, f"{token.type} cannot begin a valid local regular unit.", token.line, token.column, trace, FORMAL_MODEL)
        ok, unit_trace = run_pattern([t.type for t in unit])
        trace.extend(unit_trace)
        if not ok or len(unit) != len(pattern):
            return ValidationResult("DFA", False, DFA_PATTERN_ERROR, f"Local pattern beginning with {token.value!r} is incomplete or invalid.", token.line, token.column, trace, FORMAL_MODEL)
        i += len(unit)
    return ValidationResult("DFA", True, message="All local regular units matched. Brace nesting is intentionally left to the PDA.", trace=trace, metadata=FORMAL_MODEL)
