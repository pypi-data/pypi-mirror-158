
![PyPI](https://img.shields.io/pypi/v/token-auth-cli)
![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/0djentd/token-auth-cli?include_prereleases)
![GitHub all releases](https://img.shields.io/github/downloads/0djentd/token-auth-cli/total)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/token-auth-cli)

![GitHub issues](https://img.shields.io/github/issues/0djentd/token-auth-cli)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/0djentd/token-auth-cli)
![GitHub Repo stars](https://img.shields.io/github/stars/0djentd/token-auth-cli?style=social)

[![Python package](https://github.com/0djentd/token-auth-cli/actions/workflows/python-package.yml/badge.svg)](https://github.com/0djentd/token-auth-cli/actions/workflows/python-package.yml)
[![Pylint](https://github.com/0djentd/token-auth-cli/actions/workflows/pylint.yml/badge.svg)](https://github.com/0djentd/token-auth-cli/actions/workflows/pylint.yml)

# token-auth-cli
## Description
Simple tool for testing token authentication during development.

## Installation
```
pip install token-auth-cli
```
or
```
git clone https://github.com/0djentd/token-auth-cli.git
cd token-auth-cli
python -m pip install .
```

## How to use
```
Usage: token-auth-cli [OPTIONS] COMMAND [ARGS]...

  token-auth-cli

  Simple tool for testing token authentication during development.

Options:
  --verbose / --no-verbose    Show additional information
  --debug / --no-debug        Show debug information
  --confirm-settings BOOLEAN  Confirm settings before trying to get token.
  --show-settings BOOLEAN     Show settings before trying to get token.
  --api TEXT                  API url.
  --api-get-token TEXT        API url to use when trying to get token.
  --api-get TEXT              API url to check if token valid.
  --config FILE               Config file.
  --store BOOLEAN             Store users/tokens.
  --help                      Show this message and exit.

Commands:
  init     Create config file and users/tokens storage.
  list     List stored users/tokens.
  login    Get token and store it.
  relogin  Try to use stored token for authentication.
  remove   Remove stored user/token.
```
