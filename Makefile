PYTHON_FILES = `(find . -iname "*.py" -not -path "./.venv/*")`
TOML_FILES = `(find . -iname "*.toml" -not -path "./.venv/*")`

install: ## Install monorepo dependencies
	poetry install --sync

install-extra: ## Install monorepo dependencies and developer dependencies
	make install && yarn install --silent --ignore-optional

poetry-update: ## Upgrade poetry and dependencies
	poetry self update
	poetry run pip install --upgrade pip wheel setuptools
	poetry update

toml-sort: ## Sort pyproject.toml
	poetry run toml-sort --all --in-place $(TOML_FILES)

black: ## Run Black
	poetry run black --check

black-fix: ## Run Black with automated fix
	poetry run black $(PYTHON_FILES)

isort: ## Run Isort
	poetry run isort --check-only $(PYTHON_FILES)

isort-fix: ## Run Isort with automated fix
	poetry run isort $(PYTHON_FILES)

mypy: ## Run Mypy
	poetry run mypy $(PYTHON_FILES)

ruff: ## Run Ruff
	poetry run ruff $(PYTHON_FILES)

ruff-fix: ## Run Ruff
	poetry run ruff --fix $(PYTHON_FILES)

pytest: ## Run Pytest
	poetry run pytest tests/

pytest-coverage: ## Run coverage report
	poetry run coverage run -m pytest tests/
	poetry run coverage report

help: ## Description of the Makefile commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
