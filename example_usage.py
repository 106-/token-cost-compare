"""Example usage of TokenCounter class."""

from combined_token_counter import TokenCounter

# Initialize without API keys (can still use OpenAI models with local tiktoken)
counter = TokenCounter()

# Example text
text = "Hello, world! This is a sample text to count tokens and estimate costs."

print("=" * 80)
print("Token Counter Example Usage")
print("=" * 80)

# Count tokens for OpenAI model (no API key needed)
print("\n1. Counting tokens for GPT-4o (no API key needed):")
result = counter.count(text, "GPT-4o")
if result["success"]:
    print(f"   Tokens: {result['tokens']}")
    print(f"   Input Cost: ${result['cost']:.6f}")
    print(f"   Input Price: ${result['input_price']:.2f}/1M tokens")
    print(f"   Output Price: ${result['output_price']:.2f}/1M tokens")

# Compare across multiple OpenAI models
print("\n2. Comparing across OpenAI models:")
models = ["GPT-4o", "GPT-4o mini", "GPT-3.5 Turbo"]
results = counter.compare(text, models)

for result in results:
    if result["success"]:
        print(
            f"   {result['model_name']:20} | "
            f"Tokens: {result['tokens']:4} | "
            f"Cost: ${result['cost']:.6f}"
        )

# Get all available models
print("\n3. Available models:")
all_models = counter.get_available_models()
print(f"   Total models available: {len(all_models)}")
print(f"   Models: {', '.join(all_models[:5])}...")

# Get model info
print("\n4. Model information:")
info = counter.get_model_info("GPT-4o")
print(f"   Model: GPT-4o")
print(f"   Model ID: {info['id']}")
print(f"   Provider: {info['provider']}")
print(f"   Icon: {info['icon']}")

print("\n" + "=" * 80)
print("Note: To use Claude, Gemini, or Grok models, initialize with API keys:")
print("  counter = TokenCounter(")
print("      anthropic_api_key='your-key',")
print("      google_api_key='your-key',")
print("      xai_api_key='your-key'")
print("  )")
print("=" * 80)
