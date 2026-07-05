"""
pages/crypto_tools.py
UI page for symmetric (AES, DES, 3DES, ChaCha20) and asymmetric (RSA) cryptosystems.
"""

import streamlit as st
from modules.aes import AESCoder
from modules.des import DESCoder
from modules.triple_des import TripleDESCoder
from modules.chacha20 import ChaCha20Coder
from modules.rsa import RSACoder
from utils.helpers import show_char_counter, record_history, copy_to_clipboard_js
from utils.validators import validate_aes_key, is_hex

# Instances
AES_CODER = AESCoder()
DES_CODER = DESCoder()
DES3_CODER = TripleDESCoder()
CHACHA_CODER = ChaCha20Coder()
RSA_CODER = RSACoder()

def show() -> None:
    st.title("🔑 Cryptography Tools")
    st.caption("Perform modern symmetric encryption (AES, DES, 3DES, ChaCha20) or asymmetric encryption (RSA).")
    st.markdown("---")
    
    tab_symmetric, tab_asymmetric = st.tabs(["🔒 Symmetric Cryptosystems", "🔑 Asymmetric (RSA)"])
    
    with tab_symmetric:
        st.write("### Symmetric Encryption & Decryption")
        
        algo = st.selectbox("Select Symmetric Algorithm", ["AES", "DES", "Triple DES (3DES)", "ChaCha20"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            direction = st.radio("Operation", ["Encrypt", "Decrypt"], key="sym_dir")
            input_text = st.text_area("Input Text (Plaintext or Base64 Ciphertext)", height=150, key="sym_input")
            show_char_counter(input_text)
            
            # Key options
            with st.expander("Key & Parameter Configuration", expanded=True):
                key = st.text_input("Key (Text or Hex)", type="password", key="sym_key", help="Provide appropriate key size based on the algorithm.")
                
                # Dynamic options
                if algo == "AES":
                    mode = st.selectbox("AES Mode", ["CBC", "CTR", "ECB"], key="aes_mode")
                    iv = st.text_input("Initialization Vector (IV) - 16 bytes", key="aes_iv", placeholder="Optional (auto-generated on encryption)")
                elif algo == "DES":
                    mode = st.selectbox("DES Mode", ["CBC", "ECB"], key="des_mode")
                    iv = st.text_input("Initialization Vector (IV) - 8 bytes", key="des_iv", placeholder="Optional (auto-generated on encryption)")
                elif algo == "Triple DES (3DES)":
                    mode = st.selectbox("3DES Mode", ["CBC", "ECB"], key="des3_mode")
                    iv = st.text_input("Initialization Vector (IV) - 8 bytes", key="des3_iv", placeholder="Optional (auto-generated on encryption)")
                elif algo == "ChaCha20":
                    mode = "N/A"
                    iv = st.text_input("Nonce (8 or 12 bytes)", key="chacha_nonce", placeholder="Optional (auto-generated on encryption)")
                    
        with col2:
            st.write("### Output")
            output_text = ""
            error_msg = ""
            
            if input_text:
                if not key:
                    st.warning("Please provide an encryption key.")
                else:
                    try:
                        if algo == "AES":
                            if direction == "Encrypt":
                                output_text = AES_CODER.encode(input_text, key=key, iv=iv, mode=mode)
                            else:
                                output_text = AES_CODER.decode(input_text, key=key, iv=iv, mode=mode)
                        elif algo == "DES":
                            if direction == "Encrypt":
                                output_text = DES_CODER.encode(input_text, key=key, iv=iv, mode=mode)
                            else:
                                output_text = DES_CODER.decode(input_text, key=key, iv=iv, mode=mode)
                        elif algo == "Triple DES (3DES)":
                            if direction == "Encrypt":
                                output_text = DES3_CODER.encode(input_text, key=key, iv=iv, mode=mode)
                            else:
                                output_text = DES3_CODER.decode(input_text, key=key, iv=iv, mode=mode)
                        elif algo == "ChaCha20":
                            if direction == "Encrypt":
                                output_text = CHACHA_CODER.encode(input_text, key=key, nonce=iv)
                            else:
                                output_text = CHACHA_CODER.decode(input_text, key=key, nonce=iv)
                    except Exception as e:
                        error_msg = str(e)
                        
            if error_msg:
                st.error(f"Cryptographic Error: {error_msg}")
            elif output_text:
                st.code(output_text, language="text")
                show_char_counter(output_text)
                
                # Copy & Download
                copy_to_clipboard_js(output_text, "sym_out")
                st.download_button("📥 Download Output", output_text, file_name=f"crypto_{algo.lower().replace(' ', '_')}_{direction.lower()}.txt", mime="text/plain")
                
                # History log
                if st.session_state.get("last_recorded_sym") != (input_text, algo, direction):
                    record_history(f"{algo} {direction}", input_text[:100], output_text[:100], algo)
                    st.session_state["last_recorded_sym"] = (input_text, algo, direction)
            else:
                st.info("Input data, configure key, and proceed.")
                
            if st.button("🧹 Clear Input", key="clear_sym"):
                st.session_state["sym_input"] = ""
                st.rerun()
                
    with tab_asymmetric:
        st.write("### RSA Encryption & Keypair Generator")
        
        rsa_tab_gen, rsa_tab_enc, rsa_tab_dec = st.tabs(["🔑 Generate Keys", "🔒 RSA Encrypt", "🔓 RSA Decrypt"])
        
        with rsa_tab_gen:
            bits = st.selectbox("Key Size (bits)", [1024, 2048, 3072, 4096], index=1)
            if st.button("Generate RSA Keypair", type="primary"):
                with st.spinner("Generating keypair (this might take a few seconds)..."):
                    try:
                        priv_pem, pub_pem = RSA_CODER.generate_keypair(bits=bits)
                        st.success("Successfully generated keypair!")
                        
                        col_priv, col_pub = st.columns(2)
                        with col_priv:
                            st.write("#### Private Key (Keep Secret!)")
                            st.code(priv_pem, language="text")
                            copy_to_clipboard_js(priv_pem, "rsa_priv_pem")
                            st.download_button("📥 Download Private Key", priv_pem, file_name="private_key.pem", mime="application/x-pem-file")
                        with col_pub:
                            st.write("#### Public Key")
                            st.code(pub_pem, language="text")
                            copy_to_clipboard_js(pub_pem, "rsa_pub_pem")
                            st.download_button("📥 Download Public Key", pub_pem, file_name="public_key.pem", mime="application/x-pem-file")
                    except Exception as e:
                        st.error(f"Generation failed: {str(e)}")
                        
        with rsa_tab_enc:
            col_enc1, col_enc2 = st.columns(2)
            with col_enc1:
                rsa_enc_input = st.text_area("Plaintext to Encrypt", height=150, key="rsa_enc_input")
                pub_key_pem = st.text_area("Recipient Public Key PEM", height=150, key="rsa_pub_key_input", placeholder="-----BEGIN PUBLIC KEY-----")
            with col_enc2:
                st.write("### Ciphertext Output")
                rsa_ciphertext = ""
                if rsa_enc_input and pub_key_pem:
                    try:
                        rsa_ciphertext = RSA_CODER.encode(rsa_enc_input, public_key_pem=pub_key_pem)
                        st.code(rsa_ciphertext, language="text")
                        copy_to_clipboard_js(rsa_ciphertext, "rsa_enc_out")
                        st.download_button("📥 Download Ciphertext", rsa_ciphertext, file_name="rsa_ciphertext.txt", mime="text/plain")
                        
                        # History
                        record_history("RSA Encrypt", rsa_enc_input[:100], rsa_ciphertext[:100], "RSA")
                    except Exception as e:
                        st.error(f"RSA Encryption Error: {str(e)}")
                else:
                    st.info("Provide plaintext and recipient public key to encrypt.")
                    
        with rsa_tab_dec:
            col_dec1, col_dec2 = st.columns(2)
            with col_dec1:
                rsa_dec_input = st.text_area("Base64 Ciphertext to Decrypt", height=150, key="rsa_dec_input")
                priv_key_pem = st.text_area("Recipient Private Key PEM", height=150, key="rsa_priv_key_input", placeholder="-----BEGIN PRIVATE KEY-----")
            with col_dec2:
                st.write("### Recovered Plaintext")
                rsa_recovered = ""
                if rsa_dec_input and priv_key_pem:
                    try:
                        rsa_recovered = RSA_CODER.decode(rsa_dec_input, private_key_pem=priv_key_pem)
                        st.code(rsa_recovered, language="text")
                        copy_to_clipboard_js(rsa_recovered, "rsa_dec_out")
                        st.download_button("📥 Download Decrypted Text", rsa_recovered, file_name="rsa_decrypted.txt", mime="text/plain")
                        
                        # History
                        record_history("RSA Decrypt", rsa_dec_input[:100], rsa_recovered[:100], "RSA")
                    except Exception as e:
                        st.error(f"RSA Decryption Error: {str(e)}")
                else:
                    st.info("Provide ciphertext and corresponding private key to decrypt.")
