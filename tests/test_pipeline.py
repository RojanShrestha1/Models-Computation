from pathlib import Path

from ruleshield.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]


def test_valid_end_to_end_and_order():
    data = run_pipeline((ROOT / "examples" / "valid_basic.conf").read_text())
    assert data["final"].accepted
    assert [r.model_name for r in data["results"]] == ["Tokenizer", "DFA", "CFG", "PDA", "High-level TM Decider"]


def test_every_invalid_example_rejects():
    for path in (ROOT / "examples").glob("invalid_*.conf"):
        data = run_pipeline(path.read_text())
        assert not data["final"].accepted, path.name


def test_error_propagation_and_no_crash():
    for text in ["@", "server { listen ; }", "}", "server { listen 0; }"]:
        data = run_pipeline(text)
        assert not data["final"].accepted
        assert data["final"].error_code


def test_policy_and_ambiguity_in_pipeline():
    text = (ROOT / "examples" / "valid_basic.conf").read_text()
    data = run_pipeline(text, {"client_ip": "10.0.0.5", "path": "/", "port": 80})
    assert data["policy"].accepted
    assert data["ambiguity"].accepted
