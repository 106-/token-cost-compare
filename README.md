# Token Cost Compare

A Streamlit application that compares token counts and costs across three major LLM providers: **Claude**, **OpenAI**, and **Gemini**.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

You can use this app from link below:

https://token-cost-compare.streamlit.app/

## Features

- **Multi-Provider Comparison**: Compare token counts and costs side-by-side for Claude, OpenAI, and Gemini
- **Official APIs**: Uses official SDKs from Anthropic, OpenAI (tiktoken), and Google for accurate token counting
- **Real-time Token Counting**: Instant feedback as you type
- **File Upload Workflow**: Upload UTF-8 text files and batch-count tokens without copy/paste
- **Multipage UI**: Switch between text input and file upload flows via Streamlit's Pages sidebar
- **Cost Estimation**: Accurate pricing for input/output tokens
- **Multiple Models**: Support for 15+ models across all three providers
- **No OpenAI API Key Required**: Uses `tiktoken` for local OpenAI token counting

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

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/yourusername/combined-token-counter.git
cd combined-token-counter

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
```

**Note**: OpenAI API key is not required as token counting is done locally using `tiktoken`.

## Usage

```bash
# Run the Streamlit app
uv run streamlit run app.py
```

The app will be available at `http://localhost:8501`

### How to Use

1. **Pick a Workflow**: Use the Pages sidebar to open either "Text Input" or "File Upload".
2. **Provide Content**:
   - *Text Input*: Type or paste text into the editor.
   - *File Upload*: Select a UTF-8 `.txt`, `.md`, `.json`, `.csv`, or `.log` file.
3. **Select Models**: Add/remove models from the sidebar to focus on the providers you care about.
4. **Review Metrics**: Basic stats (characters, file size) appear above a comparison table with token counts and estimated costs.

## Project Structure

```
combined-token-counter/
├── app.py                          # Streamlit entry that links to sub-pages
├── pages/
│   ├── 0_Text_Input.py             # Manual text input workflow
│   └── 1_File_Upload.py            # UTF-8 file upload workflow
├── src/combined_token_counter/
│   ├── __init__.py
│   ├── config.py                   # Secrets/API key helpers
│   ├── model_registry.py           # Model metadata and pricing tables
│   ├── token_counting.py           # Token counting + cost utilities
│   └── ui.py                       # Shared sidebar/model selection widgets
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
- 2.5 Flash-Lite: $0.10 (in) / $0.40 (out) - **Most affordable!**
- 2.0 Flash: $0.10 (in) / $0.40 (out)
- 2.5 Pro: $1.25 (in) / $10.00 (out)

*Note: Prices may vary based on usage tier, caching, and other factors. Always check official pricing pages.*

## Dependencies

- `streamlit>=1.51.0` - Web framework
- `anthropic>=0.72.0` - Claude API client
- `tiktoken>=0.12.0` - OpenAI tokenizer (local)
- `google-genai>=1.49.0` - Gemini API client

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
# Run the app in development mode
uv run streamlit run app.py --server.runOnSave true
```

## License

MIT License - feel free to use this project for any purpose.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses official SDKs from [Anthropic](https://www.anthropic.com/), [OpenAI](https://openai.com/), and [Google](https://ai.google.dev/)
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

This tool is not affiliated with Anthropic, OpenAI, or Google.
