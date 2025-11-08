"""Reusable Streamlit UI helpers."""

from __future__ import annotations

from typing import List

import streamlit as st

from .model_registry import ALL_MODELS

DEFAULT_MODELS: List[str] = ["Claude Sonnet 4.5", "GPT-4o", "Gemini 2.5 Flash"]


def init_model_selection(session_key: str = "selected_models") -> None:
    """Ensure the model selection list exists in session state."""

    if session_key not in st.session_state:
        st.session_state[session_key] = DEFAULT_MODELS.copy()


def render_model_selection_sidebar(session_key: str = "selected_models") -> List[str]:
    """Render the sidebar controls for selecting models."""

    selected_models = st.session_state[session_key]

    st.header("Settings")
    st.subheader("Add Model")
    available_models = [m for m in ALL_MODELS.keys() if m not in selected_models]
    if available_models:
        new_model = st.selectbox(
            "Select a model",
            options=available_models,
            index=0,
            key=f"model_selector_{session_key}",
        )
        if st.button("Add", type="primary", key=f"add_model_{session_key}"):
            if new_model and new_model not in selected_models:
                selected_models.append(new_model)
                st.session_state[session_key] = selected_models
                st.rerun()
    else:
        st.caption("All available models have been added.")

    st.divider()
    st.subheader("Selected Models")

    for idx, model in enumerate(selected_models):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(f"{ALL_MODELS[model]['icon']} {model}")
        with col2:
            if st.button("✕", key=f"remove_{session_key}_{idx}"):
                selected_models.pop(idx)
                st.session_state[session_key] = selected_models
                st.rerun()

    return selected_models
