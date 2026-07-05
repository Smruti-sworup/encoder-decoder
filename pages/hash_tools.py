"""
pages/hash_tools.py
UI for hashing tools. Supports text hashing and large file hashing.
"""

import streamlit as st
import tempfile
import os
from modules.hashes import HashCoder
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js

def show() -> None:
    st.title("🧮 Hash Tools")
    st.caption("Generate checksums and hashes for text or uploaded files using modern cryptographic hash functions.")
    st.markdown("---")
    
    hasher = HashCoder()
    
    # Hash choice
    algorithm = st.selectbox("Select Hash Algorithm", hasher.SUPPORTED_ALGORITHMS, index=3) # Default SHA-256
    
    tab1, tab2 = st.tabs(["🔤 Hash Text", "📁 Hash File"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Input Text")
            input_text = st.text_area("Plain Text to Hash", height=200, key="hash_input_area")
            show_char_counter(input_text)
            
        with col2:
            st.write("### Hash Digest")
            if input_text:
                digest = hasher.hash_text(input_text, algorithm)
                
                # Check for error message
                if digest.startswith("Error") or digest.startswith("RIPEMD-160 not supported"):
                    st.error(digest)
                else:
                    st.code(digest, language="text")
                    st.markdown(f"**Length:** {len(digest)} hex characters ({len(digest)*4} bits)")
                    
                    # Copy
                    copy_to_clipboard_js(digest, "hash_out")
                    
                    # Record history
                    if st.session_state.get("last_recorded_hash_text") != (input_text, algorithm):
                        record_history("Hash Text", input_text, digest, algorithm)
                        st.session_state["last_recorded_hash_text"] = (input_text, algorithm)
            else:
                st.info("Enter text on the left to see the hash digest.")
                
            if st.button("🧹 Clear Input Text", key="clear_hash_text"):
                st.session_state["hash_input_area"] = ""
                st.rerun()
                
    with tab2:
        st.write("### Select File to Hash")
        uploaded_file = st.file_uploader("Upload File (Max 50MB)", key="hash_file_uploader")
        
        if uploaded_file:
            st.write("File Details:")
            st.write(f"- Name: `{uploaded_file.name}`")
            st.write(f"- Size: `{uploaded_file.size:,} bytes` ({uploaded_file.size / (1024*1024):.2f} MB)")
            
            if st.button("Calculate File Hash", type="primary"):
                with st.spinner("Processing file in chunks..."):
                    # Save to a temporary file
                    try:
                        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                            
                        # Perform hash
                        digest = hasher.hash_file(tmp_path, algorithm)
                        
                        # Clean up temp file
                        os.unlink(tmp_path)
                        
                        if digest.startswith("Error") or digest.startswith("RIPEMD-160 not supported"):
                            st.error(digest)
                        else:
                            st.success(f"File hashed successfully with {algorithm}!")
                            st.code(digest, language="text")
                            
                            # Action Row
                            act_col1, act_col2 = st.columns(2)
                            with act_col1:
                                copy_to_clipboard_js(digest, "hash_file_out")
                            with act_col2:
                                st.download_button(
                                    label="Download Hash Checksum",
                                    data=digest,
                                    file_name=f"{uploaded_file.name}_{algorithm.lower().replace('-', '_')}.txt",
                                    mime="text/plain"
                                )
                                
                            # Record history
                            record_history("Hash File", f"File: {uploaded_file.name}", digest, algorithm)
                    except Exception as e:
                        st.error(f"Error calculating file hash: {str(e)}")
        else:
            st.info("Upload a file above to begin hashing.")
