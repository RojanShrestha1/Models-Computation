from __future__ import annotations

from dataclasses import asdict

from .errors import CFG_SYNTAX_ERROR, INVALID_CONTEXT, UNKNOWN_DIRECTIVE
from .models import Config, Location, Rule, Server, Token, ValidationResult

GRAMMAR = """
CONFIG -> SERVER_BLOCK SERVER_LIST
SERVER_LIST -> SERVER_BLOCK SERVER_LIST | epsilon
SERVER_BLOCK -> server { SERVER_ITEMS }
SERVER_ITEMS -> SERVER_ITEM SERVER_ITEMS | epsilon
SERVER_ITEM -> LISTEN_STMT | ACCESS_STMT | LOCATION_BLOCK
LISTEN_STMT -> listen NUMBER ;
ACCESS_STMT -> ACTION TARGET ;
ACTION -> allow | deny
TARGET -> IPV4 | all
LOCATION_BLOCK -> location PATH { LOCATION_ITEMS }
LOCATION_ITEMS -> LOCATION_ITEM LOCATION_ITEMS | epsilon
LOCATION_ITEM -> ACCESS_STMT | LOCATION_BLOCK
"""


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
        self.productions: list[str] = []
        self.trace: list[str] = []

    @property
    def current(self) -> Token:
        return self.tokens[self.i]

    def error(self, code: str, message: str) -> ValidationResult:
        t = self.current
        return ValidationResult("CFG", False, code, message, t.line, t.column, self.trace, {"productions": self.productions, "grammar": GRAMMAR})

    def match(self, typ: str) -> Token | ValidationResult:
        t = self.current
        if t.type != typ:
            return self.error(CFG_SYNTAX_ERROR, f"Expected {typ}, but found {t.type} ({t.value!r}).")
        self.trace.append(f"Read {t.type}({t.value!r}) at {t.line}:{t.column}")
        self.i += 1
        return t

    def parse(self) -> tuple[Config | None, ValidationResult]:
        self.productions.append("CONFIG -> SERVER_BLOCK SERVER_LIST")
        config = Config()
        if self.current.type == "EOF":
            return None, self.error(CFG_SYNTAX_ERROR, "A configuration must contain at least one server block.")
        while self.current.type != "EOF":
            if self.current.type == "UNKNOWN":
                return None, self.error(UNKNOWN_DIRECTIVE, f"Unknown directive {self.current.value!r}.")
            if self.current.type != "SERVER":
                return None, self.error(CFG_SYNTAX_ERROR, "Only server blocks may appear at the top level.")
            server, result = self.server_block()
            if not result.accepted:
                return None, result
            config.servers.append(server)
        return config, ValidationResult(
            "CFG",
            True,
            message="Syntax accepted and AST produced.",
            trace=self.trace,
            metadata={
                "ast": asdict(config),
                "productions": self.productions,
                "grammar": GRAMMAR,
                "leftmost_derivation": sample_leftmost_derivation(),
                "parse_tree_vs_ast": "A parse tree shows every grammar step. An AST keeps the useful structure: servers, locations, listen ports and rules.",
            },
        )

    def server_block(self) -> tuple[Server, ValidationResult]:
        self.productions.append("SERVER_BLOCK -> server { SERVER_ITEMS }")
        start = self.match("SERVER")
        if isinstance(start, ValidationResult):
            return Server(), start
        lb = self.match("LBRACE")
        if isinstance(lb, ValidationResult):
            return Server(), lb
        server = Server(line=start.line, column=start.column)
        while self.current.type not in {"RBRACE", "EOF"}:
            if self.current.type == "LISTEN":
                port, result = self.listen_stmt()
                if not result.accepted:
                    return server, result
                server.listen.append(port)
            elif self.current.type in {"ALLOW", "DENY"}:
                rule, result = self.access_stmt()
                if not result.accepted:
                    return server, result
                server.rules.append(rule)
            elif self.current.type == "LOCATION":
                loc, result = self.location_block()
                if not result.accepted:
                    return server, result
                server.locations.append(loc)
            elif self.current.type == "UNKNOWN":
                return server, self.error(UNKNOWN_DIRECTIVE, f"Unknown directive {self.current.value!r}.")
            else:
                return server, self.error(CFG_SYNTAX_ERROR, f"{self.current.type} is not valid inside a server block.")
        rb = self.match("RBRACE")
        if isinstance(rb, ValidationResult):
            return server, rb
        return server, ValidationResult("CFG", True)

    def listen_stmt(self) -> tuple[int, ValidationResult]:
        self.productions.append("LISTEN_STMT -> listen NUMBER ;")
        res = self.match("LISTEN")
        if isinstance(res, ValidationResult):
            return 0, res
        num = self.match("NUMBER")
        if isinstance(num, ValidationResult):
            return 0, num
        semi = self.match("SEMICOLON")
        if isinstance(semi, ValidationResult):
            return 0, semi
        return int(num.value), ValidationResult("CFG", True)

    def access_stmt(self) -> tuple[Rule, ValidationResult]:
        self.productions.append("ACCESS_STMT -> ACTION TARGET ;")
        action = self.current
        if action.type not in {"ALLOW", "DENY"}:
            return Rule("", "", action.line, action.column), self.error(CFG_SYNTAX_ERROR, "Expected allow or deny.")
        self.i += 1
        self.trace.append(f"Read {action.type}({action.value!r}) at {action.line}:{action.column}")
        target = self.current
        if target.type not in {"IPV4", "ALL"}:
            code = UNKNOWN_DIRECTIVE if target.type == "UNKNOWN" and target.value.isalpha() else CFG_SYNTAX_ERROR
            return Rule(action.value, "", action.line, action.column), self.error(code, "Access target must be an IPv4 address or all.")
        self.i += 1
        self.trace.append(f"Read {target.type}({target.value!r}) at {target.line}:{target.column}")
        semi = self.match("SEMICOLON")
        if isinstance(semi, ValidationResult):
            return Rule(action.value, target.value, action.line, action.column), semi
        return Rule(action.value, target.value, action.line, action.column), ValidationResult("CFG", True)

    def location_block(self) -> tuple[Location, ValidationResult]:
        self.productions.append("LOCATION_BLOCK -> location PATH { LOCATION_ITEMS }")
        start = self.match("LOCATION")
        if isinstance(start, ValidationResult):
            return Location(""), start
        path = self.match("PATH")
        if isinstance(path, ValidationResult):
            return Location(""), path
        lb = self.match("LBRACE")
        if isinstance(lb, ValidationResult):
            return Location(path.value), lb
        loc = Location(path.value, line=start.line, column=start.column)
        while self.current.type not in {"RBRACE", "EOF"}:
            if self.current.type == "LISTEN":
                return loc, self.error(INVALID_CONTEXT, "listen is only valid inside server, not inside location.")
            if self.current.type in {"ALLOW", "DENY"}:
                rule, result = self.access_stmt()
                if not result.accepted:
                    return loc, result
                loc.rules.append(rule)
            elif self.current.type == "LOCATION":
                child, result = self.location_block()
                if not result.accepted:
                    return loc, result
                loc.locations.append(child)
            elif self.current.type == "UNKNOWN":
                return loc, self.error(UNKNOWN_DIRECTIVE, f"Unknown directive {self.current.value!r}.")
            else:
                return loc, self.error(CFG_SYNTAX_ERROR, f"{self.current.type} is not valid inside a location block.")
        rb = self.match("RBRACE")
        if isinstance(rb, ValidationResult):
            return loc, rb
        return loc, ValidationResult("CFG", True)


def parse_tokens(tokens: list[Token]) -> tuple[Config | None, ValidationResult]:
    return Parser(tokens).parse()


def sample_leftmost_derivation() -> list[str]:
    return [
        "CONFIG",
        "SERVER_BLOCK SERVER_LIST",
        "server { SERVER_ITEMS } SERVER_LIST",
        "server { LISTEN_STMT SERVER_ITEMS } SERVER_LIST",
        "server { listen NUMBER ; SERVER_ITEMS } SERVER_LIST",
        "server { listen NUMBER ; epsilon } epsilon",
    ]
