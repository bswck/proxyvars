# proxyvars [![Package version](https://img.shields.io/pypi/v/proxyvars?label=PyPI)](https://pypi.org/project/proxyvars) [![Supported Python versions](https://img.shields.io/pypi/pyversions/proxyvars.svg?logo=python&label=Python)](https://pypi.org/project/proxyvars)
[![Tests](https://github.com/bswck/proxyvars/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/proxyvars/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/proxyvars.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/proxyvars)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?label=Code%20style)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/bswck/proxyvars.svg?label=License)](https://github.com/bswck/proxyvars/blob/HEAD/LICENSE)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A simple and straight-forward Python module for creating context-dependent proxy objects.

As for now, the documentation is mostly in the codebase (check relevant docstrings of `proxy()`, `const_proxy()`, `lookup_proxy()`, `proxy_field_accessor()`, `proxy_item_accessor()` and `proxy_attribute_accessor()` for more information).

# Installation
If you want to…


## …use this tool in your project 💻
You might simply install it with pip:

    pip install proxyvars

If you use [Poetry](https://python-poetry.org/), then run:

    poetry add proxyvars

## …contribute to [proxyvars](https://github.com/bswck/proxyvars) 🚀

Happy to accept contributions!

> [!Note]
> If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).

First, [install Poetry](https://python-poetry.org/docs/#installation).<br/>
Poetry is an amazing tool for managing dependencies & virtual environments, building packages and publishing them.

    pipx install poetry

<sub>If you encounter any problems, refer to [the official documentation](https://python-poetry.org/docs/#installation) for the most up-to-date installation instructions.</sub>

Be sure to have Python 3.8 installed—if you use [pyenv](https://github.com/pyenv/pyenv#readme), simply run:

    pyenv install 3.8

Then, run:

    git clone https://github.com/bswck/proxyvars path/to/proxyvars
    cd path/to/proxyvars
    poetry env use $(cat .python-version)
    poetry install
    poetry shell
    pre-commit install --hook-type pre-commit --hook-type pre-push


# Legal info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).<br />This software is licensed under the [MIT License](https://github.com/bswck/proxyvars/blob/main/LICENSE).

