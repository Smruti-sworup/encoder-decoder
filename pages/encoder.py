"""
pages/encoder.py
Unified UI page for string/data encoding operations.
"""

import streamlit as st
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js
import config

# Import modules
from modules.base16 import Base16Coder
from modules.base32 import Base32Coder
from modules.base58 import Base58Coder
from modules.base62 import Base62Coder
from modules.base64 import Base64Coder
from modules.base64url import Base64UrlCoder
from modules.base85 import Base85Coder
from modules.ascii85 import ASCII85Coder
from modules.binary import BinaryCoder
from modules.octal import OctalCoder
from modules.decimal import DecimalCoder
from modules.hexadecimal import HexadecimalCoder
from modules.ascii import ASCCIICoder
from modules.unicode import UnicodeCoder
from modules.url import URLCoder
from modules.html import HTMLCoder
from modules.punycode import PunycodeCoder
from modules.morse import MorseCoder

# Instantiations
CODERS = {
    "Base16": Base16Coder(),
    "Base32": Base32Coder(),
    "Base58": Base58Coder(),
    "Base62": Base62Coder(),
    "Base64": Base64Coder(),
    "Base64 URL": Base64UrlCoder(),
    "Base85": Base85Coder(),
    "ASCII85": ASCII85Coder(),
    "Binary": BinaryCoder(),
    "Octal": OctalCoder(),
    "Decimal": DecimalCoder(),
    "Hexadecimal": HexadecimalCoder(),
    "ASCII": ASCCIICoder(),
    "Unicode": UnicodeCoder(),
    "URL Encoding": URLCoder(),
    "HTML Entity": HTMLCoder(),
    "Punycode": PunycodeCoder(),
    "Morse Code": MorseCoder(),
}

def show() -> None:
    st.title("🔄 Text Encoder")
    st.caption("Convert raw strings into multiple base, format, or standard representations.")
    st.markdown("---")
    
    # Selection of encoding
    encoder_format = st.selectbox("Select Target Encoding Format", list(CODERS.keys()))
    
    col1, col2 = st.columns(2)
    
    # Advanced Options Expander
    params = {}
    with col1:
        st.write("### Input")
        # Text Area input
        input_text = st.text_area("Plain Text to Encode", height=200, key="enc_input_area")
        show_char_counter(input_text)
        
        # Format-specific advanced settings
        with st.expander("Advanced Configuration Options", expanded=True):
            if encoder_format == "Hexadecimal":
                params["delimiter"] = st.text_input("Byte Delimiter", value=" ")
                params["prefix"] = st.text_input("Byte Prefix", value="")
            elif encoder_format == "ASCII":
                params["mode"] = st.selectbox("ASCII Mode", ["ordinals", "sanitize"])
            elif encoder_format == "Unicode":
                params["format_type"] = st.selectbox("Unicode Output Format", ["Escape Sequence", "Code Points", "Hex Bytes"])
                params["encoding"] = st.selectbox("Text Byte Encoding", ["utf-8", "utf-16", "utf-32"])
            elif encoder_format == "URL Encoding":
                params["encode_plus"] = st.checkbox("Replace spaces with + (Quote Plus)", value=False)
            elif encoder_format == "HTML Entity":
                params["quote"] = st.checkbox("Escape quotes", value=True)
            elif encoder_format == "Punycode":
                params["mode"] = st.selectbox("Punycode Output Mode", ["Punycode (Raw)", "IDNA (Domain)"])
            elif encoder_format == "Morse Code":
                params["char_delimiter"] = st.text_input("Character Delimiter", value=" ")
                params["word_delimiter"] = st.text_input("Word Delimiter", value=" / ")
            else:
                st.write("No configuration options required for this format.")
                
    with col2:
        st.write("### Encoded Output")
        
        output_placeholder = st.empty()
        
        # Run conversion when input text changes or conversion is clicked
        output_text = ""
        error_msg = ""
        
        if input_text:
            try:
                coder = CODERS[encoder_format]
                output_text = coder.encode(input_text, **params)
                error_msg = ""
            except Exception as e:
                error_msg = str(e)
                output_text = ""
        
        # Display output
        if error_msg:
            st.error(f"Encoding Error: {error_msg}")
        elif output_text:
            # Code box (pre-styled with copy button)
            st.code(output_text, language="text")
            show_char_counter(output_text)
            
            # Action Row
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                # Custom clipboard copy helper
                copy_to_clipboard_js(output_text, "encoder_out")
            with act_col2:
                st.download_button(
                    label="📥 Download Output",
                    data=output_text,
                    file_name=f"encoded_{encoder_format.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            # Log to session history
            if st.session_state.get("last_recorded_enc") != (input_text, encoder_format):
                record_history("Encode", input_text, output_text, encoder_format)
                st.session_state["last_recorded_enc"] = (input_text, encoder_format)
        else:
            st.info("Enter input text to view the encoded output.")
            
        if st.button("🧹 Clear Input", type="secondary"):
            st.session_state["enc_input_area"] = ""
            st.rerun()
