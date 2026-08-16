# Complexity Analysis

| Component        | Expected time                           | Extra space              |
| ---------------- | --------------------------------------: | -----------------------: |
| Tokenizer        | `O(n)`                                  | `O(n)`                   |
| DFA              | `O(n)`                                  | `O(1)` excluding trace    |
| CFG              | `O(n)`                                  | `O(d)` recursion          |
| PDA              | `O(n)`                                  | `O(d)` stack              |
| TM               | Based on its real number of tape sweeps | Tape-dependent            |
| Policy evaluator | Based on servers, locations and rules   | AST-dependent             |

`n` is the number of input characters or tokens depending on the component. `d` is block nesting depth.

The TM engine is step-count based because Turing Machine runtime depends on the supplied transition function and tape behavior.
