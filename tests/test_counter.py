"""Unit tests for TokenCounter class with mocked API calls."""

from unittest.mock import MagicMock, patch

import pytest

from combined_token_counter import TokenCounter


class TestTokenCounter:
    """Test suite for TokenCounter class."""

    def test_init_with_api_keys(self):
        """Test TokenCounter initialization with API keys."""
        counter = TokenCounter(
            anthropic_api_key="test-anthropic-key",
            google_api_key="test-google-key",
            xai_api_key="test-xai-key",
        )
        assert counter._api_keys["anthropic"] == "test-anthropic-key"
        assert counter._api_keys["google"] == "test-google-key"
        assert counter._api_keys["xai"] == "test-xai-key"

    def test_init_without_api_keys(self):
        """Test TokenCounter initialization without API keys."""
        counter = TokenCounter()
        assert counter._api_keys["anthropic"] is None
        assert counter._api_keys["google"] is None
        assert counter._api_keys["xai"] is None

    @patch("combined_token_counter.counter.get_token_count")
    def test_count_success(self, mock_get_token_count):
        """Test successful token counting."""
        mock_get_token_count.return_value = {"success": True, "input_tokens": 100}

        counter = TokenCounter()
        result = counter.count("Hello, world!", "GPT-4o")

        assert result["success"] is True
        assert result["tokens"] == 100
        assert "cost" in result
        assert "input_price" in result
        assert "output_price" in result
        assert result["model_id"] == "gpt-4o"
        assert result["provider"] == "openai"

    @patch("combined_token_counter.counter.get_token_count")
    def test_count_with_output_token_type(self, mock_get_token_count):
        """Test token counting with output token type."""
        mock_get_token_count.return_value = {"success": True, "input_tokens": 50}

        counter = TokenCounter()
        result = counter.count("Response text", "Claude Sonnet 4.5", token_type="output")

        assert result["success"] is True
        assert result["tokens"] == 50
        # Output pricing should be used for cost calculation
        assert result["cost"] > 0

    @patch("combined_token_counter.counter.get_token_count")
    def test_count_api_error(self, mock_get_token_count):
        """Test token counting when API returns an error."""
        mock_get_token_count.return_value = {
            "success": False,
            "error": "API key not configured",
        }

        counter = TokenCounter()
        result = counter.count("Hello", "Claude Sonnet 4.5")

        assert result["success"] is False
        assert "error" in result
        assert result["error"] == "API key not configured"

    def test_count_invalid_model(self):
        """Test token counting with invalid model name."""
        counter = TokenCounter()
        result = counter.count("Hello", "NonExistentModel")

        assert result["success"] is False
        assert "Unknown model" in result["error"]

    @patch("combined_token_counter.counter.get_token_count")
    def test_compare_multiple_models(self, mock_get_token_count):
        """Test comparing token counts across multiple models."""

        def mock_token_count(text, model_name, api_keys):
            return {"success": True, "input_tokens": len(text) * 10}

        mock_get_token_count.side_effect = mock_token_count

        counter = TokenCounter()
        models = ["GPT-4o", "GPT-4o mini", "Claude Sonnet 4.5"]
        results = counter.compare("Test", models)

        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["success"] is True
            assert result["model_name"] == models[i]
            assert "tokens" in result
            assert "cost" in result

    @patch("combined_token_counter.counter.get_token_count")
    def test_compare_all_models(self, mock_get_token_count):
        """Test comparing without specifying models (uses all models)."""
        mock_get_token_count.return_value = {"success": True, "input_tokens": 42}

        counter = TokenCounter()
        results = counter.compare("Test")

        # Should return results for all available models
        assert len(results) > 0
        assert all("model_name" in result for result in results)

    @patch("combined_token_counter.counter.get_token_count")
    def test_compare_with_errors(self, mock_get_token_count):
        """Test compare when some models fail."""

        def mock_token_count(text, model_name, api_keys):
            if "Claude" in model_name:
                return {"success": False, "error": "API key not configured"}
            return {"success": True, "input_tokens": 100}

        mock_get_token_count.side_effect = mock_token_count

        counter = TokenCounter()
        models = ["GPT-4o", "Claude Sonnet 4.5"]
        results = counter.compare("Test", models)

        assert len(results) == 2
        assert results[0]["success"] is True
        assert results[1]["success"] is False
        assert "error" in results[1]

    def test_get_available_models(self):
        """Test getting list of available models."""
        counter = TokenCounter()
        models = counter.get_available_models()

        assert isinstance(models, list)
        assert len(models) > 0
        assert "GPT-4o" in models
        assert "Claude Sonnet 4.5" in models

    def test_get_model_info_success(self):
        """Test getting model information."""
        counter = TokenCounter()
        info = counter.get_model_info("GPT-4o")

        assert info["id"] == "gpt-4o"
        assert info["provider"] == "openai"
        assert "icon" in info

    def test_get_model_info_invalid(self):
        """Test getting model info for invalid model."""
        counter = TokenCounter()

        with pytest.raises(KeyError, match="Unknown model"):
            counter.get_model_info("InvalidModel")


