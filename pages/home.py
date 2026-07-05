"""
pages/home.py
Toolkit dashboard featuring greeting, search quick links, and recent operations history.
"""

import streamlit as st
import pandas as pd
from utils.helpers import render_glass_card
from utils.export import export_to_txt, export_to_json, export_to_csv, export_to_pdf
import config

def show() -> None:
    # Header Banner
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image(config.LOGO_PATH, width=90)
    with col2:
        st.title(config.APP_NAME)
        st.caption(f"v{config.VERSION} | Cryptographically Secure & Modern Development Tools")
        
    st.markdown("---")
    
    # Overview Cards (Row 1)
    st.write("### Tool Modules Overview")
    r1_col1, r1_col2, r1_col3 = st.columns(3)
    
    with r1_col1:
        render_glass_card(
            "Encoders / Decoders",
            "Support for Base16/32/58/62/64/85, Morse code, URL percent encoding, HTML entities, and Punycode conversions.",
            "🔄"
        )
    with r1_col2:
        render_glass_card(
            "Classical Ciphers",
            "Run historic algorithms like Caesar, ROT13, ROT47, Atbash, Vigenère, Rail Fence, Bacon, Affine, and XOR ciphers.",
            "📜"
        )
    with r1_col3:
        render_glass_card(
            "Modern Cryptography",
            "Industry cryptosystems like AES (CBC/CTR/ECB), DES, 3DES, ChaCha20, and RSA asymmetric keys.",
            "🔑"
        )
        
    # Row 2
    r2_col1, r2_col2, r2_col3 = st.columns(3)
    with r2_col1:
        render_glass_card(
            "Hashes & Inspection",
            "Validate file and text integrity using MD5, SHA1/2/3, BLAKE2/3, and RIPEMD-160 algorithms.",
            "🧮"
        )
    with r2_col2:
        render_glass_card(
            "Utilities & QR",
            "Generate custom passwords with entropy meters, compile QR codes, and encode full binary files safely.",
            "🛠️"
        )
    with r2_col3:
        render_glass_card(
            "Auto Detect",
            "Analyze raw inputs with heuristics to guess their format and calculate confidence scores automatically.",
            "👁️"
        )
        
    st.markdown("---")
    
    # Session Operations History
    st.write("### 🕒 Recent Operations History")
    
    if "history" not in st.session_state or not st.session_state["history"]:
        st.info("No operations have been recorded yet. Perform encoding or decoding to populate history.")
    else:
        # Convert to DataFrame for visualization
        df = pd.DataFrame(st.session_state["history"])
        # Select columns to display
        df_display = df[["timestamp", "operation", "format", "input_len", "output_len", "input", "output"]]
        st.dataframe(df_display, use_container_width=True)
        
        # Export options
        st.write("#### Export Session History")
        exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
        
        history_list = st.session_state["history"]
        
        with exp_col1:
            txt_data = export_to_txt(history_list)
            st.download_button(
                label="📥 Export as TXT",
                data=txt_data,
                file_name="history.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        with exp_col2:
            json_data = export_to_json(history_list)
            st.download_button(
                label="📥 Export as JSON",
                data=json_data,
                file_name="history.json",
                mime="application/json",
                use_container_width=True
            )
            
        with exp_col3:
            csv_data = export_to_csv(history_list)
            st.download_button(
                label="📥 Export as CSV",
                data=csv_data,
                file_name="history.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with exp_col4:
            pdf_bytes = export_to_pdf(history_list)
            st.download_button(
                label="📥 Export as PDF",
                data=pdf_bytes,
                file_name="history.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
        if st.button("🧹 Clear History", type="secondary"):
            st.session_state["history"] = []
            st.rerun()
