"""
pages/auto_detect.py
UI for format auto-detection and confidence analyzer.
"""

import streamlit as st
import pandas as pd
from modules.auto_detector import AutoDetector
from utils.helpers import show_char_counter

def show() -> None:
    st.title("👁️ Auto-Detect Input Format")
    st.caption("Paste an unknown string, token, or ciphertext. The toolkit will analyze structure to estimate its source encoding.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    detector = AutoDetector()
    
    with col1:
        st.write("### Input")
        input_text = st.text_area("Paste Unknown Data", height=250, key="detect_input_area", placeholder="e.g. SGVsbG8gV29ybGQh or 0x48656c6c6f or [JWT token]")
        show_char_counter(input_text)
        
    with col2:
        st.write("### Detection Analysis Results")
        
        if input_text:
            detections = detector.detect(input_text)
            
            # Format display
            df = pd.DataFrame(detections)
            df["Confidence %"] = (df["confidence"] * 100).round(1).astype(str) + "%"
            
            # Show top hit inside alert box
            top_hit = detections[0]
            st.success(f"**Top Match:** {top_hit['format']} ({top_hit['confidence']*100:.1f}% confidence)")
            
            # Draw bar chart of results
            chart_df = pd.DataFrame({
                "Format": [d["format"] for d in detections if d["confidence"] > 0.1],
                "Confidence": [d["confidence"] for d in detections if d["confidence"] > 0.1]
            }).set_index("Format")
            st.bar_chart(chart_df)
            
            # Table details
            st.table(df[["format", "Confidence %", "description"]])
            
            # Action button: direct link to Decoder
            st.markdown("### 🛠️ Decode Now")
            best_match_name = top_hit['format']
            # Map name to decoder names if needed
            decoder_map = {
                "JSON Web Token (JWT)": "JWT Tools",
                "Hexadecimal": "Base16",
                "Binary Representation": "Binary",
                "Octal Representation": "Octal",
                "Decimal Byte Representation": "Decimal",
                "URL Percent Encoding": "URL Decoding",
                "HTML Entity Encoding": "HTML Entity",
                "Base64": "Base64",
                "Base32": "Base32",
                "Base58": "Base58",
                "Morse Code": "Morse Code",
                "Plain Text (UTF-8)": "ASCII"
            }
            
            target_page_or_format = decoder_map.get(best_match_name, "ASCII")
            
            # To handle routing in app.py we can set state and trigger rerun
            if st.button(f"🔓 Load in Decoder as {target_page_or_format}", type="primary"):
                st.session_state["nav_selection"] = "String Decoder" if "Decoder" in target_page_or_format or target_page_or_format in ["Base64", "Base32", "Base58", "Base16", "Hexadecimal", "Binary", "Octal", "Decimal", "Morse Code", "ASCII", "URL Decoding", "HTML Entity"] else target_page_or_format
                st.session_state["dec_input_area"] = input_text
                st.session_state["decoder_format_preselect"] = target_page_or_format
                st.success(f"Preloaded input! Switch to {st.session_state['nav_selection']} in sidebar.")
                st.rerun()
        else:
            st.info("Paste data on the left to analyze formats.")
            
        if st.button("🧹 Clear", type="secondary"):
            st.session_state["detect_input_area"] = ""
            st.rerun()
