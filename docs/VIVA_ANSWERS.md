# Viva Answers

1. What problem does RuleShield solve?
Short: It checks a simplified NGINX access-control file. Detail: It shows which errors are lexical, syntactic, structural or semantic.

2. Is NGINX a firewall?
Short: No. Detail: NGINX is mainly a web server, reverse proxy and load balancer with access-control features.

3. Does real NGINX directly use our DFA, PDA and TM?
Short: No. Detail: These are educational models.

4. Why did we choose NGINX configuration?
Short: It has clear tokens, blocks and rules. Detail: That makes it useful for teaching automata.

5. What is the DFA checking?
Short: Local directive patterns. Detail: It checks units like `listen NUMBER ;`.

6. Why can the DFA not validate arbitrary nesting?
Short: It has no stack. Detail: Unlimited nesting needs memory beyond finite states.

7. What is the CFG checking?
Short: Grammar. Detail: It checks whether server and location blocks follow the language rules.

8. What is grammar ambiguity?
Short: One input has more than one parse tree. Detail: The same token sequence can be grouped in different valid ways.

9. Why is the original grammar ambiguous?
Short: `RULES RULES` can split the list in different places. Detail: `RULE1 RULE2 RULE3` can group left or right.

10. How did we remove ambiguity?
Short: Use right recursion. Detail: `RULES -> RULE RULES | epsilon` gives one predictable list shape.

11. Why does the PDA need a stack?
Short: To remember open blocks. Detail: Each `{` pushes and each `}` pops.

12. What is pushed and popped?
Short: `SERVER` and `LOCATION`. Detail: `$` stays as the bottom marker.

13. What extra work does the Turing Machine perform?
Short: Semantic checks. Detail: Ports, IPv4 values, duplicates and unreachable rules.

14. What is the difference between the literal TM and high-level decider?
Short: One uses explicit transitions; the other is readable phases. Detail: The decider is TM-style but not a full low-level encoding.

15. Why is the code modular?
Short: Each theory concept is separate. Detail: This makes testing and explanation clearer.

16. What happens when a port is invalid?
Short: The TM decider rejects. Detail: Ports must be 1 through 65535.

17. What happens when an IP is invalid?
Short: The TM decider rejects. Detail: IPv4 must have four octets from 0 to 255, with no leading zeros.

18. Why is a rule after `deny all` unreachable?
Short: `all` matches every client. Detail: First-match evaluation means later rules cannot run.

19. What are the time and space complexities?
Short: Most stages are linear. Detail: PDA/CFG need nesting memory, and TM depends on steps.

20. What are the project limitations?
Short: It is not full NGINX. Detail: It is a teaching language with simplified semantics.

21. How were the test cases designed?
Short: One group per component. Detail: Tests cover valid behavior and common failures.

22. What result proves the increasing capabilities of the models?
Short: DFA can accept while CFG/PDA/TM reject. Detail: A missing outer brace shows DFA's limitation and PDA's stack power.
