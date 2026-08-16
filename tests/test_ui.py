import pytest
from pathlib import Path

streamlit = pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_ui_widgets_and_valid_accept():
    at = AppTest.from_file(APP).run()
    assert at.text_area
    assert any("Validate Configuration" in b.label for b in at.button)
    at.button[4].click().run(timeout=10)
    assert any("ACCEPT" in x.value for x in at.success)
    assert at.download_button


def test_ui_invalid_reject_sections():
    at = AppTest.from_file(APP).run()
    at.text_area[0].set_value("server { listen ; }")
    at.button[4].click().run(timeout=10)
    assert any("REJECT" in x.value for x in at.error)
    text = "\n".join(str(x.value) for x in at.markdown)
    assert "DFA" in text or "CFG" in text
