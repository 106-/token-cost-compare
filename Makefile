.PHONY: help dev format lint check clean install requirements test

help:
	@echo "Available commands:"
	@echo "  make dev          - Run Streamlit app in development mode"
	@echo "  make format       - Format code with ruff"
	@echo "  make lint         - Check code with ruff (no fixes)"
	@echo "  make check        - Run ruff check and format check"
	@echo "  make test         - Run unit tests with pytest"
	@echo "  make clean        - Remove Python cache files"
	@echo "  make install      - Install dependencies with uv"
	@echo "  make requirements - Generate requirements.txt for Streamlit deployment"

dev:
	uv run streamlit run app.py

format:
	uv run ruff check --fix app.py
	uv run ruff format app.py

lint:
	uv run ruff check app.py

check:
	uv run ruff check app.py
	uv run ruff format --check app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

install:
	uv sync

requirements:
	uv pip compile pyproject.toml -o requirements.txt
	@echo "requirements.txt generated successfully!"

test:
	uv run pytest tests/ -v
