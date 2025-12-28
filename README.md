<a href="https://merylldindin.com">
  <img src="https://cdn.merylldindin.com/github/sirtuin.webp" alt="sirtuin" width="100%">
</a>

<div align="center">
  <a href="https://github.com/merylldindin/sirtuin/graphs/contributors" target="_blank">
    <img src="https://img.shields.io/github/contributors/merylldindin/sirtuin.svg?style=for-the-badge" alt="contributors"/>
  </a>

  <a href="https://github.com/merylldindin/sirtuin/stargazers" target="_blank">
    <img src="https://img.shields.io/github/stars/merylldindin/sirtuin.svg?style=for-the-badge" alt="stars"/>
  </a>

  <a href="https://github.com/merylldindin/sirtuin/issues" target="_blank">
    <img src="https://img.shields.io/github/issues/merylldindin/sirtuin.svg?style=for-the-badge" alt="issues"/>
  </a>

  <a href="https://pypi.python.org/pypi/sirtuin" target="_blank">
    <img src="https://img.shields.io/pypi/v/sirtuin.svg?style=for-the-badge" alt="pypi version"/>
  </a>

  <a href="https://github.com/merylldindin/sirtuin/blob/master/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/merylldindin/sirtuin.svg?style=for-the-badge" alt="license"/>
  </a>
</div>

<div align="center">
  <p align="center">
    <h2>AWS CLI Routines</h2>
    <a href="https://github.com/merylldindin/sirtuin/issues">Report Bug</a>
  </p>
</div>

## About

Sirtuin is a collection of AWS CLI routines that automate common deployment tasks for CloudFront distributions and container services.

## Tech Stack

| Layer                | Technology                                        |
| -------------------- | ------------------------------------------------- |
| Language             | [Python 3.13](https://www.python.org/)            |
| Package Manager      | [uv](https://docs.astral.sh/uv/)                  |
| CLI Framework        | [Typer](https://typer.tiangolo.com/)              |
| Data Validation      | [Pydantic](https://docs.pydantic.dev/)            |
| Linting & Formatting | [Ruff](https://docs.astral.sh/ruff/)              |
| Type Checking        | [ty](https://docs.astral.sh/ty/)                  |
| Testing              | [Pytest](https://docs.pytest.org/)                |
| Cloud                | [AWS CLI](https://aws.amazon.com/cli/)            |

## Installation

```bash
pip install sirtuin
```

Or with uv:

```bash
uv add sirtuin
```

## Usage

### CloudFront Operations

Deploy a CloudFront distribution via a local configuration:

```bash
sirtuin cloudfront-deploy .cloudfront -p profile
```

Invalidate CloudFront cache:

```bash
sirtuin cloudfront-invalidate .cloudfront -p profile
```

Display Content Security Policy headers:

```bash
sirtuin cloudfront-headers .cloudfront
```

### Container Operations

Push an updated container to AWS via a stored configuration on S3:

```bash
sirtuin container-push s3://bucket/.container -p profile
```

Deploy a new container to AWS via a stored configuration on S3:

```bash
sirtuin container-deploy s3://bucket/.container -p profile
```

## Local Development

### Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with profiles

### Setup

```bash
git clone https://github.com/merylldindin/sirtuin
cd sirtuin
make setup
```

This installs all dependencies and configures pre-commit hooks.

### Available Commands

| Command              | Description                        |
| -------------------- | ---------------------------------- |
| `make setup`         | Install dependencies + hooks       |
| `make setup-hard`    | Clean install from scratch         |
| `make format`        | Format code with Ruff              |
| `make format-check`  | Check formatting (CI)              |
| `make lint`          | Lint code with Ruff                |
| `make lint-fix`      | Auto-fix linting issues            |
| `make types`         | Type check with ty                 |
| `make test`          | Run test suite                     |
| `make test-coverage` | Run tests with coverage            |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code quality standards
- Naming conventions
- Git workflow and conventional commits
- Pre-commit hooks

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.
