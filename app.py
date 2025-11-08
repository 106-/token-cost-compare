import pandas as pd
import streamlit as st
import tiktoken
from anthropic import Anthropic
from google import genai

# All available models (combined)
ALL_MODELS = {
    # Claude models
    "Claude Sonnet 4.5": {"id": "claude-sonnet-4-5-20250929", "provider": "claude", "icon": "🤖"},
    "Claude Haiku 4.5": {"id": "claude-haiku-4-5-20251001", "provider": "claude", "icon": "🤖"},
    "Claude Opus 4.1": {"id": "claude-opus-4-1-20250805", "provider": "claude", "icon": "🤖"},
    "Claude 3.7 Sonnet": {"id": "claude-3-7-sonnet-20250219", "provider": "claude", "icon": "🤖"},
    "Claude 3.5 Haiku": {"id": "claude-3-5-haiku-20241022", "provider": "claude", "icon": "🤖"},
    "Claude 3 Haiku": {"id": "claude-3-haiku-20240307", "provider": "claude", "icon": "🤖"},
    # OpenAI models
    "GPT-5": {"id": "gpt-5", "provider": "openai", "icon": "🔷"},
    "GPT-4o": {"id": "gpt-4o", "provider": "openai", "icon": "🔷"},
    "GPT-4o mini": {"id": "gpt-4o-mini", "provider": "openai", "icon": "🔷"},
    "GPT-4 Turbo": {"id": "gpt-4-turbo", "provider": "openai", "icon": "🔷"},
    "GPT-3.5 Turbo": {"id": "gpt-3.5-turbo", "provider": "openai", "icon": "🔷"},
    # Gemini models
    "Gemini 2.5 Flash": {"id": "gemini-2.5-flash", "provider": "gemini", "icon": "💎"},
    "Gemini 2.5 Flash-Lite": {"id": "gemini-2.5-flash-lite", "provider": "gemini", "icon": "💎"},
    "Gemini 2.0 Flash": {"id": "gemini-2.0-flash", "provider": "gemini", "icon": "💎"},
    "Gemini 2.5 Pro": {"id": "gemini-2.5-pro", "provider": "gemini", "icon": "💎"},
}

