# <div align="center">proxyvars<br>[![skeleton](https://img.shields.io/badge/0.0.2rc–239–ga084376-skeleton?label=%F0%9F%92%80%20bswck/skeleton&labelColor=black&color=grey&link=https%3A//github.com/bswck/skeleton)](https://github.com/bswck/skeleton/tree/0.0.2rc-239-ga084376) [![Supported Python versions](https://img.shields.io/pypi/pyversions/proxyvars.svg?logo=python&label=Python)](https://pypi.org/project/proxyvars/) [![Package version](https://img.shields.io/pypi/v/proxyvars?label=PyPI)](https://pypi.org/project/proxyvars/)</div>

[![Tests](https://github.com/bswck/proxyvars/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/proxyvars/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/proxyvars.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/proxyvars)
[![Documentation Status](https://readthedocs.org/projects/proxyvars/badge/?version=latest)](https://proxyvars.readthedocs.io/en/latest/?badge=latest)
[![Lifted?](https://tidelift.com/badges/package/pypi/proxyvars)](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvars&utm_medium=readme)

Callback-based object proxies in Python.

# Example Usage
The library might have many use cases.

## Asynchronous Apps
Imagine a web app that processes many requests asynchronously.
A fun design we can learn from [contextvars](https://docs.python.org/3/library/contextvars.html#asyncio-support)
is that we can run request handlers in proper contexts with all the request-related data
held in context variables instead of requiring endpoint functions to accept parameters like `request`.
This approach heavily used in Flask, where one can access request data using a global proxy
[`flask.request`](https://flask.palletsprojects.com/en/3.0.x/api/#flask.request).
With bare contextvars, we could achieve this:

```py
from contextvars import ContextVar
from proxyvars import proxy
from asgi_framework import App  # some random ASGI web framework

class Request:
    args: dict[str, str]
    headers: dict[str, str]
    data: str
    # etc...

request_context: ContextVar[Request] = ContextVar("request_context")
app = App()

# the app will manage to set the appropriate Request object in the context
# before actually triggering the index() coroutine
@app.get("/")
async def echo():
    request: Request = request_context.get()
    # do something with request...
    return request.data
```

With proxyvars, we can skip the assignment and simply create a dynamic-lookup proxy:
```py
# below the Request class
request = lookup_proxy(request_context)

@app.get("/")
async def echo():
    return request.data  # request delegated attribute access to request_context.get()
```

## Flexible "Global" State
One of the crucial caveats of using global variables is reduction of modularity and flexibility.
Typically we want to test our code in an easily-parametrizable environment,
which becomes unobvious in case of some global state that other parts of your program
might depend on.
Problems arise in multi-threaded or asynchronous applications, where some global data typically
should be thread- or task-local. Python offers [threading.local](https://docs.python.org/3/library/threading.html#threading.local) and [contextvars](https://docs.python.org/3/library/contextvars.html) (respectively) for achieving these goals.

But sometimes global state is just the most convenient solution.
Imagine running an app with a core `App` class with a config read from a file.
We don't want to populate the configuration into attributes of the `App` instance
and rather store configuration data properly in a class named `Config`.

We can store `Config` instance as an attribute `config` of our main class `App`
that manages the whole application life cycle and then, everytime we need a config value,
we can request the app's `config` attribute. With a lot of codebase, you can find
this solution more and more tedious.

Creating a global `app_config` variable, not bound to an app, is not a good direction either though.
What if you want to 2 apps with distinct configurations? Will you modify the global `app_config` to the proper
`Config` object everytime?

### Get That "Global" Experience With Proxyvars!
Simply create a global context variable.

```py
app_config_var: ContextVar[Config] = ContextVar("app_config_var")
app_config: Config = lookup_proxy(app_config_var)
```

Now just run your tests in properly set-up [contexts](https://docs.python.org/3/library/contextvars.html)
with `app_config_var` holding objects local to every thread, task or just a custom copy of the current context.


## Mutable Immutables
Ever dreamt of thread-safe, mutable integers in Python?
I don't think anybody did, but it's possible with lookup proxies & beloved contextvars just in case.

```py
from contextvars import ContextVar
from proxyvars import proxy

my_iq_var = ContextVar("my_iq_var", 100)
my_iq = lookup_proxy(my_iq_var)

print(my_iq)  # 100

# Users of proxyvars typically have 200 IQ. Patch our current variable.
my_iq_var.set(200)

print(my_iq)  # 200

# Alright, let's be real. Assuming we have 200 IQ is a non-200 IQ behavior.
# Subtract 60 IQ points. We are entitled to 140 as programmers.
my_iq -= 60

print(my_iq_var.get())  # 140
print(my_iq)  # 60
```

This way, we got a mutable immutable. Or, more correctly, we got a proxy object
that can change its state which is represented by an immutable object.

Have fun with proxyvars!

# For Enterprise

| [![Tidelift](https://nedbatchelder.com/pix/Tidelift_Logo_small.png)](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvarsutm_medium=referral&utm_campaign=readme) | [Available as part of the Tidelift Subscription.](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvars&&utm_medium=referral&utm_campaign=readme)<br>This project and the maintainers of thousands of other packages are working with Tidelift to deliver one enterprise subscription that covers all of the open source you use. [Learn more here](https://tidelift.com/subscription/pkg/pypi-proxyvars?utm_source=pypi-proxyvars&utm_medium=referral&utm_campaign=github). |
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
This section was generated from bswck/skeleton@0.0.2rc-239-ga084376.
Instead of changing this particular file, you might want to alter the template:
https://github.com/bswck/skeleton/tree/0.0.2rc-239-ga084376/project/README.md.jinja
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
    pre-commit install
    ```

For more information on how to contribute, check out [CONTRIBUTING.md](https://github.com/bswck/proxyvars/blob/HEAD/CONTRIBUTING.md).<br/>
Always happy to accept contributions! ❤️

# Legal Info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).
<br />This software is licensed under the terms of [MIT License](https://github.com/bswck/proxyvars/blob/HEAD/LICENSE).
