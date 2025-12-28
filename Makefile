PYTHON_FILES = $(shell find src tests -iname "*.py" -not -path "**/__pycache__/**")

.PHONY: setup setup-hard format format-check lint lint-fix types test test-coverage uv-lock uv-update help

setup: ## Install developer experience
	@uv sync
	@uv run pre-commit install --install-hooks || echo "Warning: pre-commit hooks not installed (core.hooksPath may be set)"

setup-hard: ## Clean install (remove caches)
	@rm -rf .venv uv.lock
	@make setup

format: ## Format all Python files
	@uv run ruff format $(PYTHON_FILES)

format-check: ## Check Python formatting
	@uv run ruff format --check $(PYTHON_FILES)

lint: ## Lint all Python files
	@uv run ruff check $(PYTHON_FILES)

lint-fix: ## Lint and auto-fix Python files
	@uv run ruff check --fix $(PYTHON_FILES)

types: ## Type check all Python files
	@uv run ty check

test: ## Run test suite
	@uv run pytest tests/

test-coverage: ## Run test suite with coverage
	@uv run pytest tests/ --cov=src/sirtuin --cov-report=term-missing

uv-lock: ## Lock dependencies
	@uv lock

uv-update: ## Update dependencies
	@uv lock --upgrade

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
