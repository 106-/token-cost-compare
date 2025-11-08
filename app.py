"""Entry point that directs users to the dedicated pages."""

import streamlit as st

st.set_page_config(page_title="Token Cost Compare", page_icon="🧮", layout="wide")

st.title("Token Cost Compare")
st.write("Choose a workflow from the Pages navigation on the left.")

st.info(
    """Available workflows:
- 📝 Text Input: Type or paste text directly to count tokens
- 📄 File Upload: Upload a UTF-8 text file and count its tokens
"""
)

st.page_link("pages/0_Text_Input.py", label="📝 Open the Text Input page", icon="📝")
st.page_link("pages/1_File_Upload.py", label="📄 Open the File Upload page", icon="📄")
