from ruleshield.tokenizer import TOKEN_TYPES, tokenize


def types(text):
    return [t.type for t, _ in [tokenize(text)] for t in t]


def test_every_keyword_and_eof():
    tokens, result = tokenize("server listen location allow deny all")
    assert result.accepted
    assert [t.type for t in tokens] == ["SERVER", "LISTEN", "LOCATION", "ALLOW", "DENY", "ALL", "EOF"]
    assert "EOF" in TOKEN_TYPES


def test_paths_ports_ipv4_comments_whitespace():
    tokens, result = tokenize("# hi\n\nlocation /admin/reports { listen 80; allow 192.168.1.10; }")
    assert result.accepted
    assert [t.type for t in tokens[:-1]] == ["LOCATION", "PATH", "LBRACE", "LISTEN", "NUMBER", "SEMICOLON", "ALLOW", "IPV4", "SEMICOLON", "RBRACE"]
    assert tokens[0].line == 3
    assert tokens[1].value == "/admin/reports"


def test_line_column_accuracy():
    tokens, _ = tokenize("server {\n    listen 80;\n}")
    listen = next(t for t in tokens if t.type == "LISTEN")
    assert (listen.line, listen.column) == (2, 5)


def test_unknown_word_and_unsupported_character():
    tokens, result = tokenize("proxy_pass http;")
    assert result.accepted
    assert tokens[0].type == "UNKNOWN"
    _, bad = tokenize("@")
    assert not bad.accepted
    assert bad.error_code == "TOKENIZATION_ERROR"


def test_malformed_dotted_address_is_unknown():
    tokens, result = tokenize("allow 1.2.3;")
    assert result.accepted
    assert [t.type for t in tokens[:3]] == ["ALLOW", "UNKNOWN", "SEMICOLON"]
