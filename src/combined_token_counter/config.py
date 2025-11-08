"""Configuration helpers (API keys, etc.)."""

from __future__ import annotations

from typing import Dict

import streamlit as st

ApiKeys = Dict[str, str | None]


def load_api_keys() -> ApiKeys:
    """Load API keys from Streamlit secrets with graceful fallbacks."""

    api_keys: ApiKeys = {"anthropic": None, "google": None, "xai": None}

    try:
        api_keys["anthropic"] = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_keys["anthropic"] = None

    try:
        api_keys["google"] = st.secrets["GOOGLE_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_keys["google"] = None

    try:
        api_keys["xai"] = st.secrets["XAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_keys["xai"] = None

    return api_keys
