# RuleShield Validation Report

## Input Configuration
```nginx
server {
    listen 80;
    allow 10.0.0.5;
    deny all;

    location /admin {
        allow 192.168.1.10;
        deny all;

        location /admin/reports {
            allow 192.168.1.20;
            deny all;
        }
    
}
```

## Tokens
| Type | Value | Line | Column |
| --- | --- | ---: | ---: |
| SERVER | `server` | 1 | 1 |
| LBRACE | `{` | 1 | 8 |
| LISTEN | `listen` | 2 | 5 |
| NUMBER | `80` | 2 | 12 |
| SEMICOLON | `;` | 2 | 14 |
| ALLOW | `allow` | 3 | 5 |
| IPV4 | `10.0.0.5` | 3 | 11 |
| SEMICOLON | `;` | 3 | 19 |
| DENY | `deny` | 4 | 5 |
| ALL | `all` | 4 | 10 |
| SEMICOLON | `;` | 4 | 13 |
| LOCATION | `location` | 6 | 5 |
| PATH | `/admin` | 6 | 14 |
| LBRACE | `{` | 6 | 21 |
| ALLOW | `allow` | 7 | 9 |
| IPV4 | `192.168.1.10` | 7 | 15 |
| SEMICOLON | `;` | 7 | 27 |
| DENY | `deny` | 8 | 9 |
| ALL | `all` | 8 | 14 |
| SEMICOLON | `;` | 8 | 17 |
| LOCATION | `location` | 10 | 9 |
| PATH | `/admin/reports` | 10 | 18 |
| LBRACE | `{` | 10 | 33 |
| ALLOW | `allow` | 11 | 13 |
| IPV4 | `192.168.1.20` | 11 | 19 |
| SEMICOLON | `;` | 11 | 31 |
| DENY | `deny` | 12 | 13 |
| ALL | `all` | 12 | 18 |
| SEMICOLON | `;` | 12 | 21 |
| RBRACE | `}` | 13 | 9 |
| RBRACE | `}` | 15 | 1 |
| EOF | `` | 16 | 1 |

## Tokenizer
Accepted: `True`
Tokenization accepted.

<details><summary>Trace</summary>

```text
SERVER('server') at 1:1
LBRACE('{') at 1:8
LISTEN('listen') at 2:5
NUMBER('80') at 2:12
SEMICOLON(';') at 2:14
ALLOW('allow') at 3:5
IPV4('10.0.0.5') at 3:11
SEMICOLON(';') at 3:19
DENY('deny') at 4:5
ALL('all') at 4:10
SEMICOLON(';') at 4:13
LOCATION('location') at 6:5
PATH('/admin') at 6:14
LBRACE('{') at 6:21
ALLOW('allow') at 7:9
IPV4('192.168.1.10') at 7:15
SEMICOLON(';') at 7:27
DENY('deny') at 8:9
ALL('all') at 8:14
SEMICOLON(';') at 8:17
LOCATION('location') at 10:9
PATH('/admin/reports') at 10:18
LBRACE('{') at 10:33
ALLOW('allow') at 11:13
IPV4('192.168.1.20') at 11:19
SEMICOLON(';') at 11:31
DENY('deny') at 12:13
ALL('all') at 12:18
SEMICOLON(';') at 12:21
RBRACE('}') at 13:9
RBRACE('}') at 15:1
```
</details>

## DFA
Accepted: `True`
All local regular units matched. Brace nesting is intentionally left to the PDA.

<details><summary>Trace</summary>

```text
q0 --SERVER--> q_server
q_server --LBRACE--> q_accept
q0 --LISTEN--> q_listen
q_listen --NUMBER--> q_number
q_number --SEMICOLON--> q_accept
q0 --ALLOW--> q_action
q_action --IPV4--> q_target
q_target --SEMICOLON--> q_accept
q0 --DENY--> q_action
q_action --ALL--> q_target
q_target --SEMICOLON--> q_accept
q0 --LOCATION--> q_location
q_location --PATH--> q_path
q_path --LBRACE--> q_accept
q0 --ALLOW--> q_action
q_action --IPV4--> q_target
q_target --SEMICOLON--> q_accept
q0 --DENY--> q_action
q_action --ALL--> q_target
q_target --SEMICOLON--> q_accept
q0 --LOCATION--> q_location
q_location --PATH--> q_path
q_path --LBRACE--> q_accept
q0 --ALLOW--> q_action
q_action --IPV4--> q_target
q_target --SEMICOLON--> q_accept
q0 --DENY--> q_action
q_action --ALL--> q_target
q_target --SEMICOLON--> q_accept
q0 --RBRACE--> q_accept
q0 --RBRACE--> q_accept
```
</details>

## CFG
Accepted: `False`
Error: `CFG_SYNTAX_ERROR` at 16:1
Expected RBRACE, but found EOF ('').

<details><summary>Trace</summary>

