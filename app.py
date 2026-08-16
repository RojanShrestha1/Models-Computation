from __future__ import annotations

from pathlib import Path

import streamlit as st

from ruleshield.pipeline import run_pipeline
from ruleshield.report_generator import generate_report

ROOT = Path(__file__).parent


def load_example(name: str) -> str:
    return (ROOT / "examples" / name).read_text(encoding="utf-8")


st.set_page_config(page_title="RuleShield", layout="wide")
st.title("RuleShield: Automata-Based NGINX Access-Control Validator")
st.caption("Educational DFA, CFG, PDA and Turing Machine model for a simplified NGINX access-control language.")

if "config_text" not in st.session_state:
    st.session_state.config_text = load_example("valid_basic.conf")

cols = st.columns(4)
if cols[0].button("Load valid_basic"):
    st.session_state.config_text = load_example("valid_basic.conf")
if cols[1].button("Load valid_nested"):
    st.session_state.config_text = load_example("valid_nested.conf")
if cols[2].button("Load invalid_semicolon"):
    st.session_state.config_text = load_example("invalid_semicolon.conf")
if cols[3].button("Load invalid_context"):
    st.session_state.config_text = load_example("invalid_context.conf")

config_text = st.text_area("NGINX configuration", key="config_text", height=300)

with st.expander("Optional policy test", expanded=True):
    pcols = st.columns(3)
    client_ip = pcols[0].text_input("Client IPv4", "192.168.1.10")
    request_path = pcols[1].text_input("Path", "/admin")
    request_port = pcols[2].number_input("Port", min_value=1, max_value=65535, value=80)
    run_policy = st.checkbox("Run policy evaluator", value=True)

if st.button("Validate Configuration", type="primary"):
    policy = {"client_ip": client_ip, "path": request_path, "port": int(request_port)} if run_policy else None
    data = run_pipeline(config_text, policy)
    final = data["final"]
    if final.accepted:
        st.success("ACCEPT")
    else:
        st.error("REJECT")
        st.write(f"Error: `{final.error_code}` at {final.line}:{final.column}")
        st.write(final.message)

    st.subheader("Tokens")
    st.dataframe([t.__dict__ for t in data["tokens"]], width="stretch")

    for result in data["results"]:
        st.subheader(result.model_name)
        st.write("ACCEPT" if result.accepted else f"REJECT: {result.error_code}")
        if result.message:
            st.write(result.message)
        with st.expander("Transition trace"):
            st.code("\n".join(result.trace[:300]) or "No trace")
        if result.model_name == "CFG":
            st.write("Productions")
            st.code("\n".join(result.metadata.get("productions", [])))
            st.write("Leftmost derivation")
            st.code("\n".join(result.metadata.get("leftmost_derivation", [])))

    st.subheader("Ambiguity demonstration")
    st.code("\n".join(data["ambiguity"].trace))

    if data.get("policy"):
        st.subheader("Policy result")
        st.write(data["policy"].message)
        st.code("\n".join(data["policy"].trace))

    st.subheader("State diagrams")
    for name in ["dfa.dot", "cfg.dot", "pda.dot", "turing_machine.dot"]:
        st.code((ROOT / "diagrams" / name).read_text(encoding="utf-8"), language="dot")

    report = generate_report(data, config_text)
    st.download_button("Download validation_report.md", report, file_name="validation_report.md")