# Model pricing (USD per million tokens)
MODEL_PRICING = {
    # Claude
    "claude-sonnet-4-5-20250929": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "claude-opus-4-1-20250805": {"input": 15.00, "output": 75.00},
    "claude-3-7-sonnet-20250219": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    # OpenAI
    "gpt-5": {"input": 1.25, "output": 10.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    # Gemini
    "gemini-2.5-flash": {"input": 0.30, "output": 2.50},
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
}


def calculate_cost(tokens: int, pricing_dict: dict, token_type: str = "input") -> float:
    """Calculate cost from token count."""
    if not pricing_dict:
        return 0.0
    price_per_million = pricing_dict.get(token_type, 0.0)
    return (tokens / 1_000_000) * price_per_million


def count_tokens_with_tiktoken(text: str, model: str) -> int:
    """Count tokens using tiktoken."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))


def count_tokens_with_gemini(text: str, model: str, api_key: str) -> dict:
    """Count tokens using Gemini API."""
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.count_tokens(model=model, contents=text)
        return {"success": True, "input_tokens": response.total_tokens}
    except Exception as e:
        return {"success": False, "error": str(e)}


def count_tokens_with_claude(text: str, model: str, api_key: str) -> dict:
    """Count tokens using Claude API."""
    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.count_tokens(
            model=model, messages=[{"role": "user", "content": text}]
        )
        return {"success": True, "input_tokens": response.input_tokens}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_token_count(text: str, model_name: str, api_keys: dict) -> dict:
    """Get token count for a specific model."""
    model_info = ALL_MODELS[model_name]
    model_id = model_info["id"]
    provider = model_info["provider"]

    if provider == "openai":
        tokens = count_tokens_with_tiktoken(text, model_id)
        return {"success": True, "input_tokens": tokens}
    elif provider == "claude":
        if not api_keys.get("anthropic"):
            return {"success": False, "error": "Claude API key not configured"}
        return count_tokens_with_claude(text, model_id, api_keys["anthropic"])
    elif provider == "gemini":
        if not api_keys.get("google"):
            return {"success": False, "error": "Gemini API key not configured"}
        return count_tokens_with_gemini(text, model_id, api_keys["google"])


def get_model_comparison_data(text: str, selected_models: list, api_keys: dict) -> pd.DataFrame:
    """Get comparison data for all selected models as a DataFrame."""
    data = []

    for model_name in selected_models:
        model_info = ALL_MODELS[model_name]
        icon = model_info["icon"]
        model_id = model_info["id"]
        pricing = MODEL_PRICING.get(model_id, {})

        result = get_token_count(text, model_name, api_keys)

        if result["success"]:
            tokens = result["input_tokens"]
            cost = calculate_cost(tokens, pricing, "input")

            data.append(
                {
                    "Model": f"{icon} {model_name}",
                    "Provider": model_info["provider"].title(),
                    "Tokens": tokens,
                    "Input Cost": f"${cost:.6f}",
                    "Input Price": f"${pricing.get('input', 0):.2f} / 1M",
                    "Output Price": f"${pricing.get('output', 0):.2f} / 1M",
                }
            )
        else:
            data.append(
                {
                    "Model": f"{icon} {model_name}",
                    "Provider": model_info["provider"].title(),
                    "Tokens": "Error",
                    "Input Cost": result["error"],
                    "Input Price": "-",
                    "Output Price": "-",
                }
            )

    return pd.DataFrame(data)


def main():
    st.title("Token Counter")
    st.write("Compare token counts and costs across Claude, OpenAI, and Gemini")

    # Initialize session state for selected models
    if "selected_models" not in st.session_state:
        st.session_state.selected_models = [
            "Claude Sonnet 4.5",
            "GPT-4o",
            "Gemini 2.5 Flash",
        ]

    # Get API keys from Streamlit secrets
    api_keys = {}
    try:
        api_keys["anthropic"] = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_keys["anthropic"] = None

    try:
        api_keys["google"] = st.secrets["GOOGLE_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_keys["google"] = None

    # Sidebar for model selection
    with st.sidebar:
        st.header("Settings")

        st.subheader("Add Model")
        new_model = st.selectbox(
            "Select a model",
            options=[m for m in ALL_MODELS.keys() if m not in st.session_state.selected_models],
            key="model_selector",
        )
        if st.button("Add", type="primary"):
            if new_model and new_model not in st.session_state.selected_models:
                st.session_state.selected_models.append(new_model)
                st.rerun()

        st.divider()
        st.subheader("Selected Models")

        # Show selected models with remove buttons
        for idx, model in enumerate(st.session_state.selected_models):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(f"{ALL_MODELS[model]['icon']} {model}")
            with col2:
                if st.button("✕", key=f"remove_{idx}"):
                    st.session_state.selected_models.pop(idx)
                    st.rerun()

    # Text input area
    text_input = st.text_area(
        "Enter your text", height=200, placeholder="Type or paste your text here..."
    )

    # Calculate and display token counts
    if text_input:
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Character Count", len(text_input))
        with col2:
            st.metric("Selected Models", len(st.session_state.selected_models))

        # Display comparison table
        if len(st.session_state.selected_models) > 0:
            st.subheader("Model Comparison")

            with st.spinner("Calculating token counts..."):
                df = get_model_comparison_data(
                    text_input, st.session_state.selected_models, api_keys
                )

            # Display the dataframe with custom styling
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

        # Disclaimers
        st.divider()
        st.caption("※ Token counts and prices are estimates. Actual usage may vary slightly.")
        st.caption(
            "※ Prices are for input tokens only and do not include batch API discounts, "
            "prompt caching, etc."
        )
    else:
        st.info("Enter text to see token counts")


if __name__ == "__main__":
    main()
