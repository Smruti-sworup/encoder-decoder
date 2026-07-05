"""
pages/password_generator.py
UI page for password generator and entropy/strength analyzer.
"""

import streamlit as st
from modules.password import PasswordGenerator
from utils.helpers import copy_to_clipboard_js

def show() -> None:
    st.title("🛠️ Password Generator")
    st.caption("Generate cryptographically secure random passwords and inspect their strength using the Shannon Entropy meter.")
    st.markdown("---")
    
    generator = PasswordGenerator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Configuration Options")
        
        length = st.slider("Password Length", min_value=6, max_value=128, value=16)
        
        use_lower = st.checkbox("Include Lowercase Characters (a-z)", value=True)
        use_upper = st.checkbox("Include Uppercase Characters (A-Z)", value=True)
        use_digits = st.checkbox("Include Numeric Digits (0-9)", value=True)
        use_special = st.checkbox("Include Special Symbols (e.g. !@#$)", value=True)
        
        custom_symbols = st.text_input("Custom Special Symbols (Optional)", value="", placeholder="Leave empty for default symbols list")
        
        # Generation Action
        generate_btn = st.button("Generate Password", type="primary")
        
    with col2:
        st.write("### Secure Output")
        
        # Keep password in session state to maintain across reruns
        if "generated_password" not in st.session_state or generate_btn:
            try:
                st.session_state["generated_password"] = generator.generate(
                    length=length,
                    use_lower=use_lower,
                    use_upper=use_upper,
                    use_digits=use_digits,
                    use_special=use_special,
                    custom_special=custom_symbols
                )
            except Exception as e:
                st.error(str(e))
                st.session_state["generated_password"] = ""
                
        password = st.session_state["generated_password"]
        
        if password:
            st.code(password, language="text")
            
            # Action Row
            copy_to_clipboard_js(password, "pass_gen")
            
            st.markdown("---")
            
            # Strength meter / Entropy Analysis
            entropy, label, color = generator.calculate_entropy(password)
            
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 15px; margin-top: 10px;">
                    <h4 style="margin: 0; padding-bottom: 8px;">Shannon Entropy Analysis</h4>
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 1.1rem; font-weight: 600; color: {color}; margin-right: 15px;">{label}</span>
                        <span style="font-family: monospace; font-size: 0.95rem; opacity: 0.85;">{entropy:.1f} bits</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); height: 10px; border-radius: 5px; width: 100%; overflow: hidden;">
                        <div style="background: {color}; height: 100%; width: {min(100.0, (entropy / 128.0) * 100.0):.1f}%;"></div>
                    </div>
                    <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 8px; margin-bottom: 0; line-height: 1.4;">
                        Entropy scores reflect guessing difficulty: &lt; 36 bits is easily crackable, 60+ bits provides strong protection for normal accounts, and 128+ bits provides military-grade cryptographic resistance.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Select parameters and click 'Generate Password' to create a password.")
