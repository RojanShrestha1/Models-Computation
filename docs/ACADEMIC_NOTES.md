# Academic Notes

RuleShield is an educational formal-language model for a simplified NGINX access-control configuration language.

NGINX is primarily a web server, reverse proxy and load balancer with access-control features. It should not be described as a complete network firewall.

This project does not claim that real NGINX internally uses these exact DFA, PDA or Turing Machine implementations. The automata are teaching models that help separate kinds of validation.

The supported language is intentionally small. It is not the complete NGINX configuration language.

Validation layers are separate:

- Lexical validation: the tokenizer recognizes allowed words, numbers, paths, braces and semicolons.
- Local regular validation: the DFA checks short directive patterns such as `listen NUMBER ;`.
- Syntax validation: the CFG parser checks grammatical structure and builds an AST.
- Structural validation: the PDA checks nested block balance with a stack.
- Semantic validation: the high-level TM-style decider checks ports, IPv4 values, duplicate rules and unreachable rules.

The DFA does not validate arbitrary nesting because a finite automaton has no unbounded stack.

The ambiguity module demonstrates ambiguity only for the supplied grammar `RULES -> RULES RULES | RULE`. The project does not claim that CFG ambiguity can be detected automatically for every arbitrary grammar.

The literal Turing Machine engine is transition-driven. The configuration semantic validator is clearly labelled as a high-level TM-style decider, not a complete low-level transition encoding of the full language.

Leading-zero IPv4 addresses are rejected in this project, so `192.168.001.1` is invalid.
