# Repository Guidelines

## Project Structure & Module Organization
`app.py` hosts the Streamlit UI and token-cost logic (models, pricing, API dispatch). `pyproject.toml`, `uv.lock`, and `requirements.txt` define dependencies for uv-based installs and Streamlit Cloud deployments. The `Makefile` centralizes dev workflows, while `.streamlit/secrets.toml` (copied from the `.example`) stores Anthropic and Google API keys. The `src/` directory is reserved for future shared modules—prefer adding reusable helpers there rather than inflating `app.py`.

## Build, Test, and Development Commands
Run `uv sync` once to install dependencies. Use `make dev` (uv run streamlit run app.py) for the local app at http://localhost:8501. `make format`, `make lint`, and `make check` wrap Ruff auto-fix, lint-only, and lint+format verification respectively. `make clean` purges Python caches, and `make requirements` regenerates the pinned `requirements.txt` for deployments.

## Coding Style & Naming Conventions
Target Python 3.12, 4-space indentation, and Ruff’s 100-character line limit. Keep constants (model maps, pricing) UPPER_SNAKE_CASE, functions snake_case, and prefer descriptive Streamlit widget keys. Maintain type hints on public helpers (see `calculate_cost`). Run `make format` before opening a PR so Ruff normalizes imports and formatting.

## Testing Guidelines
There is no dedicated pytest suite yet; linting acts as the guardrail. Always run `make check` and then exercise the UI manually: load the main page, add/remove a model, and verify token counts update. When adding regression coverage, colocate tests beside the feature (e.g., `tests/test_tokens.py`) and name them `test_<behavior>()` for clarity.

## Commit & Pull Request Guidelines
Recent history favors concise, imperative subjects (e.g., `Added link to access the app on streamlit cloud`). Follow the same style, keep bodies wrapped at 72 chars, and reference issues when applicable. PRs should include: goal-oriented summary, manual test notes or command transcript, screenshots/gifs for UI tweaks, and links to tickets. Request review once CI/lint steps pass locally.

## Security & Configuration Tips
Never commit real API keys. Copy `.streamlit/secrets.toml.example`, edit locally, and rely on Streamlit Cloud secrets in production. Treat pricing tables as authoritative—validate values against provider docs before changing them. If you need new providers, gate them behind clearly named env vars and document the setup in README plus this guide.
