# Token Cost Compare - Development Guide

A Streamlit multipage application that compares token counts and costs across Claude, OpenAI, and Gemini.

**Live App:** https://token-cost-compare.streamlit.app/

## Quick Start

```bash
# Install dependencies
make install

# Run the app locally
make dev

# Format code
make format

# Lint code
make lint

# Generate requirements.txt for deployment
make requirements
```

## Architecture

### Multipage Structure

The codebase is organized as a Streamlit multipage app with modularized shared components:

```
token-cost-compare/
├── app.py                          # Entry point (directs to pages)
├── pages/
│   ├── 0_Text_Input.py             # Manual text input workflow
│   └── 1_File_Upload.py            # UTF-8 file upload workflow
└── src/token_cost_compare/
    ├── config.py                   # API key management
    ├── model_registry.py           # Model metadata and pricing
    ├── token_counting.py           # Token counting logic
    └── ui.py                       # Shared UI widgets
```

### Key Components

**model_registry.py**
- `ALL_MODELS`: Dict mapping model display names to metadata (provider, model_id, icon)
- `MODEL_PRICING`: Dict mapping model_ids to pricing info (input/output per million tokens)
- Supports 15+ models across Claude, OpenAI, and Gemini

**token_counting.py**
- `get_token_count(text, model_id, provider)`: Unified interface for all providers
- `count_tokens_with_claude()`: Uses Anthropic SDK's `messages.count_tokens()`
- `count_tokens_with_tiktoken()`: Local OpenAI tokenization (no API key needed)
- `count_tokens_with_gemini()`: Uses Google GenAI SDK's `models.count_tokens()`
- `calculate_cost()`: Computes cost from token count and pricing
- `get_model_comparison_data()`: Returns pandas DataFrame for table display

**config.py**
- Loads API keys from `.streamlit/secrets.toml`
- Required keys: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`
- OpenAI API key NOT required (uses tiktoken locally)

**ui.py**
- Shared Streamlit widgets for model selection
- Manages session state for dynamic model addition/removal

## Technology Stack

- **uv**: Dependency management (NOT pip/venv)
- **Streamlit**: Web framework with native multipage support
- **pandas**: DataFrame for comparison tables
- **ruff**: Linting and formatting with isort
- **Anthropic SDK**: Claude token counting API
- **tiktoken**: OpenAI local tokenizer
- **google-genai**: Gemini token counting API

## Development Workflow

### Adding Dependencies

```bash
# ALWAYS use uv add, never edit pyproject.toml manually
uv add package-name
```

### Adding New Models

1. Update `ALL_MODELS` in `src/token_cost_compare/model_registry.py`:
   ```python
   "Display Name": {
       "provider": "claude" | "openai" | "gemini",
       "model_id": "official-model-id",
       "icon": "🔷"
   }
   ```

2. Add pricing to `MODEL_PRICING`:
   ```python
   "official-model-id": {
       "input": 3.00,   # per million tokens
       "output": 15.00
   }
   ```

3. For new providers, add token counting logic to `src/token_cost_compare/token_counting.py`

### Code Style

- Line length: 100 characters
- Python 3.12+
- 4-space indentation
- Run `make format` before committing
- Imports sorted with isort (ruff handles this)
- Constants: UPPER_SNAKE_CASE
- Functions: snake_case
- Type hints on public helpers

## Session State Management

Both pages use Streamlit session state for dynamic model selection:

```python
if "selected_models" not in st.session_state:
    st.session_state.selected_models = ["Claude Sonnet 4.5", "GPT-4o", "Gemini 2.5 Flash"]

