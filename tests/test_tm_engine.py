from ruleshield.tm_engine import TuringMachine, normalized_symbol_demo_machine


def test_demo_machine_accepts_normalized_symbols():
    result = normalized_symbol_demo_machine().run("SLA")
    assert result.accepted
    assert "Step 0" in result.trace[0]


def test_write_move_left_right_expansion_blank():
    tm = TuringMachine(
        {
            ("q0", "a"): ("q1", "b", "L"),
            ("q1", "_"): ("q2", "x", "R"),
            ("q2", "b"): ("qa", "b", "S"),
        },
        "q0",
        {"qa"},
        {"qr"},
    )
    result = tm.run("a")
    assert result.accepted
    assert result.metadata["tape"].startswith("xb")


def test_reject_halting_missing_transition_step_limit_and_repeatability():
    reject_tm = TuringMachine({("q0", "a"): ("qr", "a", "S")}, "q0", {"qa"}, {"qr"})
    assert not reject_tm.run("a").accepted
    missing = TuringMachine({}, "q0", {"qa"}, {"qr"}).run("a")
    assert missing.error_code == "TM_REJECT"
    loop = TuringMachine({("q0", "a"): ("q0", "a", "S")}, "q0", {"qa"}, {"qr"}, max_steps=2)
    assert loop.run("a").error_code == "TM_STEP_LIMIT"
    assert normalized_symbol_demo_machine().run("SLA").trace == normalized_symbol_demo_machine().run("SLA").trace