```text
Read SERVER('server') at 1:1
Read LBRACE('{') at 1:8
Read LISTEN('listen') at 2:5
Read NUMBER('80') at 2:12
Read SEMICOLON(';') at 2:14
Read ALLOW('allow') at 3:5
Read IPV4('10.0.0.5') at 3:11
Read SEMICOLON(';') at 3:19
Read DENY('deny') at 4:5
Read ALL('all') at 4:10
Read SEMICOLON(';') at 4:13
Read LOCATION('location') at 6:5
Read PATH('/admin') at 6:14
Read LBRACE('{') at 6:21
Read ALLOW('allow') at 7:9
Read IPV4('192.168.1.10') at 7:15
Read SEMICOLON(';') at 7:27
Read DENY('deny') at 8:9
Read ALL('all') at 8:14
Read SEMICOLON(';') at 8:17
Read LOCATION('location') at 10:9
Read PATH('/admin/reports') at 10:18
Read LBRACE('{') at 10:33
Read ALLOW('allow') at 11:13
Read IPV4('192.168.1.20') at 11:19
Read SEMICOLON(';') at 11:31
Read DENY('deny') at 12:13
Read ALL('all') at 12:18
Read SEMICOLON(';') at 12:21
Read RBRACE('}') at 13:9
Read RBRACE('}') at 15:1
```
</details>

## PDA
Accepted: `False`
Error: `PDA_UNCLOSED_BLOCK` at 16:1
Input ended while one or more blocks were still open.

<details><summary>Trace</summary>

```text
Start stack: [$]
Read: server {
Operation: push SERVER
Stack: ['$', 'SERVER']
Read: location /admin {
Operation: push LOCATION
Stack: ['$', 'SERVER', 'LOCATION']
Read: location /admin/reports {
Operation: push LOCATION
Stack: ['$', 'SERVER', 'LOCATION', 'LOCATION']
Read: }
Operation: pop LOCATION
Stack: ['$', 'SERVER', 'LOCATION']
Read: }
Operation: pop LOCATION
Stack: ['$', 'SERVER']
```
</details>

## High-level TM Decider
Accepted: `False`
Error: `CFG_SYNTAX_ERROR` at 16:1
Semantic decider rejects because syntax was not accepted first.

<details><summary>Trace</summary>

```text
q_start
q_scan
q_rewind
q_syntax
q_reject
Read SERVER('server') at 1:1
Read LBRACE('{') at 1:8
Read LISTEN('listen') at 2:5
Read NUMBER('80') at 2:12
Read SEMICOLON(';') at 2:14
Read ALLOW('allow') at 3:5
Read IPV4('10.0.0.5') at 3:11
Read SEMICOLON(';') at 3:19
Read DENY('deny') at 4:5
Read ALL('all') at 4:10
Read SEMICOLON(';') at 4:13
Read LOCATION('location') at 6:5
Read PATH('/admin') at 6:14
Read LBRACE('{') at 6:21
Read ALLOW('allow') at 7:9
Read IPV4('192.168.1.10') at 7:15
Read SEMICOLON(';') at 7:27
Read DENY('deny') at 8:9
Read ALL('all') at 8:14
Read SEMICOLON(';') at 8:17
Read LOCATION('location') at 10:9
Read PATH('/admin/reports') at 10:18
Read LBRACE('{') at 10:33
Read ALLOW('allow') at 11:13
Read IPV4('192.168.1.20') at 11:19
Read SEMICOLON(';') at 11:31
Read DENY('deny') at 12:13
Read ALL('all') at 12:18
Read SEMICOLON(';') at 12:21
Read RBRACE('}') at 13:9
Read RBRACE('}') at 15:1
```
</details>

## FINAL
Accepted: `False`
Error: `CFG_SYNTAX_ERROR` at 16:1
Final reject because CFG rejected: Expected RBRACE, but found EOF ('').

<details><summary>Trace</summary>

```text
Read SERVER('server') at 1:1
Read LBRACE('{') at 1:8
Read LISTEN('listen') at 2:5
Read NUMBER('80') at 2:12
Read SEMICOLON(';') at 2:14
Read ALLOW('allow') at 3:5
Read IPV4('10.0.0.5') at 3:11
Read SEMICOLON(';') at 3:19
Read DENY('deny') at 4:5
Read ALL('all') at 4:10
Read SEMICOLON(';') at 4:13
Read LOCATION('location') at 6:5
Read PATH('/admin') at 6:14
Read LBRACE('{') at 6:21
Read ALLOW('allow') at 7:9
Read IPV4('192.168.1.10') at 7:15
Read SEMICOLON(';') at 7:27
Read DENY('deny') at 8:9
Read ALL('all') at 8:14
Read SEMICOLON(';') at 8:17
Read LOCATION('location') at 10:9
Read PATH('/admin/reports') at 10:18
Read LBRACE('{') at 10:33
Read ALLOW('allow') at 11:13
Read IPV4('192.168.1.20') at 11:19
Read SEMICOLON(';') at 11:31
Read DENY('deny') at 12:13
Read ALL('all') at 12:18
Read SEMICOLON(';') at 12:21
Read RBRACE('}') at 13:9
Read RBRACE('}') at 15:1
```
</details>

## Ambiguity Example
The supplied grammar RULES -> RULES RULES | RULE gives two parse trees for RULE1 RULE2 RULE3.
```text
((RULE1 RULE2) RULE3)
(RULE1 (RULE2 RULE3))
Corrected grammar: RULES -> RULE RULES | epsilon
```

## Runtime
| Stage | Seconds |
| --- | ---: |
| tokenizer | 0.000057 |
| dfa | 0.000016 |
| cfg | 0.000032 |
| pda | 0.000011 |
| tm | 0.000019 |

## Test Summary
Run pytest -v for the current test summary.

## Errors
Errors are shown in each model section above.
