from __future__ import annotations

from dataclasses import dataclass, field

from .errors import TM_STEP_LIMIT
from .models import ValidationResult


@dataclass
class TuringMachine:
    transition_function: dict[tuple[str, str], tuple[str, str, str]]
    start_state: str
    accept_states: set[str]
    reject_states: set[str]
    blank: str = "_"
    max_steps: int = 1000

    def run(self, input_symbols: list[str] | str) -> ValidationResult:
        tape = list(input_symbols) if isinstance(input_symbols, str) else list(input_symbols)
        if not tape:
            tape = [self.blank]
        head = 0
        state = self.start_state
        trace: list[str] = []
        for step in range(self.max_steps + 1):
            if state in self.accept_states:
                return ValidationResult("Literal TM Engine", True, message="Machine halted in an accept state.", trace=trace, metadata={"final_state": state, "tape": "".join(tape), "head": head})
            if state in self.reject_states:
                return ValidationResult("Literal TM Engine", False, "TM_REJECT", "Machine halted in a reject state.", trace=trace, metadata={"final_state": state, "tape": "".join(tape), "head": head})
            if step == self.max_steps:
                return ValidationResult("Literal TM Engine", False, TM_STEP_LIMIT, "The machine exceeded its maximum step limit.", trace=trace, metadata={"final_state": state, "tape": "".join(tape), "head": head})
            if head < 0:
                tape.insert(0, self.blank)
                head = 0
            if head >= len(tape):
                tape.append(self.blank)
            read = tape[head]
            transition = self.transition_function.get((state, read))
            if transition is None:
                return ValidationResult("Literal TM Engine", False, "TM_REJECT", f"No transition exists for state {state} reading {read!r}.", trace=trace, metadata={"final_state": state, "tape": "".join(tape), "head": head})
            next_state, write, move = transition
            tape[head] = write
            trace.append(f"Step {step}: state={state}, read={read}, write={write}, move={move}, head={head}, tape={''.join(tape)}")
            state = next_state
            if move == "R":
                head += 1
            elif move == "L":
                head -= 1
            elif move == "S":
                pass
            else:
                return ValidationResult("Literal TM Engine", False, "TM_REJECT", f"Invalid movement {move!r}.", trace=trace)
        return ValidationResult("Literal TM Engine", False, TM_STEP_LIMIT, "The machine exceeded its maximum step limit.", trace=trace)


def normalized_symbol_demo_machine() -> TuringMachine:
    return TuringMachine(
        {
            ("q0", "S"): ("q1", "S", "R"),
            ("q1", "L"): ("q2", "L", "R"),
            ("q2", "A"): ("q_accept", "A", "S"),
        },
        "q0",
        {"q_accept"},
        {"q_reject"},
    )
