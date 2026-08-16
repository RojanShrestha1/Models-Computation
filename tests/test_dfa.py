import pytest

from ruleshield.dfa import run_pattern, validate_tokens
from ruleshield.tokenizer import tokenize


@pytest.mark.parametrize("text", ["server {", "location / {", "listen 80;", "allow 10.0.0.1;", "allow all;", "deny 10.0.0.1;", "deny all;", "}"])
def test_valid_local_patterns(text):
    tokens, _ = tokenize(text)
    assert validate_tokens(tokens).accepted


@pytest.mark.parametrize("text", ["listen ;", "listen 80", "allow ;", "allow /admin;", "server listen"])
def test_invalid_local_patterns(text):
    tokens, _ = tokenize(text)
    assert not validate_tokens(tokens).accepted


def test_dead_state_and_invalid_transition():
    ok, trace = run_pattern(["LISTEN", "IPV4"])
    assert not ok
    assert trace[-1].endswith("q_dead")


def test_dfa_limitation_missing_outer_brace():
    text = "server { listen 80; deny all;"
    tokens, _ = tokenize(text)
    result = validate_tokens(tokens)
    assert result.accepted
    assert "Brace nesting" in result.message


def test_deterministic_repeated_runs(valid_tokens):
    assert validate_tokens(valid_tokens).trace == validate_tokens(valid_tokens).trace
