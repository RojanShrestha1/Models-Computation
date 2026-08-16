# Formal Specification

## DFA

`M = (Q, Sigma, delta, q0, F)`

- `Q = {q0, q_server, q_location, q_path, q_listen, q_number, q_action, q_target, q_accept, q_dead}`
- `Sigma = {SERVER, LOCATION, PATH, LISTEN, NUMBER, ALLOW, DENY, IPV4, ALL, LBRACE, RBRACE, SEMICOLON}`
- `q0 = q0`
- `F = {q_accept}`
- `q_dead` is the reject sink.

Example trace: `q0 --LISTEN--> q_listen`, `q_listen --NUMBER--> q_number`, `q_number --SEMICOLON--> q_accept`.

The DFA validates local regular units only.

## CFG

```text
CONFIG         -> SERVER_BLOCK SERVER_LIST
SERVER_LIST    -> SERVER_BLOCK SERVER_LIST | epsilon
SERVER_BLOCK   -> server { SERVER_ITEMS }
SERVER_ITEMS   -> SERVER_ITEM SERVER_ITEMS | epsilon
SERVER_ITEM    -> LISTEN_STMT | ACCESS_STMT | LOCATION_BLOCK
LISTEN_STMT    -> listen NUMBER ;
ACCESS_STMT    -> ACTION TARGET ;
ACTION         -> allow | deny
TARGET         -> IPV4 | all
LOCATION_BLOCK -> location PATH { LOCATION_ITEMS }
LOCATION_ITEMS -> LOCATION_ITEM LOCATION_ITEMS | epsilon
LOCATION_ITEM  -> ACCESS_STMT | LOCATION_BLOCK
```

The AST keeps useful nodes: configuration, server, location and rule.

## PDA

`M = (Q, Sigma, Gamma, delta, q0, Z0, F)`

- `Q = {q0, q_read, q_accept, q_reject}`
- `Gamma = {$, SERVER, LOCATION}`
- Start stack symbol is `$`.
- `server {` pushes `SERVER`.
- `location PATH {` pushes `LOCATION`.
- `}` pops one block symbol.
- EOF accepts only when the stack is `$`.

## Turing Machine

Part A is a literal single-tape engine with explicit transitions.

Part B is a high-level TM-style decider with phases `q_start`, `q_scan`, `q_rewind`, `q_syntax`, `q_check_context`, `q_check_ports`, `q_check_ipv4`, `q_check_rules`, `q_accept`, `q_reject`.
