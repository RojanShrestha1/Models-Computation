from __future__ import annotations

import ipaddress

from . import errors
from .cfg import parse_tokens
from .models import Config, Location, Rule, Token, ValidationResult

PHASES = ["q_start", "q_scan", "q_rewind", "q_syntax", "q_check_context", "q_check_ports", "q_check_ipv4", "q_check_rules", "q_accept", "q_reject"]


def validate_tokens(tokens: list[Token], ast: Config | None = None) -> ValidationResult:
    trace = ["q_start", "q_scan", "q_rewind", "q_syntax"]
    if ast is None:
        ast, syntax = parse_tokens(tokens)
        if not syntax.accepted:
            trace.append("q_reject")
            return ValidationResult("High-level TM Decider", False, syntax.error_code or errors.CFG_SYNTAX_ERROR, "Semantic decider rejects because syntax was not accepted first.", syntax.line, syntax.column, trace + syntax.trace, {"phases": PHASES})
    trace.append("q_check_context")
    trace.append("q_check_ports")
    for server in ast.servers:
        for port in server.listen:
            if port < 1 or port > 65535:
                trace.append("q_reject")
                return ValidationResult("High-level TM Decider", False, errors.INVALID_PORT, f"Port {port} is outside the allowed range 1-65535.", server.line, server.column, trace, {"phases": PHASES})
    trace.append("q_check_ipv4")
    for rule in _rules(ast):
        if rule.target != "all" and not is_valid_ipv4(rule.target):
            trace.append("q_reject")
            return ValidationResult("High-level TM Decider", False, errors.INVALID_IPV4, f"IPv4 address {rule.target!r} is invalid. Four octets from 0 to 255 are required; leading zeros are rejected.", rule.line, rule.column, trace, {"phases": PHASES})
    trace.append("q_check_rules")
    for block_name, ruleset in _rule_sets(ast):
        seen: set[tuple[str, str]] = set()
        terminal_seen = False
        for rule in ruleset:
            key = (rule.action, rule.target)
            if key in seen:
                trace.append("q_reject")
                return ValidationResult("High-level TM Decider", False, errors.DUPLICATE_RULE, f"Duplicate rule {rule.action} {rule.target} in {block_name}.", rule.line, rule.column, trace, {"phases": PHASES})
            if terminal_seen:
                trace.append("q_reject")
                return ValidationResult("High-level TM Decider", False, errors.UNREACHABLE_RULE, f"Rule {rule.action} {rule.target} is unreachable after a previous all rule in {block_name}.", rule.line, rule.column, trace, {"phases": PHASES})
            seen.add(key)
            if rule.target == "all":
                terminal_seen = True
    trace.append("q_accept")
    return ValidationResult("High-level TM Decider", True, message="Semantic checks accepted.", trace=trace, metadata={"phases": PHASES, "note": "This is a readable high-level TM-style decider, not a full low-level transition encoding."})


def is_valid_ipv4(value: str) -> bool:
    parts = value.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if len(part) > 1 and part.startswith("0"):
            return False
    try:
        ipaddress.IPv4Address(value)
    except ipaddress.AddressValueError:
        return False
    return True


def _rules(config: Config) -> list[Rule]:
    return [rule for _, ruleset in _rule_sets(config) for rule in ruleset]


def _rule_sets(config: Config) -> list[tuple[str, list[Rule]]]:
    sets: list[tuple[str, list[Rule]]] = []
    for idx, server in enumerate(config.servers):
        sets.append((f"server[{idx}]", server.rules))
        sets.extend(_location_rule_sets(server.locations, f"server[{idx}]"))
    return sets


def _location_rule_sets(locations: list[Location], prefix: str) -> list[tuple[str, list[Rule]]]:
    sets: list[tuple[str, list[Rule]]] = []
    for loc in locations:
        name = f"{prefix}/location({loc.path})"
        sets.append((name, loc.rules))
        sets.extend(_location_rule_sets(loc.locations, name))
    return sets
