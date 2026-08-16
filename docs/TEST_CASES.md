# Test Cases

Tests are split by component:

- Tokenizer: keywords, paths, comments, positions, unknown words and EOF.
- DFA: valid local units, missing tokens, invalid transitions and the missing-brace limitation.
- CFG: valid blocks, nested locations, invalid braces, context errors and AST output.
- Ambiguity: two parse trees for the supplied ambiguous grammar and one predictable corrected structure.
- PDA: balanced blocks, underflow, unclosed blocks and 100-level nesting.
- TM engine: transition lookup, writes, movement, expansion, halting and step limits.
- TM decider: ports, IPv4, duplicate rules, unreachable rules and accept/reject phases.
- Policy evaluator: exact IPs, `all`, first match, longest path, inheritance and default deny.
- Pipeline: model order, final decision and invalid example handling.
- UI: Streamlit widgets, accept/reject display and report generation.
