# RuleShield: An Automata-Based NGINX Access-Control Validator

RuleShield is an educational Python application that validates a small NGINX-like access-control language with several formal-language models:

1. Tokenizer for lexical validation.
2. DFA for local regular directive patterns.
3. CFG recursive-descent parser for syntax and AST construction.
4. PDA for nested block balancing.
5. Literal Turing Machine engine plus a high-level TM-style semantic decider.
6. Policy evaluator for simplified allow/deny decisions.

NGINX is a web server, reverse proxy and load balancer with access-control features. This project does not model the full NGINX language and does not claim that real NGINX internally uses these exact automata.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

python main.py examples/valid_nested.conf --trace
streamlit run app.py
pytest -v
pytest --cov=ruleshield --cov-report=term-missing
python generate_diagrams.py
```

## Supported Directives

`server`, `listen`, `location`, `allow`, `deny`, `all`, IPv4 addresses, port numbers, paths, braces, semicolons and comments beginning with `#`.

Unrelated directives are rejected with `UNKNOWN_DIRECTIVE`.
