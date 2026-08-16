# Project Definition

RuleShield validates simplified NGINX access-control files and shows how increasing formal models catch different classes of errors.

Problem: students often see DFA, CFG, PDA and Turing Machines as abstract. RuleShield maps them to a small practical language while keeping the limitations explicit.

Scope:

- Multiple `server` blocks.
- `listen` at server level.
- `allow` and `deny` at server or location level.
- Nested `location` blocks.
- IPv4 and `all` targets.

Out of scope:

- Complete NGINX syntax.
- Real NGINX runtime behavior.
- Networking, TLS, proxying, databases, login systems or Docker.
