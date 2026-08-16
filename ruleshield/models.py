from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Token:
    type: str
    value: str
    line: int
    column: int
    offset: int


@dataclass
class ValidationResult:
    model_name: str
    accepted: bool
    error_code: str | None = None
    message: str = ""
    line: int | None = None
    column: int | None = None
    trace: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Rule:
    action: str
    target: str
    line: int
    column: int


@dataclass
class Location:
    path: str
    rules: list[Rule] = field(default_factory=list)
    locations: list["Location"] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class Server:
    listen: list[int] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
    locations: list[Location] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class Config:
    servers: list[Server] = field(default_factory=list)

