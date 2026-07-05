"""
pages/text_converter.py
UI page for Text & Unicode conversion (ASCII, Unicode, UTF-8, UTF-16, UTF-32).
Shows multi-format output dashboard.
"""

import streamlit as st
from modules.unicode import UnicodeCoder
from modules.ascii import ASCCIICoder
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js

def show() -> None:
    st.title("🔤 Text & Unicode Converter")
    st.caption("Inspect how a string of text represents across multiple standards: ASCII, UTF-8, UTF-16, UTF-32, and Unicode Code Points.")
    st.markdown("---")
    
    uni_coder = UnicodeCoder()
    ascii_coder = ASCCIICoder()
    
    input_text = st.text_area("Source Text", height=150, key="text_input_area", placeholder="Type Unicode text (e.g. Hello 🚀)")
    show_char_counter(input_text)
    
    st.markdown("---")
    
    if input_text:
        st.write("### Multi-Encoding Inspection Panel")
        
        # We will generate representations
        col1, col2 = st.columns(2)
        
        with col1:
            # UTF-8 hex
            st.markdown("#### 🔹 UTF-8 Bytes (Hex)")
            utf8_bytes = uni_coder.encode(input_text, format_type="Hex Bytes", encoding="utf-8")
            st.code(utf8_bytes, language="text")
            copy_to_clipboard_js(utf8_bytes, "conv_utf8")
            
            # UTF-16 hex
            st.markdown("#### 🔹 UTF-16 Bytes (Hex)")
            utf16_bytes = uni_coder.encode(input_text, format_type="Hex Bytes", encoding="utf-8" if not input_text else "", encoding_type_kwarg_fake="utf-16") # wait! the argument name in unicode.py is encoding
            utf16_bytes = uni_coder.encode(input_text, format_type="Hex Bytes", encoding="utf-16")
            st.code(utf16_bytes, language="text")
            copy_to_clipboard_js(utf16_bytes, "conv_utf16")
            
            # UTF-32 hex
            st.markdown("#### 🔹 UTF-32 Bytes (Hex)")
            utf32_bytes = uni_coder.encode(input_text, format_type="Hex Bytes", encoding="utf-32")
            st.code(utf32_bytes, language="text")
            copy_to_clipboard_js(utf32_bytes, "conv_utf32")
            
        with col2:
            # ASCII Ordinals
            st.markdown("#### 🔹 ASCII Ordinals")
            try:
                ascii_ords = ascii_coder.encode(input_text, mode="ordinals")
                st.code(ascii_ords if ascii_ords else "Contains only non-ASCII characters.", language="text")
                if ascii_ords:
                    copy_to_clipboard_js(ascii_ords, "conv_ascii")
            except Exception as e:
                st.error(str(e))
                
            # Unicode Escape
            st.markdown("#### 🔹 Unicode Escape Sequence")
            uni_escape = uni_coder.encode(input_text, format_type="Escape Sequence")
            st.code(uni_escape, language="text")
            copy_to_clipboard_js(uni_escape, "conv_escape")
            
            # Unicode Code Points
            st.markdown("#### 🔹 Unicode Code Points (U+XXXX)")
            uni_pts = uni_coder.encode(input_text, format_type="Code Points")
            st.code(uni_pts, language="text")
            copy_to_clipboard_js(uni_pts, "conv_points")
            
        # Log to history
        if st.session_state.get("last_recorded_text_conv") != input_text:
            record_history("Multi-Text-Convert", input_text, f"UTF8: {utf8_bytes[:30]}...", "Unicode")
            st.session_state["last_recorded_text_conv"] = input_text
    else:
        st.info("Provide input text above to view multi-format encoding maps.")
        
    if st.button("🧹 Clear Input", key="clear_text_conv"):
        st.session_state["text_input_area"] = ""
        st.rerun()
