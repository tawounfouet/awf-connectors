.PHONY: help install test lint format clean check

help:
	@echo "Available commands:"
	@echo "  install    - Install project and development dependencies"
	@echo "  test       - Run tests with pytest"
	@echo "  lint       - Run Ruff and Mypy for linting and type checking"
	@echo "  format     - Run Black to format code"
	@echo "  check      - Run all checks (format, lint, test)"
	@echo "  clean      - Remove compiled files and cache"

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src/ tests/ examples/
	mypy src/

format:
	black src/ tests/ examples/

check: format lint test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf pyconnectors.egg-info
