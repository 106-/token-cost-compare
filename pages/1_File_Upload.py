"""Streamlit page for counting tokens from uploaded text files."""

from pathlib import Path
import sys

import streamlit as st

st.set_page_config(
    page_title="Token Cost Compare - File Upload",
    page_icon="📄",
    layout="wide",
)

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if SRC_DIR.exists():
    src_path = str(SRC_DIR)
    if src_path not in sys.path:
        sys.path.append(src_path)

from token_cost_compare import (  # noqa: E402
    get_model_comparison_data,
    init_model_selection,
    load_api_keys,
    render_model_selection_sidebar,
)


def main() -> None:
    st.title("Token Cost Compare - File Upload")
    st.write("Upload a UTF-8 text file to compare token usage and costs across models.")

    init_model_selection()
    api_keys = load_api_keys()

    with st.sidebar:
        render_model_selection_sidebar()

    uploaded_file = st.file_uploader(
        "Upload a text file",
        type=["txt", "md", "json", "csv", "log"],
        accept_multiple_files=False,
    )

    if not uploaded_file:
        st.info("Upload a text file to calculate token counts.")
        return

    file_bytes = uploaded_file.read()
    if not file_bytes:
        st.warning("The file appears to be empty. Try another file.")
        return

    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        st.error("Please upload UTF-8 encoded text files only.")
        return

    st.subheader("Basic Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Filename")
        st.write(uploaded_file.name)
    with col2:
        st.metric("File Size (KB)", f"{len(file_bytes) / 1024:.2f}")
    with col3:
        st.metric("Character Count", len(text))

    if len(st.session_state.selected_models) > 0:
        st.subheader("Model Comparison")
        with st.spinner("Calculating token counts..."):
            df = get_model_comparison_data(
                text, st.session_state.selected_models, api_keys, include_per_char=True
            )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No models selected. Add at least one model from the sidebar.")

    st.subheader("Text Preview")
    st.text_area("Content", text, height=200, disabled=True)

    st.divider()
    st.caption("Only UTF-8 encoded text files are supported. Convert before uploading if needed.")


if __name__ == "__main__":
    main()
