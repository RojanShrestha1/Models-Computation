from __future__ import annotations

import time
from dataclasses import asdict
from typing import Any

from . import ambiguity, dfa, pda, turing_validator
from .cfg import parse_tokens
from .models import Config, ValidationResult
from .policy_evaluator import evaluate_policy
from .tokenizer import tokenize


def run_pipeline(text: str, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    timings: dict[str, float] = {}
    results: list[ValidationResult] = []
    ast: Config | None = None

    start = time.perf_counter()
    tokens, token_result = tokenize(text)
    timings["tokenizer"] = time.perf_counter() - start
    results.append(token_result)
    if not token_result.accepted:
        final = _final(results)
        return {"tokens": tokens, "ast": ast, "results": results, "ambiguity": ambiguity.demonstrate(), "policy": None, "final": final, "timings": timings}

    for name, func in [("dfa", dfa.validate_tokens), ("cfg", parse_tokens), ("pda", pda.validate_tokens)]:
        start = time.perf_counter()
        if name == "cfg":
            ast, res = func(tokens)
        else:
            res = func(tokens)
        timings[name] = time.perf_counter() - start
        results.append(res)

    start = time.perf_counter()
    tm_result = turing_validator.validate_tokens(tokens, ast if ast else None)
    timings["tm"] = time.perf_counter() - start
    results.append(tm_result)

    policy_result = None
    if policy and ast and all(r.accepted for r in results):
        start = time.perf_counter()
        policy_result = evaluate_policy(ast, policy["client_ip"], policy["path"], int(policy["port"]))
        timings["policy"] = time.perf_counter() - start

    final = _final(results)
    return {"tokens": tokens, "ast": ast, "results": results, "ambiguity": ambiguity.demonstrate(), "policy": policy_result, "final": final, "timings": timings}


def _final(results: list[ValidationResult]) -> ValidationResult:
    for result in results:
        if not result.accepted:
            return ValidationResult("FINAL", False, result.error_code, f"Final reject because {result.model_name} rejected: {result.message}", result.line, result.column, result.trace, {"model_results": [(r.model_name, r.accepted) for r in results]})
    return ValidationResult("FINAL", True, message="Final accept: tokenizer, DFA, CFG, PDA and TM semantic validation all accepted.", metadata={"model_results": [(r.model_name, r.accepted) for r in results]})


def ast_to_dict(config: Config | None) -> dict[str, Any] | None:
    return asdict(config) if config else None
