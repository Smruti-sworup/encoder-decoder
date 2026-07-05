"""
pages/compare.py
Provides side-by-side output comparer.
"""

import streamlit as st
import difflib

def show() -> None:
    st.title("⚖️ Compare Outputs")
    st.caption("Compare two text blocks to inspect differences, length deviations, and diff structures.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        text1 = st.text_area("Text Block A", height=200, placeholder="Paste first text here...")
        st.markdown(f"**Length:** {len(text1)} characters | **Words:** {len(text1.split())}")
        
    with col2:
        text2 = st.text_area("Text Block B", height=200, placeholder="Paste second text here...")
        st.markdown(f"**Length:** {len(text2)} characters | **Words:** {len(text2.split())}")
        
    st.markdown("---")
    
    st.write("### 📊 Metrics")
    diff_chars = len(text2) - len(text1)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Length Difference", f"{diff_chars:+} chars" if diff_chars != 0 else "Identical Length")
    with m_col2:
        match_status = "Exact Match" if text1 == text2 else "Mismatch"
        st.metric("Content Match", match_status)
    with m_col3:
        percentage = 0.0
        if max(len(text1), len(text2)) > 0:
            matcher = difflib.SequenceMatcher(None, text1, text2)
            percentage = matcher.ratio() * 100
        st.metric("Similarity Ratio", f"{percentage:.2f}%")
        
    if text1 != text2:
        st.write("### 🔍 Line-by-Line Differences (Unified Diff)")
        # Split text lines
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        diff = difflib.unified_diff(lines1, lines2, fromfile='Block A', tofile='Block B', lineterm='')
        diff_list = list(diff)
        
        if diff_list:
            formatted_diff = "\n".join(diff_list)
            st.code(formatted_diff, language="diff")
        else:
            st.info("Line differences are too complex or represent only whitespaces.")
