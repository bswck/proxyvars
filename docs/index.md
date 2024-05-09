
# <div align="center">proxyvars<br>[![skeleton](https://img.shields.io/badge/0.0.2rc–238–g68b0ab8-skeleton?label=%F0%9F%92%80%20bswck/skeleton&labelColor=black&color=grey&link=https%3A//github.com/bswck/skeleton)](https://github.com/bswck/skeleton/tree/0.0.2rc-238-g68b0ab8) [![Supported Python versions](https://img.shields.io/pypi/pyversions/proxyvars.svg?logo=python&label=Python)](https://pypi.org/project/proxyvars/) [![Package version](https://img.shields.io/pypi/v/proxyvars?label=PyPI)](https://pypi.org/project/proxyvars/)</div>

[![Tests](https://github.com/bswck/proxyvars/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/proxyvars/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/proxyvars.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/proxyvars)
[![Documentation Status](https://readthedocs.org/projects/proxyvars/badge/?version=latest)](https://proxyvars.readthedocs.io/en/latest/?badge=latest)
[![Lifted?](https://tidelift.com/badges/package/pypi/proxyvars)](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvars&utm_medium=readme)

Callback-based object proxies in Python.


# For Enterprise

| [![Tidelift](https://nedbatchelder.com/pix/Tidelift_Logo_small.png)](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvarsutm_medium=referral&utm_campaign=readme) | [Available as part of the Tidelift Subscription.](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvars&&utm_medium=referral&utm_campaign=readme)<br>This project and the maintainers of thousands of other packages are working with Tidelift to deliver one enterprise subscription that covers all of the open source you use. [Learn more here](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvars&utm_medium=referral&utm_campaign=readthedocs). |
| - | - |

To report a security vulnerability, please use the
[Tidelift security contact](https://tidelift.com/security).<br>
Tidelift will coordinate the fix and disclosure.

# Installation
You might simply install it with pip:

```shell
pip install proxyvars
```

If you use [Poetry](https://python-poetry.org/), then you might want to run:

```shell
poetry add proxyvars
```

## For Contributors
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
<!--
This section was generated from bswck/skeleton@0.0.2rc-238-g68b0ab8.
Instead of changing this particular file, you might want to alter the template:
https://github.com/bswck/skeleton/tree/0.0.2rc-238-g68b0ab8/fragments/readme.md
-->
!!! Note
    If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).
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
    pre-commit install
    ```

For more information on how to contribute, check out [CONTRIBUTING.md](https://github.com/bswck/proxyvars/blob/HEAD/CONTRIBUTING.md).<br/>
Always happy to accept contributions! ❤️

# Legal Info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).
<br />This software is licensed under the terms of [MIT License](https://github.com/bswck/proxyvars/blob/HEAD/LICENSE).
