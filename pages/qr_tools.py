"""
pages/qr_tools.py
UI page for generating and decoding QR codes.
"""

import streamlit as st
from modules.qr import QRTool
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js

def show() -> None:
    st.title("📱 QR Tools")
    st.caption("Generate barcodes/QR codes from text, or decode raw QR codes from uploaded images.")
    st.markdown("---")
    
    qr_tool = QRTool()
    
    tab_gen, tab_dec = st.tabs(["➕ Generate QR Code", "🔍 Decode QR Code Image"])
    
    with tab_gen:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("### Input Text")
            input_text = st.text_area("Text to encode into QR", height=150, key="qr_gen_input", placeholder="Type url or text...")
            show_char_counter(input_text)
            
            with st.expander("Design Settings", expanded=True):
                box_size = st.slider("Box Size (Resolution)", min_value=5, max_value=25, value=10)
                border = st.slider("Border Padding", min_value=1, max_value=10, value=4)
                fill_color = st.selectbox("Fill Color", ["black", "navy", "darkgreen", "darkred", "indigo"])
                back_color = st.selectbox("Background Color", ["white", "lightgray", "yellow"])
                
        with col_g2:
            st.write("### Generated QR Code")
            if input_text:
                try:
                    qr_bytes = qr_tool.generate_qr(
                        input_text,
                        box_size=box_size,
                        border=border,
                        fill_color=fill_color,
                        back_color=back_color
                    )
                    
                    st.image(qr_bytes, width=280)
                    
                    # Download
                    st.download_button(
                        label="📥 Download QR Code (PNG)",
                        data=qr_bytes,
                        file_name="qr_code.png",
                        mime="image/png"
                    )
                    
                    # Record history
                    if st.session_state.get("last_recorded_qr_gen") != input_text:
                        record_history("Generate QR", input_text[:100], "Generated PNG image", "QR Code")
                        st.session_state["last_recorded_qr_gen"] = input_text
                except Exception as e:
                    st.error(f"Failed to generate QR: {str(e)}")
            else:
                st.info("Input text on the left to compile a QR code.")
                
            if st.button("🧹 Clear Input", key="clear_qr_gen"):
                st.session_state["qr_gen_input"] = ""
                st.rerun()
                
    with tab_dec:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            uploaded_file = st.file_uploader("Upload QR Code Image (PNG, JPG)", key="qr_dec_uploader")
            
        with col_d2:
            st.write("### Decoded Content")
            if uploaded_file:
                image_bytes = uploaded_file.getvalue()
                st.image(image_bytes, width=200, caption="Uploaded QR Image")
                
                if st.button("Decode QR Code Image", type="primary"):
                    success, result = qr_tool.decode_qr(image_bytes)
                    if success:
                        st.success("Successfully decoded!")
                        st.code(result, language="text")
                        
                        # Copy
                        copy_to_clipboard_js(result, "qr_dec_out")
                        
                        # Record history
                        record_history("Decode QR File", f"File: {uploaded_file.name}", result[:100], "QR Code")
                    else:
                        st.error(result)
            else:
                st.info("Upload a QR code image to decode it.")
