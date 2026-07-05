"""
utils/clipboard.py
Provides helpers for clipboard interactions in Streamlit.
Since server-side Python cannot directly write to client clipboard,
we use Javascript-based triggers.
"""

import streamlit as st

def copy_text(text: str) -> None:
    """
    Triggers client-side copy by injecting a tiny JS script.
    Note: Must be run within a Streamlit block that can execute script injections.
    """
    escaped_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("\"", "\\\"").replace("\n", "\\n")
    js_code = f"""
    <script>
    navigator.clipboard.writeText(`{escaped_text}`).then(() => {{
        console.log('Copied to clipboard successfully.');
    }}).catch(err => {{
        console.error('Failed to copy text: ', err);
    }});
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)
