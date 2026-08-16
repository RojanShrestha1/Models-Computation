import pytest

from ruleshield.cfg import parse_tokens
from ruleshield.tokenizer import tokenize


def parse(text):
    tokens, tok = tokenize(text)
    assert tok.accepted
    return parse_tokens(tokens)


@pytest.mark.parametrize("text", [
    "server {}",
    "server { listen 80; } server { listen 81; }",
    "server { allow all; deny 10.0.0.1; }",
    "server { location /admin { deny all; } }",
    "server { location /a { location /a/b { allow all; } } }",
])
def test_valid_cfg_forms(text):
    ast, result = parse(text)
    assert result.accepted
    assert ast.servers
    assert result.metadata["productions"]


@pytest.mark.parametrize("text, code", [
    ("server { listen 80 }", "CFG_SYNTAX_ERROR"),
    ("server listen 80; }", "CFG_SYNTAX_ERROR"),
    ("server { listen 80;", "CFG_SYNTAX_ERROR"),
    ("server { proxy_pass x; }", "UNKNOWN_DIRECTIVE"),
    ("server { location / { listen 80; } }", "INVALID_CONTEXT"),
    ("listen 80;", "CFG_SYNTAX_ERROR"),
    ("server {} deny all;", "CFG_SYNTAX_ERROR"),
])
def test_invalid_cfg_forms(text, code):
    _, result = parse(text)
    assert not result.accepted
    assert result.error_code == code


def test_correct_ast_nodes_and_trace(valid_tokens):
    ast, result = parse_tokens(valid_tokens)
    assert result.accepted
    assert ast.servers[0].listen == [80]
    assert ast.servers[0].rules[0].target == "10.0.0.5"
    assert "parse tree" in result.metadata["parse_tree_vs_ast"].lower()
