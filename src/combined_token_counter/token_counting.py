"""Token counting helpers shared across UI surfaces."""

from __future__ import annotations

from typing import Dict, List

import pandas as pd
import tiktoken
from anthropic import Anthropic
from google import genai
from xai_sdk import Client as XAIClient

from .model_registry import ALL_MODELS, get_pricing

ApiKeyMap = Dict[str, str | None]


def calculate_cost(tokens: int, pricing_dict: Dict[str, float], token_type: str = "input") -> float:
    """Calculate the dollar cost for the given token count."""

    if not pricing_dict:
        return 0.0
    price_per_million = pricing_dict.get(token_type, 0.0)
    return (tokens / 1_000_000) * price_per_million


def count_tokens_with_tiktoken(text: str, model: str) -> int:
    """Count tokens using the local tiktoken encoder."""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except Exception:  # pragma: no cover - fallback path
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def count_tokens_with_gemini(text: str, model: str, api_key: str) -> Dict[str, int | bool | str]:
    """Count tokens using the Gemini API."""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.count_tokens(model=model, contents=text)
        return {"success": True, "input_tokens": response.total_tokens}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def count_tokens_with_claude(text: str, model: str, api_key: str) -> Dict[str, int | bool | str]:
    """Count tokens using the Claude API."""

    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.count_tokens(
            model=model, messages=[{"role": "user", "content": text}]
        )
        return {"success": True, "input_tokens": response.input_tokens}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def count_tokens_with_grok(text: str, model: str, api_key: str) -> Dict[str, int | bool | str]:
    """Count tokens using the xAI Grok API."""

    try:
        client = XAIClient(api_key=api_key)
        tokens = client.tokenize.tokenize_text(text=text, model=model)
        return {"success": True, "input_tokens": len(tokens)}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def get_token_count(text: str, model_name: str, api_keys: ApiKeyMap) -> Dict[str, int | bool | str]:
    """Get the token count for a single model entry."""

    model_info = ALL_MODELS[model_name]
    model_id = model_info["id"]
    provider = model_info["provider"]

    if provider == "openai":
        tokens = count_tokens_with_tiktoken(text, model_id)
        return {"success": True, "input_tokens": tokens}
    if provider == "claude":
        if not api_keys.get("anthropic"):
            return {"success": False, "error": "Claude API key not configured"}
        return count_tokens_with_claude(text, model_id, api_keys["anthropic"] or "")
    if provider == "gemini":
        if not api_keys.get("google"):
            return {"success": False, "error": "Gemini API key not configured"}
        return count_tokens_with_gemini(text, model_id, api_keys["google"] or "")
    if provider == "grok":
        if not api_keys.get("xai"):
            return {"success": False, "error": "xAI API key not configured"}
        return count_tokens_with_grok(text, model_id, api_keys["xai"] or "")

    return {"success": False, "error": f"Unsupported provider: {provider}"}


def get_model_comparison_data(
    text: str, selected_models: List[str], api_keys: ApiKeyMap
) -> pd.DataFrame:
    """Return a comparison table for the selected models."""

    data = []

    for model_name in selected_models:
        model_info = ALL_MODELS[model_name]
        icon = model_info["icon"]
        model_id = model_info["id"]
        pricing = get_pricing(model_id)

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