# Users can add/remove models dynamically
# Results displayed in pandas DataFrame table
```

## API Keys Setup

Create `.streamlit/secrets.toml` from the example:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Required keys:
- `ANTHROPIC_API_KEY`: Get from https://console.anthropic.com/
- `GOOGLE_API_KEY`: Get from https://aistudio.google.com/apikey

OpenAI key NOT required (tiktoken is local).

**Security Note:** Never commit real API keys. The secrets.toml file is gitignored. Use Streamlit Cloud secrets for production deployments.

## Deployment

Streamlit Cloud requires `requirements.txt`:

```bash
make requirements
```

This generates a pinned dependency file via `uv pip compile pyproject.toml -o requirements.txt`.

## Important Notes

1. **Use uv, not pip**: All dependency operations go through `uv add` or `uv sync`
2. **Model IDs must be current**: Check official docs for latest model identifiers (2025 models)
3. **Pricing updates**: Model pricing changes; verify with provider documentation
4. **No emoji by default**: Only add emojis if explicitly requested
5. **Secrets not in git**: `.streamlit/secrets.toml` is gitignored
6. **Table format for scaling**: Changed from columns to pandas DataFrame for better UX with many models
7. **Modular by design**: Common logic in src/, workflows in pages/

## Testing Locally

```bash
# Start app with auto-reload
uv run streamlit run app.py --server.runOnSave true
```

Navigate to:
- http://localhost:8501 - Landing page
- Use sidebar "Pages" navigation to switch between Text Input and File Upload

### Manual Testing Checklist

Always run `make check` and then exercise the UI manually:
- Load the main page
- Navigate to Text Input page
- Add/remove models from the comparison
- Verify token counts update correctly
- Test File Upload page with UTF-8 text files
- Check pricing calculations

## Common Tasks

| Task | Command |
|------|---------|
| Add dependency | `uv add package-name` |
| Run app | `make dev` |
| Format code | `make format` |
| Check linting | `make lint` |
| Clean cache | `make clean` |
| Sync dependencies | `uv sync` |
| Deploy prep | `make requirements` |

## Pricing Reference (2025)

### Claude
- Sonnet 4.5: $3.00 / $15.00 (in/out per 1M tokens)
- Haiku 4.5: $1.00 / $5.00
- Opus 4.1: $15.00 / $75.00
- 3.7 Sonnet: $3.00 / $15.00
- 3.5 Haiku: $0.80 / $4.00
- 3 Haiku: $0.25 / $1.25

### OpenAI
- GPT-5: $1.25 / $10.00
- GPT-4o: $2.50 / $10.00
- GPT-4o mini: $0.15 / $0.60
- GPT-4 Turbo: $10.00 / $30.00
- GPT-3.5 Turbo: $0.50 / $1.50

### Gemini
- 2.5 Flash: $0.30 / $2.50
- 2.5 Flash-Lite: $0.10 / $0.40 (most affordable)
- 2.0 Flash: $0.10 / $0.40
- 2.5 Pro: $1.25 / $10.00

**Treat pricing tables as authoritative—validate values against provider docs before changing them.**

## Git Configuration

Current author: `106- <segmentation-fault@yandex.com>`

If commit author is wrong:
```bash
git commit --amend --author="106- <segmentation-fault@yandex.com>" --no-edit
git push --force-with-lease origin main
```

## Commit & Pull Request Guidelines

Recent history favors concise, imperative subjects (e.g., "Added link to access the app on streamlit cloud"). Follow the same style:

- Keep subject lines concise and imperative
- Wrap commit bodies at 72 characters
- Reference issues when applicable
- PRs should include:
  - Goal-oriented summary
  - Manual test notes or command transcript
  - Screenshots/gifs for UI tweaks
  - Links to tickets
- Request review once CI/lint steps pass locally

## Known Issues & Solutions

- **Claude 404 errors**: Check model IDs are current (use 2025 models like `claude-sonnet-4-5-20250929`)
- **Import errors after adding deps**: Restart Streamlit process completely
- **README rendering**: Avoid special control characters in markdown
- **Secrets not loading**: Ensure `.streamlit/secrets.toml` exists and has correct TOML format

## Future Enhancement Areas

When adding regression coverage, colocate tests beside the feature (e.g., `tests/test_tokens.py`) and name them `test_<behavior>()` for clarity.

Potential enhancements:
- Additional providers (Mistral, Cohere, etc.)
- Batch processing for multiple files
- Export comparison results to CSV/JSON
- Cost tracking over time
- Custom pricing configurations
- Image/PDF token counting support
- pytest suite for automated testing
