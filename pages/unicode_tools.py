"""
pages/unicode_tools.py
UI page for Unicode escape conversions and Character Inspector.
"""

import streamlit as st
import unicodedata
import pandas as pd
from modules.unicode import UnicodeCoder
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js

def show() -> None:
    st.title("🔤 Unicode Tools")
    st.caption("Escape unicode sequences or inspect character metadata (names, categories, points).")
    st.markdown("---")
    
    coder = UnicodeCoder()
    
    tab_esc, tab_inspect = st.tabs(["🔄 Escape / Unescape", "🔍 Character Inspector"])
    
    with tab_esc:
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Input")
            direction = st.radio("Direction", ["Escape", "Unescape"], key="uni_tool_dir")
            input_text = st.text_area("Source Text", height=180, key="uni_tool_input", placeholder="Escape: Hello 🚀\nUnescape: Hello \\U0001f680")
            show_char_counter(input_text)
            
            with st.expander("Settings", expanded=True):
                format_type = st.selectbox("Escape Format", ["Escape Sequence", "Code Points"], key="uni_tool_fmt")
                
        with col2:
            st.write("### Output")
            output_text = ""
            error_msg = ""
            
            if input_text:
                try:
                    if direction == "Escape":
                        output_text = coder.encode(input_text, format_type=format_type)
                    else:
                        output_text = coder.decode(input_text, format_type=format_type)
                except Exception as e:
                    error_msg = str(e)
                    
            if error_msg:
                st.error(error_msg)
            elif output_text:
                st.code(output_text, language="text")
                show_char_counter(output_text)
                
                # Copy & Download
                copy_to_clipboard_js(output_text, "uni_tool_out")
                st.download_button("📥 Download Output", output_text, file_name="unicode_tool_output.txt", mime="text/plain")
                
                # History log
                if st.session_state.get("last_recorded_uni_tool") != (input_text, direction):
                    record_history(f"Unicode {direction}", input_text, output_text, "Unicode")
                    st.session_state["last_recorded_uni_tool"] = (input_text, direction)
            else:
                st.info("Input unicode strings to start escape conversions.")
                
            if st.button("🧹 Clear Input", key="clear_uni_tool"):
                st.session_state["uni_tool_input"] = ""
                st.rerun()
                
    with tab_inspect:
        st.write("### Character Inspector")
        inspect_input = st.text_input("Enter characters to inspect", value="Hello 🛠️")
        
        if inspect_input:
            records = []
            for i, char in enumerate(inspect_input):
                codepoint_dec = ord(char)
                codepoint_hex = f"U+{codepoint_dec:04X}"
                
                # Retrieve Unicode name
                try:
                    name = unicodedata.name(char)
                except ValueError:
                    name = "<Unknown Character Name>"
                    
                # Retrieve category
                category = unicodedata.category(char)
                
                records.append({
                    "Index": i,
                    "Character": char,
                    "Code Point (Dec)": codepoint_dec,
                    "Code Point (Hex)": codepoint_hex,
                    "Category Code": category,
                    "Unicode Name": name
                })
                
            df_inspect = pd.DataFrame(records)
            st.dataframe(df_inspect, use_container_width=True)
            st.info("Category codes correspond to Unicode database classifications (e.g. Lu = Letter uppercase, Ll = Letter lowercase, So = Symbol other).")
