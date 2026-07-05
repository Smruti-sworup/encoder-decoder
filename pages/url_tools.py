"""
pages/url_tools.py
UI page for URL encoding, decoding, and parsing.
"""

import streamlit as st
import urllib.parse
import pandas as pd
from modules.url import URLCoder
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js

def show() -> None:
    st.title("🌐 URL Tools")
    st.caption("Percent-encode, decode, or extract component fields from web uniform resource identifiers (URIs).")
    st.markdown("---")
    
    coder = URLCoder()
    
    tab_codec, tab_parser = st.tabs(["🔄 Encode / Decode", "🔍 URL Parser"])
    
    with tab_codec:
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Input")
            direction = st.radio("Direction", ["Encode URL", "Decode URL"], key="url_codec_dir")
            input_url = st.text_area("Source URL/String", height=180, key="url_codec_input", placeholder="https://example.com/search?q=hello world")
            show_char_counter(input_url)
            
            with st.expander("Settings", expanded=True):
                encode_plus = st.checkbox("Encode spaces as '+'", value=False, key="url_codec_plus")
                
        with col2:
            st.write("### Output")
            output_url = ""
            error_msg = ""
            
            if input_url:
                try:
                    if direction == "Encode URL":
                        output_url = coder.encode(input_url, encode_plus=encode_plus)
                    else:
                        output_url = coder.decode(input_url, decode_plus=encode_plus)
                except Exception as e:
                    error_msg = str(e)
                    
            if error_msg:
                st.error(error_msg)
            elif output_url:
                st.code(output_url, language="text")
                show_char_counter(output_url)
                
                # Copy & Download
                copy_to_clipboard_js(output_url, "url_codec_out")
                st.download_button("📥 Download URL", output_url, file_name="url_codec_output.txt", mime="text/plain")
                
                # History log
                if st.session_state.get("last_recorded_url_codec") != (input_url, direction):
                    record_history(direction, input_url, output_url, "URL")
                    st.session_state["last_recorded_url_codec"] = (input_url, direction)
            else:
                st.info("Input URL text to show transformed outcome.")
                
            if st.button("🧹 Clear Input", key="clear_url_codec"):
                st.session_state["url_codec_input"] = ""
                st.rerun()
                
    with tab_parser:
        st.write("### Parse Web Address")
        parse_input = st.text_input("Enter URL to Parse", value="https://user:pass@example.com:8080/path/to/resource?query1=hello&query2=world#section-1")
        
        if parse_input:
            try:
                parsed = urllib.parse.urlparse(parse_input)
                
                # Render metadata grid
                col_s, col_h, col_p = st.columns(3)
                with col_s:
                    st.metric("Scheme / Protocol", parsed.scheme or "None")
                with col_h:
                    st.metric("Host/Netloc", parsed.netloc or "None")
                with col_p:
                    st.metric("Path", parsed.path or "None")
                    
                # Full details table
                st.write("#### Components")
                components_data = {
                    "Component": ["Scheme", "Netloc (Host:Port)", "Path", "Params", "Query String", "Fragment (Hash)", "Username", "Password", "Hostname", "Port"],
                    "Value": [
                        parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment,
                        parsed.username or "N/A", parsed.password or "N/A", parsed.hostname or "N/A", parsed.port or "N/A"
                    ]
                }
                st.table(pd.DataFrame(components_data))
                
                # Query Parameters parser
                if parsed.query:
                    st.write("#### Query Parameters")
                    queries = urllib.parse.parse_qs(parsed.query)
                    # Convert to flat key-value strings
                    flat_queries = {k: ", ".join(v) for k, v in queries.items()}
                    df_queries = pd.DataFrame(list(flat_queries.items()), columns=["Parameter Key", "Value"])
                    st.dataframe(df_queries, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to parse URL: {str(e)}")
