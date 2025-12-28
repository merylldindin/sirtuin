# Sirtuin

AWS CLI routines library for Python projects.

## Tech Stack

| Layer                | Technology     |
| -------------------- | -------------- |
| Language             | Python 3.13    |
| Package Manager      | uv             |
| Linting & Formatting | Ruff           |
| Type Checking        | ty             |
| Testing              | Pytest         |
| CI/CD                | GitHub Actions |

## Prerequisites

- Python 3.13
- uv (Astral package manager)
- AWS CLI v2 (configured with profiles)

## Quick Start

```bash
git clone https://github.com/merylldindin/sirtuin
cd sirtuin
make setup
```

## Project Structure

```
sirtuin/
├── src/sirtuin/           # Main package
│   ├── main.py            # CLI entry point (Typer)
│   ├── controllers/       # AWS operation handlers
│   │   ├── aws_cloudfront.py
│   │   ├── aws_container.py
│   │   └── http_headers.py
│   ├── models/            # Pydantic data models
│   │   ├── base_models.py
│   │   ├── aws_regions.py
│   │   ├── aws_container.py
│   │   ├── aws_cloudfront.py
│   │   ├── aws_instances.py
│   │   └── http_headers.py
│   └── utils/             # Utility functions
│       ├── constants.py
│       ├── loaders.py
│       ├── cleaners.py
│       ├── dumpers.py
│       ├── filepaths.py
│       └── decorators.py
├── tests/                 # Pytest test suite
│   ├── conftest.py
│   ├── controllers/
│   └── fixtures/
├── pyproject.toml         # uv configuration
├── .pre-commit-config.yaml
├── Makefile
└── renovate.json
```

## Commands

| Command              | Purpose                                 |
| -------------------- | --------------------------------------- |
| `make setup`         | Install dependencies + pre-commit hooks |
| `make setup-hard`    | Clean install from scratch              |
| `make format`        | Format code with Ruff                   |
| `make format-check`  | Check formatting (CI)                   |
| `make lint`          | Lint code with Ruff                     |
| `make lint-fix`      | Auto-fix linting issues                 |
| `make types`         | Type check with ty                      |
| `make test`          | Run test suite                          |
| `make test-coverage` | Run tests with coverage                 |
| `make uv-lock`       | Lock dependencies                       |
| `make uv-update`     | Update dependencies                     |

## CLI Commands

| Command                         | Purpose                                 |
| ------------------------------- | --------------------------------------- |
| `sirtuin container-push`        | Push updated container to AWS           |
| `sirtuin container-deploy`      | Deploy new container to AWS             |
| `sirtuin cloudfront-deploy`     | Deploy CloudFront distribution          |
| `sirtuin cloudfront-invalidate` | Invalidate CloudFront cache             |
| `sirtuin cloudfront-headers`    | Display Content Security Policy headers |

## Code Conventions

- Line length: 88 characters
- Type hints required on all functions
- Conventional commits enforced via pre-commit
- Branch naming: `{initials}/{descriptive-kebab-case}`
- Naming:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `SCREAMING_SNAKE_CASE` for constants

## CI/CD

- **Continuous Integration**: Runs on PR/merge_group
  - Ruff format check
  - Ruff lint
  - ty type check
  - Pytest test suite
- **PyPI Release**: Manual trigger with semantic version

## Dependencies

All dependencies pinned to exact versions. Renovate handles updates automatically:

- Minor/patch updates: Auto-merged after 7 days
- Major updates (dev deps): Auto-merged after 14 days
- Security updates: Immediate

## Key Files

| File                                           | Purpose                                     |
| ---------------------------------------------- | ------------------------------------------- |
| `pyproject.toml`                               | Project config, dependencies, tool settings |
| `.pre-commit-config.yaml`                      | Pre-commit hooks configuration              |
| `Makefile`                                     | Development commands                        |
| `renovate.json`                                | Dependency update automation                |
| `.github/workflows/continuous-integration.yml` | CI workflow                                 |
| `.github/workflows/pypi-release.yml`           | PyPI release workflow                       |
