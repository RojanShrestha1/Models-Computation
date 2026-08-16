from __future__ import annotations

import ipaddress

from .errors import DEFAULT_DENY, INVALID_IPV4, NO_MATCHING_SERVER
from .models import Config, Location, Rule, Server, ValidationResult
from .turing_validator import is_valid_ipv4


def evaluate_policy(config: Config, client_ip: str, path: str, port: int) -> ValidationResult:
    trace = [f"Requested client: {client_ip}", f"Requested path: {path}", f"Requested port: {port}"]
    if not is_valid_ipv4(client_ip):
        return ValidationResult("Policy Evaluator", False, INVALID_IPV4, f"Client IP {client_ip!r} is invalid.", trace=trace)
    server = _match_server(config, port)
    if server is None:
        trace.append("No server listens on the requested port.")
        return ValidationResult("Policy Evaluator", False, NO_MATCHING_SERVER, "No matching server was found for the requested port.", trace=trace, metadata={"decision": "DENY"})
    trace.append(f"Matched server: port {port}")
    location = _longest_location(server.locations, path)
    if location:
        trace.append(f"Matched location: {location.path}")
    rules = location.rules if location and location.rules else server.rules
    if location and not location.rules:
        trace.append("Location has no rules; inherited server-level rules.")
    for rule in rules:
        trace.append(f"Checked rule: {rule.action} {rule.target}")
        if _matches(rule, client_ip):
            decision = "ALLOW" if rule.action == "allow" else "DENY"
            trace.append(f"Final decision: {decision}")
            return ValidationResult("Policy Evaluator", decision == "ALLOW", message=f"Policy decision: {decision}.", trace=trace, metadata={"decision": decision, "matched_rule": f"{rule.action} {rule.target}"})
    trace.append("Final decision: DENY")
    return ValidationResult("Policy Evaluator", False, DEFAULT_DENY, "No rule matched, so the project default is deny.", trace=trace, metadata={"decision": "DENY"})


def _match_server(config: Config, port: int) -> Server | None:
    for server in config.servers:
        if port in server.listen:
            return server
    return None


def _longest_location(locations: list[Location], path: str) -> Location | None:
    matches: list[Location] = []

    def visit(items: list[Location]) -> None:
        for loc in items:
            if path == loc.path or path.startswith(loc.path.rstrip("/") + "/") or loc.path == "/":
                matches.append(loc)
            visit(loc.locations)

    visit(locations)
    if not matches:
        return None
    return max(matches, key=lambda loc: len(loc.path))


def _matches(rule: Rule, client_ip: str) -> bool:
    if rule.target == "all":
        return True
    return ipaddress.IPv4Address(rule.target) == ipaddress.IPv4Address(client_ip)
