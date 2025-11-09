"""Token counter class for programmatic use without Streamlit dependencies."""

from __future__ import annotations

from typing import Dict, List, Optional

from .model_registry import ALL_MODELS, get_pricing
from .token_counting import calculate_cost, get_token_count


class TokenCounter:
    """Token counter with API key management for programmatic usage.

    Example:
        >>> counter = TokenCounter(
        ...     anthropic_api_key="sk-ant-...",
        ...     google_api_key="AI...",
        ...     xai_api_key="xai-..."
        ... )
        >>> result = counter.count("Hello, world!", "Claude Sonnet 4.5")
        >>> print(result["tokens"], result["cost"])
    """

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        google_api_key: Optional[str] = None,
        xai_api_key: Optional[str] = None,
    ):
        """Initialize TokenCounter with API keys.

        Args:
            anthropic_api_key: API key for Claude models
            google_api_key: API key for Gemini models
            xai_api_key: API key for Grok models (OpenAI models don't require a key)
        """
        self._api_keys = {
            "anthropic": anthropic_api_key,
            "google": google_api_key,
            "xai": xai_api_key,
        }

    def count(
        self, text: str, model_name: str, token_type: str = "input"
    ) -> Dict[str, int | float | bool | str]:
        """Count tokens and calculate cost for the given text and model.

        Args:
            text: Text to count tokens for
            model_name: Display name of the model (e.g., "Claude Sonnet 4.5", "GPT-4o")
            token_type: Type of tokens ("input" or "output") for cost calculation

        Returns:
            Dictionary with:
                - success (bool): Whether the operation succeeded
                - tokens (int): Number of tokens (if success)
                - cost (float): Cost in USD (if success)
                - input_price (float): Input price per 1M tokens (if success)
                - output_price (float): Output price per 1M tokens (if success)
                - error (str): Error message (if not success)

        Raises:
            KeyError: If model_name is not found in ALL_MODELS
        """
        if model_name not in ALL_MODELS:
            available = ", ".join(ALL_MODELS.keys())
            return {
                "success": False,
                "error": f"Unknown model: {model_name}. Available models: {available}",
            }

        model_info = ALL_MODELS[model_name]
        model_id = model_info["id"]
        pricing = get_pricing(model_id)

        result = get_token_count(text, model_name, self._api_keys)

        if not result["success"]:
            return result

        tokens = result["input_tokens"]
        cost = calculate_cost(tokens, pricing, token_type)

        return {
            "success": True,
            "tokens": tokens,
            "cost": cost,
            "input_price": pricing.get("input", 0.0),
            "output_price": pricing.get("output", 0.0),
            "model_id": model_id,
            "provider": model_info["provider"],
        }

    def compare(
        self, text: str, model_names: Optional[List[str]] = None
    ) -> List[Dict[str, int | float | bool | str]]:
        """Compare token counts and costs across multiple models.

        Args:
            text: Text to count tokens for
            model_names: List of model display names. If None, uses all available models.

        Returns:
            List of dictionaries, each containing the result from count() plus model_name
        """
        if model_names is None:
            model_names = list(ALL_MODELS.keys())

        results = []
        for model_name in model_names:
            result = self.count(text, model_name)
            result["model_name"] = model_name
            results.append(result)

        return results

    def get_available_models(self) -> List[str]:
        """Get list of all available model names.

        Returns:
            List of model display names
        """
        return list(ALL_MODELS.keys())

    def get_model_info(self, model_name: str) -> Dict[str, str]:
        """Get information about a specific model.

        Args:
            model_name: Display name of the model

        Returns:
            Dictionary with model_id, provider, and icon

        Raises:
            KeyError: If model_name is not found
        """
        if model_name not in ALL_MODELS:
            raise KeyError(f"Unknown model: {model_name}")
        return ALL_MODELS[model_name]
