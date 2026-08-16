from ruleshield.cfg import parse_tokens
from ruleshield.policy_evaluator import evaluate_policy
from ruleshield.tokenizer import tokenize


def ast(text):
    tokens, _ = tokenize(text)
    config, result = parse_tokens(tokens)
    assert result.accepted
    return config


def test_exact_allow_deny_all_and_first_match():
    config = ast("server { listen 80; allow 1.1.1.1; deny all; }")
    assert evaluate_policy(config, "1.1.1.1", "/", 80).accepted
    assert not evaluate_policy(config, "2.2.2.2", "/", 80).accepted
    first = ast("server { listen 80; deny 1.1.1.1; allow all; }")
    assert not evaluate_policy(first, "1.1.1.1", "/", 80).accepted
    assert evaluate_policy(first, "2.2.2.2", "/", 80).accepted


def test_longest_location_inheritance_override_and_port():
    config = ast("server { listen 80; deny all; location /admin { allow 1.1.1.1; deny all; } location /admin/reports { deny all; } }")
    assert evaluate_policy(config, "1.1.1.1", "/admin", 80).accepted
    assert not evaluate_policy(config, "1.1.1.1", "/admin/reports/q", 80).accepted
    inherited = ast("server { listen 80; allow all; location /empty { } }")
    assert evaluate_policy(inherited, "3.3.3.3", "/empty", 80).accepted
    assert evaluate_policy(inherited, "3.3.3.3", "/", 81).error_code == "NO_MATCHING_SERVER"


def test_default_deny_invalid_ip_and_deny_all():
    config = ast("server { listen 80; }")
    assert evaluate_policy(config, "1.1.1.1", "/", 80).error_code == "DEFAULT_DENY"
    assert evaluate_policy(config, "01.1.1.1", "/", 80).error_code == "INVALID_IPV4"
    deny = ast("server { listen 80; deny all; }")
    assert evaluate_policy(deny, "1.1.1.1", "/", 80).metadata["decision"] == "DENY"
