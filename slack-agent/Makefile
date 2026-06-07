.PHONY: help install dev test lint format type-check clean build publish

help:
	@echo "Agent Slouch Mode - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install package"
	@echo "  make dev          Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test         Run tests"
	@echo "  make lint         Check code style"
	@echo "  make format       Format code with Black"
	@echo "  make type-check   Run type checking with mypy"
	@echo ""
	@echo "Quality:"
	@echo "  make clean        Remove build artifacts"
	@echo ""
	@echo "Build & Release:"
	@echo "  make build        Build distribution package"
	@echo "  make publish      Publish to PyPI (requires credentials)"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest

test-verbose:
	pytest -v --cov=src/slouch_mode --cov-report=html

lint:
	ruff check src/ tests/

format:
	black src/ tests/

type-check:
	mypy src/

quality: lint type-check
	@echo "All quality checks passed!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/

build: clean
	python -m build

publish: build
	twine upload dist/*

run:
	slouch-mode

run-debug:
	SLOTH_LOG_LEVEL=DEBUG slouch-mode
