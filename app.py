"""
app.py
Main entry point for the Universal Encoder & Decoder Toolkit.
Handles application layout, sidebar search filtering, and page routing.
"""

import streamlit as st
import importlib
import config
from utils.helpers import init_theme

# Execute Page configuration as the absolute first Streamlit command
st.set_page_config(**config.PAGE_CONFIG)

def main() -> None:
    # Inject CSS
    init_theme()
    
    # Sidebar Header
    st.sidebar.image(config.LOGO_PATH, width=70)
    st.sidebar.title(config.APP_NAME)
    st.sidebar.caption(f"Toolkit Version: {config.VERSION}")
    st.sidebar.markdown("---")
    
    # Sidebar Search Box for filtering formats/tools
    search_query = st.sidebar.text_input("🔍 Search formats or tools", value="", placeholder="e.g. AES, Base64, QR...")
    
    # Build list of tools matching search
    available_tools = {}
    
    # Populate tools from config
    for category, cat_data in config.TOOL_CATEGORIES.items():
        for tool_name, module_path in cat_data["tools"].items():
            # Match search query (case-insensitive)
            if not search_query or search_query.lower() in tool_name.lower() or search_query.lower() in category.lower():
                available_tools[tool_name] = module_path
                
    st.sidebar.write("### 🛠️ Navigation")
    
    # Pre-selection logic (e.g. from Auto-Detect redirect)
    default_index = 0
    preselect_name = st.session_state.get("nav_selection", "Home")
    
    # If search filters the list, find matching index
    tool_names = list(available_tools.keys())
    
    if not tool_names:
        st.sidebar.warning("No tools match your search criteria.")
        selected_page = None
    else:
        if preselect_name in tool_names:
            default_index = tool_names.index(preselect_name)
        else:
            default_index = 0
            
        selected_page = st.sidebar.radio(
            "Select a page",
            options=tool_names,
            index=default_index,
            label_visibility="collapsed"
        )
        
        # Clear navigation redirect state once processed
        if "nav_selection" in st.session_state:
            del st.session_state["nav_selection"]
            
    st.sidebar.markdown("---")
    st.sidebar.info(
        f"Pair Programmed by Antigravity.\n"
        f"Production-Ready & Highly Extensible."
    )
    
    # Render the selected page
    if selected_page:
        module_path = available_tools[selected_page]
        try:
            # Dynamic import and execution
            module = importlib.import_module(module_path)
            
            # Pass pre-selected format from search/redirects if applicable
            if selected_page == "String Decoder" and "decoder_format_preselect" in st.session_state:
                pre_fmt = st.session_state.pop("decoder_format_preselect")
                st.sidebar.info(f"Auto-selected source format: **{pre_fmt}**")
                
            module.show()
        except Exception as e:
            st.error(f"Error loading page '{selected_page}': {str(e)}")
            st.exception(e)
    else:
        st.info("Please select a tool from the navigation sidebar.")

if __name__ == "__main__":
    main()
