"""
pages/decoder.py
Unified UI page for string/data decoding operations.
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
    "URL Decoding": URLCoder(),
    "HTML Entity": HTMLCoder(),
    "Punycode": PunycodeCoder(),
    "Morse Code": MorseCoder(),
}

def show() -> None:
    st.title("🔄 Text Decoder")
    st.caption("Reconstruct plain text from encoded bases, hex strings, or format layouts.")
    st.markdown("---")
    
    # Selection of decoding
    decoder_format = st.selectbox("Select Source Encoded Format", list(CODERS.keys()))
    
    col1, col2 = st.columns(2)
    
    params = {}
    with col1:
        st.write("### Input")
        input_text = st.text_area("Encoded Text to Decode", height=200, key="dec_input_area")
        show_char_counter(input_text)
        
        # Format-specific advanced settings
        with st.expander("Advanced Configuration Options", expanded=True):
            if decoder_format == "ASCII":
                params["mode"] = st.selectbox("ASCII Mode", ["ordinals", "sanitize"])
            elif decoder_format == "Unicode":
                params["format_type"] = st.selectbox("Unicode Source Format", ["Escape Sequence", "Code Points", "Hex Bytes"])
                params["encoding"] = st.selectbox("Original Byte Encoding", ["utf-8", "utf-16", "utf-32"])
            elif decoder_format == "URL Decoding":
                params["decode_plus"] = st.checkbox("Interpret + as space", value=False)
            elif decoder_format == "Punycode":
                params["mode"] = st.selectbox("Punycode Source Mode", ["Punycode (Raw)", "IDNA (Domain)"])
            elif decoder_format == "Morse Code":
                params["char_delimiter"] = st.text_input("Character Delimiter", value=" ")
                params["word_delimiter"] = st.text_input("Word Delimiter", value="/")
            else:
                st.write("No configuration options required for this format.")
                
    with col2:
        st.write("### Decoded Output")
        
        output_text = ""
        error_msg = ""
        
        if input_text:
            try:
                coder = CODERS[decoder_format]
                output_text = coder.decode(input_text, **params)
                error_msg = ""
            except Exception as e:
                error_msg = str(e)
                output_text = ""
                
        # Display output
        if error_msg:
            st.error(f"Decoding Error: {error_msg}")
        elif output_text:
            st.code(output_text, language="text")
            show_char_counter(output_text)
            
            # Action Row
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                copy_to_clipboard_js(output_text, "decoder_out")
            with act_col2:
                st.download_button(
                    label="📥 Download Output",
                    data=output_text,
                    file_name=f"decoded_{decoder_format.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            # Log to session history
            if st.session_state.get("last_recorded_dec") != (input_text, decoder_format):
                record_history("Decode", input_text, output_text, decoder_format)
                st.session_state["last_recorded_dec"] = (input_text, decoder_format)
        else:
            st.info("Enter input text to view the decoded output.")
            
        if st.button("🧹 Clear Input", type="secondary"):
            st.session_state["dec_input_area"] = ""
            st.rerun()
