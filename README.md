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
  </a></div>

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

Sirtuin is a collection of AWS CLI routines that can be used to automate some of the most common tasks. It is a work in progress.

## Built With

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Typer](https://typer.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [AWS CLI](https://aws.amazon.com/cli/)

## Get Started

```bash
pip install sirtuin
# or with poetry
poetry add sirtuin
```

### How To Use

Deploy a cloudfront distribution via a local configuration:

```bash
poetry run sirtuin cloudfront-deploy .cloudfront -p profile
```

Push an updated container to AWS via a stored configuration on S3:

```bash
poetry run sirtuin container-push s3://bucket/.container -p profile
```

Deploy a new container to AWS via a stored configuration on S3:

```bash
poetry run sirtuin container-deploy s3://bucket/.container -p profile
```

### Local Installation

```bash
git clone https://github.com/merylldindin/sirtuin
# install dependencies
make install
```

**Installing `awscli`:** A fully documented tutorial is available [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), and is recommended to follow depending on your distribution. Verify whether your installation worked by opening a new terminal:

```bash
meryll@xps:~/Venvs$ aws --version
aws-cli/2.15.23 Python/3.11.6 Darwin/23.5.0 exe/x86_64 prompt/off
```
