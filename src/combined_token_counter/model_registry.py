"""Model metadata and pricing tables shared by the application."""

from __future__ import annotations

from typing import Dict

ModelInfo = Dict[str, str]

ALL_MODELS: Dict[str, Dict[str, str]] = {
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
MODEL_PRICING: Dict[str, Dict[str, float]] = {
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


def get_model_info(name: str) -> ModelInfo:
    """Return the metadata dictionary for a model name."""

    try:
        return ALL_MODELS[name]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(f"Unknown model: {name}") from exc


def get_pricing(model_id: str) -> Dict[str, float]:
    """Return pricing data for the given model id."""

    return MODEL_PRICING.get(model_id, {})
