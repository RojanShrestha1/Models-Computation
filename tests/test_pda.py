from ruleshield.pda import validate_tokens
from ruleshield.tokenizer import tokenize


def pda(text):
    tokens, result = tokenize(text)
    assert result.accepted
    return validate_tokens(tokens)


def test_basic_nested_and_siblings():
    assert pda("server { location /a { } location /b { } }").accepted
    assert pda("server { location /a { location /a/b { } } }").accepted


def test_underflow_unclosed_and_extra_closing():
    assert pda("}").error_code == "PDA_STACK_UNDERFLOW"
    assert pda("server {").error_code == "PDA_UNCLOSED_BLOCK"
    assert pda("server { } }").error_code == "PDA_STACK_UNDERFLOW"


def test_deep_nesting_100_and_final_stack():
    text = "server {" + " ".join(f"location /a{i} {{" for i in range(100)) + " " + ("}" * 101)
    result = pda(text)
    assert result.accepted
    assert result.metadata["final_stack"] == ["$"]


def test_push_pop_trace():
    result = pda("server { location /admin { } }")
    joined = "\n".join(result.trace)
    assert "push SERVER" in joined
    assert "push LOCATION" in joined
    assert "pop LOCATION" in joined
