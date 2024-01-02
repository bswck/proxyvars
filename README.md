
# proxyvars [![skeleton](https://img.shields.io/badge/7935235-skeleton?label=%F0%9F%92%80%20bswck/skeleton&labelColor=black&color=grey&link=https%3A//github.com/bswck/skeleton)](https://github.com/bswck/skeleton/tree/7935235)
[![Package version](https://img.shields.io/pypi/v/proxyvars?label=PyPI)](https://pypi.org/project/proxyvars/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/proxyvars.svg?logo=python&label=Python)](https://pypi.org/project/proxyvars/)

[![Tests](https://github.com/bswck/proxyvars/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/proxyvars/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/proxyvars.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/proxyvars)
[![Documentation Status](https://readthedocs.org/projects/proxyvars/badge/?version=latest)](https://proxyvars.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/github/license/bswck/proxyvars.svg?label=License)](https://github.com/bswck/proxyvars/blob/HEAD/LICENSE)

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A simple and straight-forward Python module for creating context-dependent proxy objects.

As for now, the documentation is mostly in the codebase (check relevant docstrings of `proxy()`, `const_proxy()`, `lookup_proxy()`, `proxy_field_accessor()`, `proxy_item_accessor()` and `proxy_attribute_accessor()` for more information).

# Installation



You might simply install it with pip:

```shell
pip install proxyvars
```

If you use [Poetry](https://python-poetry.org/), then run:

```shell
poetry add proxyvars
```

## For contributors

<!--
This section was generated from bswck/skeleton@7935235.
Instead of changing this particular file, you might want to alter the template:
https://github.com/bswck/skeleton/tree/7935235/project/README.md.jinja
-->

> [!Note]
> If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).



1.  Fork the [proxyvars repository](https://github.com/bswck/proxyvars) on GitHub.

1.  [Install Poetry](https://python-poetry.org/docs/#installation).<br/>
    Poetry is an amazing tool for managing dependencies & virtual environments, building packages and publishing them.
    You might use [pipx](https://github.com/pypa/pipx#readme) to install it globally (recommended):

    ```shell
    pipx install poetry
    ```

    <sub>If you encounter any problems, refer to [the official documentation](https://python-poetry.org/docs/#installation) for the most up-to-date installation instructions.</sub>

    Be sure to have Python 3.8 installed—if you use [pyenv](https://github.com/pyenv/pyenv#readme), simply run:

    ```shell
    pyenv install 3.8
    ```

1.  Clone your fork locally and install dependencies.

    ```shell
    git clone https://github.com/your-username/proxyvars path/to/proxyvars
    cd path/to/proxyvars
    poetry env use $(cat .python-version)
    poetry install
    ```

    Next up, simply activate the virtual environment and install pre-commit hooks:

    ```shell
    poetry shell
    pre-commit install --hook-type pre-commit --hook-type pre-push
    ```

For more information on how to contribute, check out [CONTRIBUTING.md](https://github.com/bswck/proxyvars/blob/HEAD/CONTRIBUTING.md).<br/>
Always happy to accept contributions! ❤️


# Legal info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).
<br />This software is licensed under the terms of [MIT License](https://github.com/bswck/proxyvars/blob/HEAD/LICENSE).
