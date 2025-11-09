# Token Cost Compare

A token counting and cost comparison tool for four major LLM providers: **Claude**, **OpenAI**, **Gemini**, and **Grok**.

Use it as a **Streamlit web app** or as a **Python module** in your code.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Try the web app:** https://token-cost-compare.streamlit.app/

## Features

- **Dual Usage**: Use as a Streamlit web app or import as a Python module in your code
- **Multi-Provider Comparison**: Compare token counts and costs side-by-side for Claude, OpenAI, Gemini, and Grok
- **Official APIs**: Uses official SDKs from Anthropic, OpenAI (tiktoken), Google, and xAI for accurate token counting
- **Real-time Token Counting**: Instant feedback as you type (web app)
- **File Upload Workflow**: Upload UTF-8 text files and batch-count tokens without copy/paste (web app)
- **Multipage UI**: Switch between text input and file upload flows via Streamlit's Pages sidebar (web app)
- **Programmatic Access**: Use TokenCounter class in your Python scripts with simple API (module)
- **Cost Estimation**: Accurate pricing for input/output tokens
- **Multiple Models**: Support for 19+ models across all four providers
- **No OpenAI API Key Required**: Uses `tiktoken` for local OpenAI token counting
- **Per-Character Cost Analysis**: File upload page includes cost per character metric (web app)

## Supported Models

### Claude (Anthropic)
- Claude Sonnet 4.5
- Claude Haiku 4.5
- Claude Opus 4.1
- Claude 3.7 Sonnet
- Claude 3.5 Haiku
- Claude 3 Haiku

### OpenAI
- GPT-5
- GPT-4o
- GPT-4o mini
- GPT-4 Turbo
- GPT-3.5 Turbo

### Gemini (Google)
- Gemini 2.5 Flash
- Gemini 2.5 Flash-Lite
- Gemini 2.0 Flash
- Gemini 2.5 Pro

### Grok (xAI)
- Grok 3
- Grok 3 Mini
- Grok 4
- Grok 4 Fast

## Installation

### As a Python Package

You can install this package directly from GitHub without cloning the repository:

```bash
# Using pip
pip install git+https://github.com/106-/token-cost-compare.git

# Using uv
uv pip install git+https://github.com/106-/token-cost-compare.git
```

Or add it to your `requirements.txt`:

```txt
# Install from main branch
git+https://github.com/106-/token-cost-compare.git

# Install from specific branch
git+https://github.com/106-/token-cost-compare.git@main

# Install from specific tag or commit
git+https://github.com/106-/token-cost-compare.git@v1.0.0
```

Then install with:

```bash
pip install -r requirements.txt
# or
uv pip install -r requirements.txt
```

### For Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/106-/token-cost-compare.git
cd token-cost-compare

# Install dependencies
uv sync
```

## Configuration

Create a `.streamlit/secrets.toml` file from the example:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your API keys:

```toml
# Anthropic API Key
# Get your API key from https://console.anthropic.com/
ANTHROPIC_API_KEY = "sk-ant-your-api-key-here"

# Google API Key (for Gemini)
# Get your API key from https://aistudio.google.com/apikey
GOOGLE_API_KEY = "your-google-api-key-here"

# xAI API Key (for Grok)
# Get your API key from https://console.x.ai/
XAI_API_KEY = "your-xai-api-key-here"
```

**Note**: OpenAI API key is not required as token counting is done locally using `tiktoken`.

## Usage

### As a Streamlit Web App

```bash
# Run the Streamlit app
uv run streamlit run app.py
```

The app will be available at `http://localhost:8501`

#### How to Use the Web App

1. **Pick a Workflow**: Use the Pages sidebar to open either "Text Input" or "File Upload".
2. **Provide Content**:
   - *Text Input*: Type or paste text into the editor.
   - *File Upload*: Select a UTF-8 `.txt`, `.md`, `.json`, `.csv`, or `.log` file.
3. **Select Models**: Add/remove models from the sidebar to focus on the providers you care about.
4. **Review Metrics**: Basic stats (characters, file size) appear above a comparison table with token counts and estimated costs.

### As a Python Module

You can also use this package programmatically in your Python code:

```python
from token_cost_compare import TokenCounter

# Initialize with API keys
counter = TokenCounter(
    anthropic_api_key="sk-ant-...",  # Required for Claude models
    google_api_key="AI...",          # Required for Gemini models
    xai_api_key="xai-..."            # Required for Grok models
)

# Count tokens for a single model
text = "Hello, world! This is a test message."
result = counter.count(text, "GPT-4o")

if result["success"]:
    print(f"Tokens: {result['tokens']}")
    print(f"Cost: ${result['cost']:.6f}")
    print(f"Input price: ${result['input_price']:.2f}/1M tokens")
    print(f"Output price: ${result['output_price']:.2f}/1M tokens")

# Compare across multiple models
models = ["GPT-4o", "Claude Sonnet 4.5", "Gemini 2.5 Flash"]
results = counter.compare(text, models)

for result in results:
    if result["success"]:
        print(f"{result['model_name']}: {result['tokens']} tokens, ${result['cost']:.6f}")

# Get available models
models = counter.get_available_models()
print(f"Available models: {models}")

# Get model information
info = counter.get_model_info("GPT-4o")
print(f"Model ID: {info['id']}, Provider: {info['provider']}")
```

