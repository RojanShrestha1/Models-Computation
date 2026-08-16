from __future__ import annotations

from pathlib import Path

import pytest

from ruleshield.cfg import parse_tokens
from ruleshield.tokenizer import tokenize

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def valid_text() -> str:
    return (ROOT / "examples" / "valid_basic.conf").read_text(encoding="utf-8")


@pytest.fixture
def valid_tokens(valid_text):
    tokens, result = tokenize(valid_text)
    assert result.accepted
    return tokens


@pytest.fixture
def valid_ast(valid_tokens):
    ast, result = parse_tokens(valid_tokens)
    assert result.accepted
    return ast
