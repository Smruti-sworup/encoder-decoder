"""
pages/jwt_tools.py
UI page for JSON Web Token (JWT) inspection, decoding, and verification.
"""

import streamlit as st
import json
from modules.jwt import JWTTool
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js

def show() -> None:
    st.title("🔑 JWT Tools")
    st.caption("Inspect and verify JSON Web Tokens (JWT). Decodes headers and payloads, and performs signature validation.")
    st.markdown("---")
    
    jwt_tool = JWTTool()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Input Token")
        token = st.text_area("Paste JWT Token", height=180, key="jwt_input_area", placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        show_char_counter(token)
        
        st.write("### Signature Verification")
        with st.expander("Configure Verification Key", expanded=True):
            secret_key = st.text_input("Symmetric Secret or Public Key (PEM)", type="password", help="For algorithms like HS256, enter the shared secret. For RS256, enter the PEM public key.")
            
            # Check algorithm
            alg_options = ["Detect from Header", "HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "ES256", "ES384", "ES512"]
            selected_alg = st.selectbox("Algorithm", alg_options)
            
            trigger_verify = st.button("Verify Signature", type="primary")
            
    with col2:
        st.write("### Token Details")
        
        if token:
            success, header, payload, error_msg = jwt_tool.decode_unverified(token)
            
            if not success:
                st.error(error_msg)
            else:
                # Expiration analysis
                exp_analysis = jwt_tool.check_expiration(payload)
                
                # Active Status Alert
                if exp_analysis["has_exp"]:
                    if exp_analysis["expired"]:
                        st.error(f"🔴 Token Expired at {exp_analysis['exp_date']}")
                    else:
                        st.success(f"🟢 Token Active. Remaining: {exp_analysis['time_remaining']}")
                else:
                    st.warning("⚠️ Token has no expiration ('exp') claim.")
                    
                # Signature verification outcome
                if trigger_verify:
                    if not secret_key:
                        st.error("Please provide a Verification Key inside the expander.")
                    else:
                        algs = None if selected_alg == "Detect from Header" else [selected_alg]
                        valid, verify_msg = jwt_tool.verify_token(token, secret_key, algs)
                        if valid:
                            st.success(f"✔️ {verify_msg}")
                        else:
                            st.error(f"❌ {verify_msg}")
                            
                # Tabs for Header and Payload
                tab_payload, tab_header = st.tabs(["📄 Payload (Claims)", "header Header"])
                
                with tab_header:
                    st.json(header)
                    copy_to_clipboard_js(json.dumps(header, indent=2), "jwt_header")
                    
                with tab_payload:
                    st.json(payload)
                    copy_to_clipboard_js(json.dumps(payload, indent=2), "jwt_payload")
                    
                # History log
                if st.session_state.get("last_recorded_jwt") != token:
                    record_history("JWT Inspect", token[:100] + "...", f"Header: {header.get('alg', 'None')}", "JWT")
                    st.session_state["last_recorded_jwt"] = token
        else:
            st.info("Paste a JSON Web Token on the left to inspect its contents.")
            
        if st.button("🧹 Clear Input", key="clear_jwt"):
            st.session_state["jwt_input_area"] = ""
            st.rerun()
