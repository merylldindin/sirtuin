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

  <a href="https://github.com/merylldindin/sirtuin/blob/master/LICENSE.txt" target="_blank">
    <img src="https://img.shields.io/github/license/merylldindin/sirtuin.svg?style=for-the-badge" alt="license"/>
  </a>
</div>

<div align="center">
  <p align="center">
    <h2> AWS CLI Routines </h2>
    <a href="https://github.com/merylldindin/sirtuin/issues">
        Report Bug
    </a>
  </p>
</div>

## <summary>Table of Contents</summary>

<ol>
    <li><a href="#about-sirtuin">About Sirtuin</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#get-started">Get Started</a></li>
    <li><a href="#ide-recommendations">IDE Recommendations</a></li>
    <li><a href="#code-quality">Code quality</a></li>
    <li><a href="#git-conventions">Git Conventions</a></li>
</ol>

## About Sirtuin

Sirtuin is a collection of AWS CLI routines that can be used to automate some of the most common tasks. It is a work in progress and will be updated regularly.

## Built With

- [Python](https://www.python.org/)
- [Bash](https://www.gnu.org/software/bash/)
- [Typer](https://typer.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)

## Get Started

```bash
# install dev experience
make setup
# install dependencies
make install
```

### Installing `awscli`:

A fully documented tutorial is available [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), and is recommended to follow depending on your distribution.

Verify whether your installation worked by opening a new terminal:

```bash
meryll@xps:~/Venvs$ aws --version
aws-cli/2.7.27 Python/3.9.11 Linux/5.15.0-56-generic exe/x86_64.ubuntu.22 prompt/off
```

### Installing `awsebcli`:

A fully documented tutorial is available [here](https://github.com/aws/aws-elastic-beanstalk-cli-setup), and is recommended to follow depending on your distribution.

Verify whether your installation worked by opening a new terminal:

```bash
meryll@xps:~/Venvs$ eb --version
EB CLI 3.20.3 (Python 3.10.)
```

## IDE Recommendations

I recommend working with VSCode, an IDE that does not need to be presented. Internally, I use a set of code extensions enabling a minimum of code standardization, making the life of many developers more enjoyable. Those extensions are given in `.vscode/extensions.json`, and can be downloaded directly via the VSCode extension store. This goes hand and hand with properly configured VSCode workspace settings, available in `.vscode/settings.json`.

## Code Quality

### Husky:

Many of our internal toolings are enforced via [husky](https://typicode.github.io/husky/#/), a wrapper for Git hooks. I currently enforce two hooks:

- `commit-msg` relying on [commitlint](https://commitlint.js.org/) to make sure that our commit conventions are respected
- `pre-push` relying on a `yarn` command to run locally a majority of our CI scripts

Make sure you correctly initialized your hooks prior to starting:

```bash
yarn husky:setup
```

### Return Statements:

A comment that will come back often in PR reviews is the spacing in your code. The overall strategy is to split your code by functional blocks, aka adding empty lines to differentiate loops, if-statements or clusters of similar actions. There are also a few more guidelines:

1. Return statements should be isolated from any code blocks
2. Do not use spacing betIen a function name and the first line of code

An application of those guidelines is illustrated below:

```python
# do
def function():
  return object

# don't
def function():

  return object

# do
def function():
  object = get_object()

  return object

# don't
def function():
  object = get_object()
  return object
```

### Assert Statements:

The guidelines are the same for `assert` statements than they are for `return` statements.

### Prettier:

To maintain some minimal standards within our codebase, I rely on [prettier](https://prettier.io/) that is configured through `.prettierrc`. I use `.prettierignore` to avoid conflicts with some configuration files that would otherwise be broken by using prettier. Make sure prettier is correctly used in VSCode by installing the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode).

### Helpers:

I use Python 3.10 so make sure to install a clean venv environment depending on a 3.10.\* version. I rely on [poetry](https://python-poetry.org/) for environment management.

I use some pieces of software to help with code development, those are:

- [black](https://pypi.org/project/black/) configured in `pyproject.toml`
- [isort](https://pypi.org/project/isort/) configured in `pyproject.toml`
- [ruff](https://pypi.org/project/ruff/) configured in `pyproject.toml`

### Naming Conventions:

"There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

That is exactly why it is important everyone follow guidelines regarding naming conventions, especially when moving quickly as a team. Here are a set of rules that will most likely guide you through any problem you would face:

1. Do not use abbreviations
2. Use at least 2 words for function names
3. Boolean variables should be infered from their name (e.g. start with `is_` or `has_`)
4. Use `snake_case` for folder names, function names
5. Use `PascalCase` for class names
6. Use `SCREAMING_SNAKE_CASE` for constants
7. Use `_` prefix for private functions

### Typing:

Typing is key to maintainability. It will increase the readability of the code, but will also passively document your code. Finally, type checking will help to find some obvious bugs.

I rely on dynamic typing via [Pydantic](https://pydantic-docs.helpmanual.io/) and use static typing via VSCode for now. To enable static typing, ensure that you are using the VSCode extension [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance).

I will most likely move towards the introduction of [mypy](https://pydantic-docs.helpmanual.io/mypy_plugin/) in the future to manage our static typing.

## Git Conventions

### Branches:

I have a simple convention for branch naming: `{initials}/{descriptive-kebab-case}`. Keep them all loIrcase. For John Doe working on a feature A, that would be `jd/feature-a`.

### Commits:

The Conventional Commits specification is a lightIight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of. This convention dovetails with SemVer, by describing the features, fixes, and breaking changes made in commit messages. Learn more [here](https://www.conventionalcommits.org/en/v1.0.0/).

### Pull Requests:

There are simple rules in regards to our PR management:

- Link your PRs to their related Notion tickets;
- Use prefixes for your PR titles among [FIX], [FEAT], [REFACTOR], [RELEASE], [HOTFIX], [TEST];
- If your code affects the application build, be sure to update the `README.md`;
- Do not merge a PR until all comments are resolved;
- Remove your branch after merging;
