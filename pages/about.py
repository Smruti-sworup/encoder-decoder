"""
pages/about.py
Documentation and toolkit information.
"""

import streamlit as st
import config

def show() -> None:
    st.title("ℹ️ About & Documentation")
    st.caption(f"Universal Encoder & Decoder Toolkit v{config.VERSION}")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### 📖 Toolkit Overview")
        st.write(
            "This toolkit is designed for developers, security enthusiasts, and cryptographers. "
            "It groups multiple categories of text encoding, formatting, cryptographic functions, "
            "ciphers, compression, and analysis tools into a single modular visual application."
        )
        
        st.write("### ⚙️ Understanding the Concepts")
        
        tab1, tab2, tab3 = st.tabs(["🔄 Encoding", "🧮 Hashing", "🔑 Encryption"])
        
        with tab1:
            st.markdown(
                "**Encoding** is a two-way process that transforms data into a specific format using a publicly known "
                "algorithm so that it can be safely transmitted or stored. "
                "It does **NOT** provide security or confidentiality.\n\n"
                "**Examples:** Base64, URL Encoding, Binary conversion, Morse code."
            )
            
        with tab2:
            st.markdown(
                "**Hashing** is a one-way mathematical function that maps input data of any size to a fixed-size string of characters. "
                "It is mathematically infeasible to reverse a cryptographic hash. "
                "It is used for integrity verification and password verification.\n\n"
                "**Examples:** SHA-256, BLAKE3, MD5."
            )
            
        with tab3:
            st.markdown(
                "**Encryption** is a two-way transformation that secures data using a secret key. "
                "Only authorized parties with the correct key can decrypt the data. "
                "It guarantees confidentiality.\n\n"
                "* **Symmetric Encryption:** Uses the same key for encryption and decryption (e.g., AES, ChaCha20).\n"
                "* **Asymmetric Encryption:** Uses a public/private keypair (e.g., RSA)."
            )
            
    with col2:
        st.write("### 📌 Information")
        st.markdown(
            f"""
            * **Author:** {config.AUTHOR}
            * **Version:** {config.VERSION}
            * **OS Compatibility:** Windows, macOS, Linux
            * **License:** Production-Ready MIT
            """
        )
        st.info("Ensure to handle cryptographic keys securely. Do not store production keys in session history.")
