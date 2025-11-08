import streamlit as st
import tiktoken
from anthropic import Anthropic
from google import genai

# Available Claude models
CLAUDE_MODELS = {
    "Claude Sonnet 4.5 (Recommended)": "claude-sonnet-4-5-20250929",
    "Claude Haiku 4.5": "claude-haiku-4-5-20251001",
    "Claude Opus 4.1": "claude-opus-4-1-20250805",
    "Claude 3.7 Sonnet": "claude-3-7-sonnet-20250219",
    "Claude 3.5 Haiku": "claude-3-5-haiku-20241022",
    "Claude 3 Haiku": "claude-3-haiku-20240307",
}

# Claude model pricing (USD per million tokens)
MODEL_PRICING = {
    "claude-sonnet-4-5-20250929": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "claude-opus-4-1-20250805": {"input": 15.00, "output": 75.00},
    "claude-3-7-sonnet-20250219": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
}

# Available OpenAI models
OPENAI_MODELS = {
    "GPT-5": "gpt-5",
    "GPT-4o": "gpt-4o",
    "GPT-4o mini": "gpt-4o-mini",
    "GPT-4 Turbo": "gpt-4-turbo",
    "GPT-3.5 Turbo": "gpt-3.5-turbo",
}

# OpenAI model pricing (USD per million tokens)
OPENAI_PRICING = {
    "gpt-5": {"input": 1.25, "output": 10.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
}

# Available Gemini models
GEMINI_MODELS = {
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.5 Flash-Lite": "gemini-2.5-flash-lite",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 2.5 Pro": "gemini-2.5-pro",
}

# Gemini model pricing (USD per million tokens)
GEMINI_PRICING = {
    "gemini-2.5-flash": {"input": 0.30, "output": 2.50},
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},  # <200K tokens
}


def calculate_cost(tokens: int, pricing_dict: dict, token_type: str = "input") -> float:
    """
    Calculate cost from token count.

    Args:
        tokens: Number of tokens
        pricing_dict: Pricing information dictionary
        token_type: "input" or "output"

    Returns:
        Cost in USD
    """
    if not pricing_dict:
        return 0.0

    price_per_million = pricing_dict.get(token_type, 0.0)
    return (tokens / 1_000_000) * price_per_million


