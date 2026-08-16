from __future__ import annotations

from .models import ValidationResult


def ambiguous_rule_trees(rules: list[str] | None = None) -> dict[str, str]:
    rules = ["RULE1", "RULE2", "RULE3"] if rules is None else rules
    if len(rules) != 3:
        raise ValueError("This classroom demonstration expects exactly three rule symbols.")
    a, b, c = rules
    return {
        "left_grouped": f"(({a} {b}) {c})",
        "right_grouped": f"({a} ({b} {c}))",
    }


def corrected_rule_structure(rules: list[str] | None = None) -> str:
    rules = ["RULE1", "RULE2", "RULE3"] if rules is None else rules
    if not rules:
        return "epsilon"
    return "RULE " + corrected_rule_structure(rules[1:])


def demonstrate() -> ValidationResult:
    trees = ambiguous_rule_trees()
    return ValidationResult(
        "CFG Ambiguity Demo",
        True,
        message="The supplied grammar RULES -> RULES RULES | RULE gives two parse trees for RULE1 RULE2 RULE3.",
        trace=[trees["left_grouped"], trees["right_grouped"], "Corrected grammar: RULES -> RULE RULES | epsilon"],
        metadata={
            "ambiguous_grammar": "RULES -> RULES RULES | RULE",
            "corrected_grammar": "RULES -> RULE RULES | epsilon",
            "universal_detection_claim": "No universal ambiguity detector is claimed; this program demonstrates ambiguity only for this supplied example.",
        },
    )
