import pytest

from ruleshield.turing_validator import is_valid_ipv4, validate_tokens
from ruleshield.tokenizer import tokenize


def tm(text):
    tokens, result = tokenize(text)
    assert result.accepted
    return validate_tokens(tokens)


@pytest.mark.parametrize("port", [1, 65535])
def test_valid_ports(port):
    assert tm(f"server {{ listen {port}; deny all; }}").accepted


@pytest.mark.parametrize("port", [0, 65536])
def test_invalid_ports(port):
    result = tm(f"server {{ listen {port}; deny all; }}")
    assert result.error_code == "INVALID_PORT"


@pytest.mark.parametrize("ip", ["0.0.0.0", "255.255.255.255", "192.168.1.10"])
def test_valid_ipv4(ip):
    assert is_valid_ipv4(ip)


@pytest.mark.parametrize("ip", ["192.168.1.256", "1.2.3", "1.2.3.4.5", "01.2.3.4", "a.b.c.d"])
def test_invalid_ipv4_helper(ip):
    assert not is_valid_ipv4(ip)


def test_duplicate_unreachable_valid_order_and_syntax_reject():
    assert tm("server { listen 80; allow 1.1.1.1; allow 1.1.1.1; }").error_code == "DUPLICATE_RULE"
    assert tm("server { listen 80; deny all; allow 1.1.1.1; }").error_code == "UNREACHABLE_RULE"
    assert tm("server { listen 80; allow all; deny 1.1.1.1; }").error_code == "UNREACHABLE_RULE"
    assert tm("server { listen 80; allow 1.1.1.1; deny all; }").accepted
    assert not tm("server { listen ; }").accepted
