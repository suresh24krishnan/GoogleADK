import streamlit as st
import pandas as pd
import re
import secrets
from datetime import datetime
from core.ghost.proxy import GhostProxy
from sentinel.jira_bridge import JiraBridge

# --- PAGE CONFIG ---
st.set_page_config(page_title="Project Ghost: Control Center", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        border-radius: 8px;
        height: 3.5em;
        transition: all 0.2s ease-in-out;
        border: 1px solid #4a4a4a;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    div.stButton > button:hover {
        border-color: #00ff00;
        color: #00ff00;
        box-shadow: 0 0 12px rgba(0, 255, 0, 0.15);
    }
    .status-success { color: #00ff00; font-weight: bold; }
    .status-critical { color: #ff4b4b; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE LOGIC ---
if 'ghost' not in st.session_state:
    st.session_state.ghost = GhostProxy()
if 'bridge' not in st.session_state:
    st.session_state.bridge = JiraBridge()
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'sim_token' not in st.session_state:
    st.session_state.sim_token = f"PERSON_{secrets.token_hex(3).upper()}"
if 'sim_status' not in st.session_state:
    st.session_state.sim_status = None
if 'last_shadowed' not in st.session_state:
    st.session_state.last_shadowed = None
if 'jira_feedback' not in st.session_state:
    st.session_state.jira_feedback = None
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def add_log(event, details, status="INFO"):
    st.session_state.logs.insert(0, {
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Event": event,
        "Details": details,
        "Status": status
    })

def color_status(val):
    if val == "SUCCESS" or val == "SECURE":
        return 'color: #00ff00; font-weight: bold'
    elif val == "CRITICAL":
        return 'color: #ff4b4b; font-weight: bold'
    return ''

st.title("👻 Project Ghost: Zero-Knowledge Neuro-Mesh")

# --- SYSTEM GOVERNANCE OVERVIEW & HELP ---
with st.expander("ℹ️ Help & System Governance", expanded=False):
    st.markdown("""
    ### 🛠️ Quick Start Guide
    1. **Cloaking**: Enter text in **Ingress**. The system replaces PII with tokens (e.g., `PERSON_A1B2`).
    2. **Rehydration**: If the token is recognized in the **Identity Vault**, the real name returns in **Egress**.
    3. **Sentinel Loop**: If a token is "leaked" (unrecognized), Sentinel creates a Jira ticket. 
    4. **Resolution**: Once you authorize a token in the sidebar, Sentinel **self-heals** by closing or escalating the ticket based on the situation [cite: 2026-01-08].
    """)

st.markdown("---")

# --- SIDEBAR: SENTINEL WATCHTOWER ---
with st.sidebar:
    st.header("🛰️ Sentinel Watchtower")
    
    if st.button("🛰️ Run System Audit", use_container_width=True, help="Scans Jira for open leaks and closes them if they've been authorized in the Vault."):
        add_log("Sentinel Audit", "Scanning Jira for state mismatch...", "AUDIT")
        with st.spinner("Analyzing SEN Board..."):
            jql = f'project = "{st.session_state.bridge.project_key}" AND statusCategory != "Done"'
            issues = st.session_state.bridge.client.search_issues(jql)
            if issues:
                for issue in issues:
                    match = re.search(r"[A-Z0-9]+_[A-Z0-9]+", issue.fields.summary)
                    if match and st.session_state.ghost.vault.is_token_valid(match.group()):
                        st.session_state.bridge.auto_close_resolved_issues(match.group())
                        add_log("Self-Heal", f"Closed {issue.key}", "SUCCESS")
                st.toast("Jira Audit Complete!", icon="🚀")
            else:
                st.success("No active PII leaks detected.")

    st.markdown("---")
    st.header("🔑 Identity Vault")
    
    with st.expander("Resolve Alias Mapping", expanded=True):
        unmapped_id = st.text_input(
            "Alias ID (IDP)", 
            placeholder="e.g. PERSON_A1B2C3", 
            key=f"alias_id_{st.session_state.reset_counter}",
            help="The Ghost Token you want to authorize or block."
        )
        real_value = st.text_input(
            "Entity Identity", 
            placeholder="Real name", 
            key=f"real_id_{st.session_state.reset_counter}",
            help="The real identity that should replace the token."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✅ AUTHORIZE IDENTITY", use_container_width=True, help="Verify this identity and close associated Jira tickets."):
            if unmapped_id and real_value:
                st.session_state.ghost.vault.add_mapping(real_value, unmapped_id)
                st.session_state.bridge.auto_close_resolved_issues(unmapped_id, comment="✨ Sentinel: Authorized.")
                st.session_state.jira_feedback = f"✅ Resolved: {unmapped_id} is now Authorized."
                add_log("Identity Resolution", f"Mapped {unmapped_id}", "SUCCESS")
                st.rerun()
            else:
                st.warning("⚠️ Enter both Alias ID and Entity Identity to authorize.")

        st.markdown("<div style='text-align: center; margin: 10px 0; color: #888;'>— OR —</div>", unsafe_allow_html=True)

        if st.button("🚫 RESTRICT ACCESS", use_container_width=True, help="Block this token and close Jira ticket as Restricted."):
            if unmapped_id:
                st.session_state.ghost.vault.add_mapping("🚫 [RESTRICTED]", unmapped_id)
                st.session_state.bridge.auto_close_resolved_issues(unmapped_id, comment="🚨 Sentinel: Restricted.")
                st.session_state.jira_feedback = f"🚫 Blocked: {unmapped_id} Restricted & Ticket Closed."
                add_log("Security Restriction", f"Restricted: {unmapped_id}", "CRITICAL")
                st.rerun()
            else:
                st.error("🚨 Alias ID (IDP) is needed for Restrict access.")
        
        st.caption("Note: Enter the Alias ID (IDP) above to restrict access to a specific token.")

    if st.session_state.jira_feedback:
        st.info(st.session_state.jira_feedback)

    st.markdown("---")
    if st.button("🔄 FULL SYSTEM RESET", use_container_width=True, help="Wipes all local logs, clears the Identity Vault, and resets the Jira Bridge."):
        for key in list(st.session_state.keys()):
            if key != 'reset_counter':
                del st.session_state[key]
        st.session_state.reset_counter += 1
        st.session_state.ghost = GhostProxy()
        st.session_state.bridge = JiraBridge()
        st.session_state.logs = []
        st.rerun()

# --- MAIN INTERACTION ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Ingress: Raw Prompt")
    user_input = st.text_area(
        "Secure Input Field:", 
        "Draft a notice for Suresh Krishnan at suresh@example.com.", 
        height=150,
        key=f"ingress_{st.session_state.reset_counter}"
    )
    
    if st.button("Initiate Identity Transformation", use_container_width=True):
        st.session_state.last_shadowed = st.session_state.ghost.cloak(user_input)
        add_log("Identity Transformation", "De-identification completed.", "SECURE")
    
    if st.session_state.last_shadowed:
        st.write("**Cloaked Identity Output:**")
        st.code(st.session_state.last_shadowed, language="text")

with col2:
    st.subheader("🔓 Egress: De-identified Result")
    if st.session_state.last_shadowed:
        mock_reply = f"The Neuro-Mesh has processed the request for {st.session_state.last_shadowed}."
        final_output = st.session_state.ghost.reveal(mock_reply)
        st.info(f"**Final Restored Result:**\n\n{final_output}")
        
        st.markdown("---")
        st.subheader("🚨 Sentinel Governance Simulation")
        if st.button("🔥 Simulate Hallucination Event", use_container_width=True, help="Force a leak detection to trigger a new Jira ticket."):
            status_data = st.session_state.bridge.handle_rehydration_failure(st.session_state.sim_token)
            st.session_state.sim_status = status_data[0] if isinstance(status_data, tuple) else status_data
            
            if "Created" in st.session_state.sim_status:
                add_log("Leak Detected", f"Hallucination: {st.session_state.sim_token}", "CRITICAL")
            else:
                add_log("Escalation", f"Repeated Leak: {st.session_state.sim_token}", "CRITICAL")

        if st.session_state.sim_status:
            if "Escalated" in st.session_state.sim_status or "Repeated" in st.session_state.sim_status:
                st.error(f"🚨 {st.session_state.sim_status}")
            else:
                st.warning(f"🛰️ Sentinel Notification: {st.session_state.sim_status}")

# --- LIVE TRAFFIC MONITOR ---
st.markdown("---")
log_header_col1, log_header_col2 = st.columns([0.85, 0.15])
with log_header_col1:
    st.subheader("📟 Live Network Traffic & Sentinel Logs")
with log_header_col2:
    if st.button("🗑️ Clear Logs", use_container_width=True):
        st.session_state.logs = []
        st.rerun()

if st.session_state.logs:
    log_df = pd.DataFrame(st.session_state.logs)
    st.table(log_df.style.map(color_status, subset=['Status']))