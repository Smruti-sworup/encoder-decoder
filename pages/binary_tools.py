"""
pages/binary_tools.py
UI page for binary conversions (ASCII, Binary, Decimal, Hex).
"""

import streamlit as st
from modules.binary import BinaryCoder
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js

def show() -> None:
    st.title("⚙️ Binary Tools")
    st.caption("Perform bitwise conversion operations: ASCII to Binary, Binary to Decimal, and Hex to Binary.")
    st.markdown("---")
    
    coder = BinaryCoder()
    
    # Operation selection
    op_type = st.selectbox("Select Conversion Operation", [
        "ASCII Text ↔ Binary Bytes",
        "Binary Bytes ↔ Decimal Values",
        "Hexadecimal ↔ Binary Bytes"
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Input")
        if op_type == "ASCII Text ↔ Binary Bytes":
            direction = st.radio("Direction", ["Text to Binary", "Binary to Text"])
            placeholder = "Type ASCII text..." if direction == "Text to Binary" else "01001000 01100101 01101100 01101100 01101111"
        elif op_type == "Binary Bytes ↔ Decimal Values":
            direction = st.radio("Direction", ["Binary to Decimal", "Decimal to Binary"])
            placeholder = "01001000 01100101" if direction == "Binary to Decimal" else "72 101"
        else:  # Hexadecimal ↔ Binary Bytes
            direction = st.radio("Direction", ["Hex to Binary", "Binary to Hex"])
            placeholder = "48656c6c6f" if direction == "Hex to Binary" else "01001000 01100101"
            
        input_data = st.text_area("Source Value", height=180, key="bin_input_area", placeholder=placeholder)
        show_char_counter(input_data)
        
    with col2:
        st.write("### Converted Output")
        
        output_data = ""
        error_msg = ""
        
        if input_data:
            try:
                if op_type == "ASCII Text ↔ Binary Bytes":
                    if direction == "Text to Binary":
                        output_data = coder.encode(input_data)
                    else:
                        output_data = coder.decode(input_data)
                elif op_type == "Binary Bytes ↔ Decimal Values":
                    if direction == "Binary to Decimal":
                        output_data = coder.binary_to_decimal(input_data)
                    else:
                        output_data = coder.decimal_to_binary(input_data)
                else:  # Hex ↔ Binary
                    if direction == "Hex to Binary":
                        output_data = coder.hex_to_binary(input_data)
                    else:
                        output_data = coder.binary_to_hex(input_data)
            except Exception as e:
                error_msg = str(e)
                
        # Display output
        if error_msg:
            st.error(f"Conversion Error: {error_msg}")
        elif output_data:
            st.code(output_data, language="text")
            show_char_counter(output_data)
            
            # Action Row
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                copy_to_clipboard_js(output_data, "binary_tools_out")
            with act_col2:
                st.download_button(
                    label="📥 Download Output",
                    data=output_data,
                    file_name="binary_tools_output.txt",
                    mime="text/plain"
                )
                
            # History
            hist_op = f"Binary ({op_type} - {direction})"
            if st.session_state.get("last_recorded_bin_tool") != (input_data, direction):
                record_history(hist_op, input_data, output_data, "Binary")
                st.session_state["last_recorded_bin_tool"] = (input_data, direction)
        else:
            st.info("Input target values on the left to display conversion results.")
            
        if st.button("🧹 Clear Input", key="clear_bin_tool"):
            st.session_state["bin_input_area"] = ""
            st.rerun()