class TestTokenCounterIntegration:
    """Integration tests with real tokenizers (mocking only API calls)."""

    @patch("combined_token_counter.token_counting.Anthropic")
    def test_claude_token_counting(self, mock_anthropic):
        """Test Claude token counting with mocked API."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.input_tokens = 15
        mock_client.messages.count_tokens.return_value = mock_response
        mock_anthropic.return_value = mock_client

        counter = TokenCounter(anthropic_api_key="test-key")
        result = counter.count("Hello, world!", "Claude Sonnet 4.5")

        assert result["success"] is True
        assert result["tokens"] == 15
        assert result["cost"] > 0
        mock_client.messages.count_tokens.assert_called_once()

    def test_openai_token_counting_no_api_key(self):
        """Test OpenAI token counting without API key (uses local tiktoken)."""
        counter = TokenCounter()
        result = counter.count("Hello, world!", "GPT-4o")

        # Should work without API key because tiktoken is local
        assert result["success"] is True
        assert result["tokens"] > 0
        assert isinstance(result["tokens"], int)

    @patch("combined_token_counter.token_counting.genai.Client")
    def test_gemini_token_counting(self, mock_genai_client):
        """Test Gemini token counting with mocked API."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.total_tokens = 20
        mock_client.models.count_tokens.return_value = mock_response
        mock_genai_client.return_value = mock_client

        counter = TokenCounter(google_api_key="test-key")
        result = counter.count("Hello, world!", "Gemini 2.5 Flash")

        assert result["success"] is True
        assert result["tokens"] == 20
        mock_client.models.count_tokens.assert_called_once()

    @patch("combined_token_counter.token_counting.XAIClient")
    def test_grok_token_counting(self, mock_xai_client):
        """Test Grok token counting with mocked API."""
        mock_client = MagicMock()
        mock_client.tokenize.tokenize_text.return_value = [1, 2, 3, 4, 5]
        mock_xai_client.return_value = mock_client

        counter = TokenCounter(xai_api_key="test-key")
        result = counter.count("Hello, world!", "Grok 3")

        assert result["success"] is True
        assert result["tokens"] == 5
        mock_client.tokenize.tokenize_text.assert_called_once()


class TestTokenCounterPricing:
    """Test pricing calculations."""

    @patch("combined_token_counter.counter.get_token_count")
    def test_input_cost_calculation(self, mock_get_token_count):
        """Test input token cost calculation."""
        mock_get_token_count.return_value = {"success": True, "input_tokens": 1_000_000}

        counter = TokenCounter()
        result = counter.count("Large text", "GPT-4o", token_type="input")

        # GPT-4o input price is $2.50 per 1M tokens
        assert result["success"] is True
        assert result["cost"] == pytest.approx(2.50, rel=0.01)

    @patch("combined_token_counter.counter.get_token_count")
    def test_output_cost_calculation(self, mock_get_token_count):
        """Test output token cost calculation."""
        mock_get_token_count.return_value = {"success": True, "input_tokens": 1_000_000}

        counter = TokenCounter()
        result = counter.count("Large text", "GPT-4o", token_type="output")

        # GPT-4o output price is $10.00 per 1M tokens
        assert result["success"] is True
        assert result["cost"] == pytest.approx(10.00, rel=0.01)

    @patch("combined_token_counter.counter.get_token_count")
    def test_cost_calculation_small_tokens(self, mock_get_token_count):
        """Test cost calculation for small token counts."""
        mock_get_token_count.return_value = {"success": True, "input_tokens": 100}

        counter = TokenCounter()
        result = counter.count("Small text", "Claude Sonnet 4.5")

        # Claude Sonnet 4.5 input price is $3.00 per 1M tokens
        # 100 tokens = 100/1M * 3.00 = 0.0003
        assert result["success"] is True
        assert result["cost"] == pytest.approx(0.0003, rel=0.01)
