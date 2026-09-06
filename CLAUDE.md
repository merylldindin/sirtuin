# Sirtuin

AWS deployment CLI for CloudFront distributions and Elastic Container Service. Published to PyPI as `sirtuin`; installing it puts a `sirtuin` console script on the path.

## Stack

Python is pinned to `==3.13.*` — an exact pin, not a floor, so `uv sync` refuses any other interpreter. uv for packaging, Typer for the CLI, Pydantic for config parsing, Ruff for lint and format, `ty` for type checking, Pytest for tests, GitHub Actions for CI.

Sirtuin drives the **AWS CLI v2 and Docker as subprocesses**. There is no boto3 and no AWS SDK. AWS CLI v2 must be installed and its profiles configured for anything but the tests to work.

`rich.progress` is imported by `utils/decorators.py` but `rich` is not a declared dependency — it arrives transitively through Typer. Treat that as a latent break, not a licence to add more undeclared imports.

## Architecture

`src/sirtuin/` is a Typer entry point over three layers:

- `main.py` — the five commands, one thin function each, delegating straight to a controller
- `controllers/` — one module per surface (`aws_cloudfront`, `aws_container`, `http_headers`)
- `models/` — Pydantic models for the config file and AWS enums; nothing here touches AWS
- `utils/` — loaders, dumpers, cleaners, filepaths, decorators, constants

Two conventions in `utils/decorators.py` govern how a controller is written, and both are invisible from a call site:

- A function wrapped in `@run_command` **returns a shell command string**; the decorator executes it with `subprocess.Popen(shell=True)`. Write the string, never call the process yourself. Under pytest the decorator short-circuits and returns the string unexecuted, which is what every controller test asserts against — so a controller test checks the command that would run, not an AWS effect.
- `@catch_remote_config` accepts an `s3://` URI in place of a path: it downloads the object to `.sirtuin.cfg` in the working directory, runs the command, and deletes it. That is why container commands take an S3 URI and CloudFront commands take a local path.

Every command takes a config file rather than flags. The default filename is `.sirtuin.cfg`, TOML, defined as `DEFAULT_SIRTUIN_CONFIG_NAME` in `utils/constants.py`.

## Public API

The CLI is the public surface, so semver tracks it: renaming a command, dropping an option, or changing a config-file key is a breaking change. The importable modules carry no compatibility promise.

| Command                         | Purpose                                 |
| ------------------------------- | --------------------------------------- |
| `sirtuin cloudfront-deploy`     | Deploy a CloudFront distribution        |
| `sirtuin cloudfront-headers`    | Print Content Security Policy headers   |
| `sirtuin cloudfront-invalidate` | Invalidate a CloudFront cache           |
| `sirtuin container-deploy`      | Deploy a new container to ECS           |
| `sirtuin container-push`        | Push an updated container to ECR        |

All five accept `--profile/-p` and `--verbose/-v`. Verbose streams subprocess output instead of showing a spinner.

## Commands

| Command              | Purpose                                 |
| -------------------- | --------------------------------------- |
| `make setup`         | Install dependencies + pre-commit hooks |
| `make setup-hard`    | Clean install from scratch              |
| `make format`        | Check formatting                        |
| `make format-fix`    | Format with Ruff                        |
| `make lint`          | Lint with Ruff                          |
| `make lint-fix`      | Lint and auto-fix                       |
| `make types`         | Type check with ty                      |
| `make test`          | Run the test suite                      |
| `make test-coverage` | Run tests with a coverage report        |
| `make uv-lock`       | Lock dependencies                       |
| `make uv-update`     | Upgrade the lockfile                    |

There is no `check` aggregate. `make format lint types test` is the full local gate, and it matches CI exactly.

## Gates

`make setup` installs the pre-commit hooks. They run on every commit: trailing whitespace, end-of-file, YAML and TOML syntax, `ruff format`, `ruff check --fix`, and commitizen on the message — so every commit must be a Conventional Commit.

CI runs on `pull_request` and `merge_group`, and runs the same four make targets.

Ruff selects only `E`, `F`, `I001`, `W`. Annotation, naming and docstring rules are **not enforced by any tool here**, so what `CONTRIBUTING.md` states about typing and naming is convention a reviewer checks, not a gate. One convention it does not state: no inline comments and no docstrings — names carry the meaning, and a comment is a second source of truth nothing verifies.

## Release

The version lives in `[project] version` of `pyproject.toml`, and that field is the only one the release reads.

Publishing is manual and never happens on merge. Run the `PyPI Release` workflow with a semantic version; it rewrites that field, pushes the bump directly to `main`, cuts the GitHub release, builds, publishes to PyPI, and opens a pull request from `gh/release-<version>`.

## Dependencies

Every dependency is pinned to an exact version. Renovate auto-merges minor and patch updates after 7 days, major updates to dev dependencies after 14, and security updates immediately.