def count_tokens_with_tiktoken(text: str, model: str) -> int:
    """
    Count tokens using tiktoken.

    Args:
        text: Text to count tokens for
        model: OpenAI model name

    Returns:
        Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # Use default encoding if model not found
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))


def count_tokens_with_gemini(text: str, model: str, api_key: str) -> dict:
    """
    Count tokens using Gemini API.

    Args:
        text: Text to count tokens for
        model: Gemini model to use
        api_key: Google API Key

    Returns:
        Dictionary containing token count
    """
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.count_tokens(
            model=model,
            contents=text,
        )

        return {
            "success": True,
            "input_tokens": response.total_tokens,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def count_tokens_with_claude(text: str, model: str, api_key: str) -> dict:
    """
    Count tokens using Claude API.

    Args:
        text: Text to count tokens for
        model: Claude model to use
        api_key: Anthropic API key

    Returns:
        Dictionary containing token count
    """
    try:
        client = Anthropic(api_key=api_key)

        response = client.messages.count_tokens(
            model=model,
            messages=[{"role": "user", "content": text}],
        )

        return {
            "success": True,
            "input_tokens": response.input_tokens,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def main():
    st.title("Token Counter")
    st.write("Compare token counts and costs across Claude, OpenAI, and Gemini")

    # Get API keys from Streamlit secrets
    try:
        anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        anthropic_api_key = None

    try:
        google_api_key = st.secrets["GOOGLE_API_KEY"]
    except (KeyError, FileNotFoundError):
        google_api_key = None

    # Sidebar settings
    with st.sidebar:
        st.header("Settings")

        # Claude model selection
        st.subheader("Claude")
        claude_model_name = st.selectbox(
            "Claude Model", options=list(CLAUDE_MODELS.keys()), help="Select Claude model"
        )
        claude_model_id = CLAUDE_MODELS[claude_model_name]

        # OpenAI model selection
        st.subheader("OpenAI")
        openai_model_name = st.selectbox(
            "OpenAI Model", options=list(OPENAI_MODELS.keys()), help="Select OpenAI model"
        )
        openai_model_id = OPENAI_MODELS[openai_model_name]

        # Gemini model selection
        st.subheader("Gemini")
        gemini_model_name = st.selectbox(
            "Gemini Model", options=list(GEMINI_MODELS.keys()), help="Select Gemini model"
        )
        gemini_model_id = GEMINI_MODELS[gemini_model_name]

        # API key status
        st.divider()
        st.subheader("API Key Status")
        if anthropic_api_key:
            st.success("✓ Claude API key configured")
        else:
            st.error("✗ Claude API key not set")

        if google_api_key:
            st.success("✓ Google API key configured")
        else:
            st.error("✗ Google API key not set")

    # Text input area
    text_input = st.text_area(
        "Enter your text", height=200, placeholder="Type or paste your text here..."
    )

    # Calculate and display token counts
    if text_input:
        st.subheader("Basic Information")
        st.metric("Character Count", len(text_input))

        # 3-column layout: Claude vs OpenAI vs Gemini
        col1, col2, col3 = st.columns(3)

        # Claude column
        with col1:
            st.subheader("🤖 Claude")

            if not anthropic_api_key:
                st.warning("⚠️ API key not configured")
                st.info("Please set your API key in `.streamlit/secrets.toml`")
                st.code('ANTHROPIC_API_KEY = "sk-ant-..."', language="toml")
            else:
                with st.spinner("Calculating..."):
                    claude_result = count_tokens_with_claude(
                        text_input, claude_model_id, anthropic_api_key
                    )

                if claude_result["success"]:
                    claude_tokens = claude_result["input_tokens"]
                    claude_pricing = MODEL_PRICING.get(claude_model_id, {})
                    claude_cost = calculate_cost(claude_tokens, claude_pricing, "input")

                    st.metric("Token Count", claude_tokens)
                    st.metric("Input Cost", f"${claude_cost:.6f}")

                    st.caption(f"**Model**: {claude_model_name}")
                    st.caption(f"**Input**: ${claude_pricing.get('input', 0):.2f} / 1M tokens")
                    st.caption(f"**Output**: ${claude_pricing.get('output', 0):.2f} / 1M tokens")
                else:
                    st.error(f"❌ Error: {claude_result['error']}")

        # OpenAI column
        with col2:
            st.subheader("🔷 OpenAI")

            openai_tokens = count_tokens_with_tiktoken(text_input, openai_model_id)
            openai_pricing = OPENAI_PRICING.get(openai_model_id, {})
            openai_cost = calculate_cost(openai_tokens, openai_pricing, "input")

            st.metric("Token Count", openai_tokens)
            st.metric("Input Cost", f"${openai_cost:.6f}")

            st.caption(f"**Model**: {openai_model_name}")
            st.caption(f"**Input**: ${openai_pricing.get('input', 0):.2f} / 1M tokens")
            st.caption(f"**Output**: ${openai_pricing.get('output', 0):.2f} / 1M tokens")

        # Gemini column
        with col3:
            st.subheader("💎 Gemini")

            if not google_api_key:
                st.warning("⚠️ API key not configured")
                st.info("Please set your API key in `.streamlit/secrets.toml`")
                st.code('GOOGLE_API_KEY = "..."', language="toml")
            else:
                with st.spinner("Calculating..."):
                    gemini_result = count_tokens_with_gemini(
                        text_input, gemini_model_id, google_api_key
                    )

                if gemini_result["success"]:
                    gemini_tokens = gemini_result["input_tokens"]
                    gemini_pricing = GEMINI_PRICING.get(gemini_model_id, {})
                    gemini_cost = calculate_cost(gemini_tokens, gemini_pricing, "input")

                    st.metric("Token Count", gemini_tokens)
                    st.metric("Input Cost", f"${gemini_cost:.6f}")

                    st.caption(f"**Model**: {gemini_model_name}")
                    st.caption(f"**Input**: ${gemini_pricing.get('input', 0):.2f} / 1M tokens")
                    st.caption(f"**Output**: ${gemini_pricing.get('output', 0):.2f} / 1M tokens")
                else:
                    st.error(f"❌ Error: {gemini_result['error']}")

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
