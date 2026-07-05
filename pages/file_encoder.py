"""
pages/file_encoder.py
UI page for converting full files to/from Base64, Hex, Binary representation, or Data URI.
"""

import streamlit as st
from modules.file_encoding import FileEncoder
from utils.helpers import record_history, copy_to_clipboard_js

def show() -> None:
    st.title("🛠️ File Encoder & Decoder")
    st.caption("Encode complete files (PDF, Images, Binaries) into text strings (Base64, Hex, Binary bits, or Data URIs) and restore them.")
    st.markdown("---")
    
    encoder = FileEncoder()
    
    tab_enc, tab_dec = st.tabs(["🔒 File to String (Encode)", "🔓 String to File (Decode)"])
    
    with tab_enc:
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            uploaded_file = st.file_uploader("Select File to Encode (Max 15MB)", key="file_enc_uploader")
            format_type = st.selectbox("Target File Format", ["Base64", "Hexadecimal", "Binary Bits", "Data URI (for Browser Embeds)"], key="file_enc_fmt")
            
        with col_e2:
            st.write("### Encoded File Results")
            if uploaded_file:
                file_bytes = uploaded_file.getvalue()
                st.write(f"- Name: `{uploaded_file.name}`")
                st.write(f"- Size: `{len(file_bytes):,} bytes`")
                
                try:
                    if format_type == "Base64":
                        output_str = encoder.encode_file_to_base64(file_bytes)
                    elif format_type == "Hexadecimal":
                        output_str = encoder.encode_file_to_hex(file_bytes)
                    elif format_type == "Binary Bits":
                        output_str = encoder.encode_file_to_binary(file_bytes)
                    else:  # Data URI
                        output_str = encoder.encode_to_data_uri(file_bytes, uploaded_file.name)
                        
                    # Show preview snippet
                    snippet_len = min(500, len(output_str))
                    st.text_area("Encoded Snippet (First 500 characters)", value=output_str[:snippet_len] + ("..." if len(output_str) > snippet_len else ""), height=120)
                    
                    # Action Buttons
                    copy_to_clipboard_js(output_str, "file_enc_out")
                    st.download_button(
                        label="📥 Download Encoded File String",
                        data=output_str,
                        file_name=f"{uploaded_file.name}_{format_type.lower().replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                    # Preview Renderings for Images/PDFs
                    if format_type == "Data URI":
                        if "image/" in output_str:
                            st.write("#### 🖼️ Image Preview")
                            st.markdown(f'<img src="{output_str}" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />', unsafe_allow_html=True)
                        elif "application/pdf" in output_str:
                            st.write("#### 📄 PDF Embed Preview")
                            st.markdown(f'<iframe src="{output_str}" width="100%" height="400px" style="border: none; border-radius: 8px;"></iframe>', unsafe_allow_html=True)
                            
                    # Record history
                    record_history(f"Encode File ({format_type})", f"File: {uploaded_file.name}", f"Length: {len(output_str)}", format_type)
                except Exception as e:
                    st.error(f"Encoding failed: {str(e)}")
            else:
                st.info("Upload a file to begin the encoding process.")
                
    with tab_dec:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            encoded_str = st.text_area("Paste Encoded String here", height=200, key="file_dec_input")
            format_type_dec = st.selectbox("Source Format", ["Base64", "Hexadecimal", "Binary Bits"], key="file_dec_fmt")
            target_filename = st.text_input("Restore Filename (with extension)", value="restored_file.bin")
            
        with col_d2:
            st.write("### Restored File Output")
            if encoded_str:
                try:
                    if format_type_dec == "Base64":
                        decoded_bytes = encoder.decode_base64_to_file(encoded_str)
                    elif format_type_dec == "Hexadecimal":
                        decoded_bytes = encoder.decode_hex_to_file(encoded_str)
                    else:  # Binary Bits
                        decoded_bytes = encoder.decode_binary_to_file(encoded_str)
                        
                    st.success(f"Successfully decoded! Recovered `{len(decoded_bytes):,}` bytes.")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Restored File",
                        data=decoded_bytes,
                        file_name=target_filename,
                        mime="application/octet-stream"
                    )
                    
                    # Record history
                    record_history(f"Decode File ({format_type_dec})", f"String Len: {len(encoded_str)}", f"Restored: {target_filename}", format_type_dec)
                except Exception as e:
                    st.error(f"Decoding failed. Ensure string corresponds to selected source format: {str(e)}")
            else:
                st.info("Paste the encoded string to verify and decode.")
