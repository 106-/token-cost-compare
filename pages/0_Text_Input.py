"""Streamlit page for manual text input token counting."""

from pathlib import Path
import sys

import streamlit as st

st.set_page_config(
    page_title="Token Cost Compare - Text Input",
    page_icon="📝",
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
    st.title("Token Cost Compare - Text Input")
    st.write(
        "Type or paste text directly to compare token usage and costs across models."
    )

    init_model_selection()
    api_keys = load_api_keys()

    with st.sidebar:
        render_model_selection_sidebar()

    text_input = st.text_area(
        "Enter text",
        height=200,
        placeholder="Type or paste your content here",
    )

    if not text_input:
        st.info("Enter text to calculate token counts.")
        return

    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Character Count", len(text_input))
    with col2:
        st.metric("Selected Models", len(st.session_state.selected_models))

    if len(st.session_state.selected_models) > 0:
        st.subheader("Model Comparison")
        with st.spinner("Calculating token counts..."):
            df = get_model_comparison_data(text_input, st.session_state.selected_models, api_keys)
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.caption("Token counts and prices are estimates; actual usage may vary.")
    st.caption("Prices reflect input tokens only and exclude provider-specific discounts.")


if __name__ == "__main__":
    main()
