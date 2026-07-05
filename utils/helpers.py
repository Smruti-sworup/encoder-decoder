"""
utils/helpers.py
Contains user interface helper functions for Streamlit, such as layout macros,
metrics, character counters, and action panels.
"""

import streamlit as st
from typing import Any, Optional, Dict
import time

def init_theme() -> None:
    """Injects custom CSS styling from the assets folder into the Streamlit app."""
    try:
        css_path = "Universal-Encoder-Decoder/assets/style.css"
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except Exception:
        # Fallback to local assets path if run from subfolder
        try:
            with open("assets/style.css", "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception:
            pass

def show_char_counter(text: str) -> None:
    """Displays a character and word counter styled using style.css."""
    if text:
        char_count = len(text)
        word_count = len(text.split())
        st.markdown(
            f'<div class="char-counter">Length: {char_count} chars | Words: {word_count}</div>',
            unsafe_allow_html=True
        )

def render_glass_card(title: str, content: str, icon: str = "") -> None:
    """Renders a custom glassmorphism card for statistics or welcome message."""
    icon_str = f"<h3>{icon}</h3>" if icon else ""
    st.markdown(
        f"""
        <div class="glass-card">
            {icon_str}
            <h4 style="margin-top:0.2rem; margin-bottom: 0.5rem; color: #6366f1;">{title}</h4>
            <p style="font-size: 0.95rem; line-height: 1.5; opacity: 0.85; margin: 0;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def copy_to_clipboard_js(text: str, element_id: str) -> None:
    """
    Renders an HTML button with JS to copy text to clipboard.
    Useful for elements where standard st.code is not preferred.
    """
    escaped_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("\"", "\\\"").replace("\n", "\\n")
    button_html = f"""
    <button id="btn_{element_id}" class="st-emotion-cache-12fm72w" style="margin-top: 5px; padding: 4px 10px; font-size: 12px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2); background: transparent; cursor: pointer; color: #ffffff;" onclick="navigator.clipboard.writeText(`{escaped_text}`); this.innerText='Copied!'; setTimeout(()=>this.innerText='Copy', 2000);">Copy</button>
    """
    st.markdown(button_html, unsafe_allow_html=True)

def record_history(operation: str, input_data: str, output_data: str, format_type: str) -> None:
    """Appends an operation to the recent operations list stored in session state."""
    if "history" not in st.session_state:
        st.session_state["history"] = []
        
    st.session_state["history"].append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "operation": operation,
        "format": format_type,
        "input_len": len(input_data),
        "output_len": len(output_data),
        "input": input_data[:200] + ("..." if len(input_data) > 200 else ""),
        "output": output_data[:200] + ("..." if len(output_data) > 200 else ""),
        "full_input": input_data,
        "full_output": output_data
    })
    
    # Cap history at 50 items
    if len(st.session_state["history"]) > 50:
        st.session_state["history"].pop(0)
