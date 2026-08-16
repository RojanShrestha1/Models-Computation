from __future__ import annotations

import re

from .errors import TOKENIZATION_ERROR
from .models import Token, ValidationResult

KEYWORDS = {
    "server": "SERVER",
    "listen": "LISTEN",
    "location": "LOCATION",
    "allow": "ALLOW",
    "deny": "DENY",
    "all": "ALL",
}

TOKEN_TYPES = [
    "SERVER",
    "LISTEN",
    "LOCATION",
    "ALLOW",
    "DENY",
    "ALL",
    "IPV4",
    "NUMBER",
    "PATH",
    "LBRACE",
    "RBRACE",
    "SEMICOLON",
    "UNKNOWN",
    "EOF",
]

_IP_CANDIDATE = re.compile(r"^[0-9.]+$")
_IPV4_SHAPE = re.compile(r"^\d+\.\d+\.\d+\.\d+$")


def tokenize(text: str) -> tuple[list[Token], ValidationResult]:
    tokens: list[Token] = []
    i = 0
    line = 1
    col = 1
    trace: list[str] = []

    def add(kind: str, value: str, start_line: int, start_col: int, start: int) -> None:
        token = Token(kind, value, start_line, start_col, start)
        tokens.append(token)
        trace.append(f"{kind}({value!r}) at {start_line}:{start_col}")

    while i < len(text):
        ch = text[i]
        if ch in " \t\r":
            i += 1
            col += 1
            continue
        if ch == "\n":
            i += 1
            line += 1
            col = 1
            continue
        if ch == "#":
            while i < len(text) and text[i] != "\n":
                i += 1
                col += 1
            continue
        start, start_line, start_col = i, line, col
        if ch == "{":
            add("LBRACE", ch, start_line, start_col, start)
            i += 1
            col += 1
            continue
        if ch == "}":
            add("RBRACE", ch, start_line, start_col, start)
            i += 1
            col += 1
            continue
        if ch == ";":
            add("SEMICOLON", ch, start_line, start_col, start)
            i += 1
            col += 1
            continue
        if ch == "/":
            i += 1
            col += 1
            while i < len(text) and re.match(r"[A-Za-z0-9_./-]", text[i]):
                i += 1
                col += 1
            add("PATH", text[start:i], start_line, start_col, start)
            continue
        if ch.isalpha() or ch == "_":
            i += 1
            col += 1
            while i < len(text) and (text[i].isalnum() or text[i] in "_-"):
                i += 1
                col += 1
            value = text[start:i]
            add(KEYWORDS.get(value, "UNKNOWN"), value, start_line, start_col, start)
            continue
        if ch.isdigit():
            i += 1
            col += 1
            while i < len(text) and (text[i].isdigit() or text[i] == "."):
                i += 1
                col += 1
            value = text[start:i]
            if "." in value:
                kind = "IPV4" if _IPV4_SHAPE.match(value) else "UNKNOWN"
            else:
                kind = "NUMBER"
            add(kind, value, start_line, start_col, start)
            continue
        if _IP_CANDIDATE.match(ch):
            add("UNKNOWN", ch, start_line, start_col, start)
            i += 1
            col += 1
            continue
        result = ValidationResult(
            "Tokenizer",
            False,
            TOKENIZATION_ERROR,
            f"Unsupported character {ch!r}. Only the simplified NGINX language is allowed.",
            start_line,
            start_col,
            trace,
        )
        return tokens, result

    tokens.append(Token("EOF", "", line, col, len(text)))
    return tokens, ValidationResult("Tokenizer", True, message="Tokenization accepted.", trace=trace)