#### TokenCounter API

**`__init__(anthropic_api_key=None, google_api_key=None, xai_api_key=None)`**
- Initialize the token counter with API keys
- OpenAI models don't require an API key (uses local tiktoken)

**`count(text, model_name, token_type="input")`**
- Count tokens and calculate cost for given text
- Returns dict with `success`, `tokens`, `cost`, `input_price`, `output_price`, etc.
- `token_type` can be "input" or "output" for cost calculation

**`compare(text, model_names=None)`**
- Compare tokens across multiple models
- If `model_names` is None, compares all available models
- Returns list of dicts with results for each model

**`get_available_models()`**
- Returns list of all available model display names

**`get_model_info(model_name)`**
- Returns dict with `id`, `provider`, and `icon` for the model

## Project Structure

```
token-cost-compare/
├── app.py                          # Streamlit entry that links to sub-pages
├── pages/
│   ├── 0_Text_Input.py             # Manual text input workflow
│   └── 1_File_Upload.py            # UTF-8 file upload workflow
├── src/token_cost_compare/
│   ├── __init__.py
│   ├── config.py                   # Secrets/API key helpers
│   ├── counter.py                  # TokenCounter class for programmatic use
│   ├── model_registry.py           # Model metadata and pricing tables
│   ├── token_counting.py           # Token counting + cost utilities
│   └── ui.py                       # Shared sidebar/model selection widgets
├── tests/
│   └── test_counter.py             # Unit tests for TokenCounter
├── pyproject.toml                  # Project dependencies (uv)
├── Makefile                        # Development commands
├── requirements.txt                # Frozen dependencies (for deployment)
├── .streamlit/
│   ├── secrets.toml.example        # Example secrets file
│   └── secrets.toml                # Your API keys (gitignored)
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Pricing Information (2025)

All prices are per million tokens (USD):

### Claude
- Sonnet 4.5: $3.00 (in) / $15.00 (out)
- Haiku 4.5: $1.00 (in) / $5.00 (out)
- Opus 4.1: $15.00 (in) / $75.00 (out)

### OpenAI
- GPT-5: $1.25 (in) / $10.00 (out)
- GPT-4o: $2.50 (in) / $10.00 (out)
- GPT-4o mini: $0.15 (in) / $0.60 (out)

### Gemini
- 2.5 Flash: $0.30 (in) / $2.50 (out)
- 2.5 Flash-Lite: $0.10 (in) / $0.40 (out)
- 2.0 Flash: $0.10 (in) / $0.40 (out)
- 2.5 Pro: $1.25 (in) / $10.00 (out)

### Grok
- Grok 3: $3.00 (in) / $15.00 (out)
- Grok 3 Mini: $0.30 (in) / $0.50 (out)
- Grok 4: $3.00 (in) / $15.00 (out)
- Grok 4 Fast: $0.20 (in) / $0.50 (out)

*Note: Prices may vary based on usage tier, caching, and other factors. Always check official pricing pages.*

## Dependencies

- `streamlit>=1.51.0` - Web framework
- `anthropic>=0.72.0` - Claude API client
- `tiktoken>=0.12.0` - OpenAI tokenizer (local)
- `google-genai>=1.49.0` - Gemini API client
- `xai-sdk>=1.4.0` - Grok API client

## Development

### Adding New Models

1. Update the model dictionary in `app.py`:
   ```python
   PROVIDER_MODELS = {
       "Model Name": "model-id",
   }
   ```

2. Add pricing information:
   ```python
   PROVIDER_PRICING = {
       "model-id": {"input": X.XX, "output": Y.YY},
   }
   ```

### Running Tests

```bash
# Run unit tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src/token_cost_compare --cov-report=html

# Run the app in development mode
uv run streamlit run app.py --server.runOnSave true
```

## License

MIT License - feel free to use this project for any purpose.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses official SDKs from [Anthropic](https://www.anthropic.com/), [OpenAI](https://openai.com/), [Google](https://ai.google.dev/), and [xAI](https://x.ai/)
- Dependency management by [uv](https://github.com/astral-sh/uv)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Disclaimer

Token counts and pricing are estimates and may differ from actual usage. Always refer to official provider documentation for the most accurate information.

This tool is not affiliated with Anthropic, OpenAI, Google, or xAI.
