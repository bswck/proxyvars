## `commonvars`

A simple & straight-forward Python library for creating type-safe, context-dependent proxy objects.

## Example

The following example shows how to use `commonvars` with `contextvars`:

```python
>>> from contextvars import ContextVar
>>> from commonvars import commonvar
...
>>> count_var = ContextVar("count_var")
>>> count = commonvar(counter, int)
...
>>> count
<unbound 'int' object>
>>> count_var.set(0)
>>> count
0
>>> count += 1
>>> count
1
>>> count_var.get()
1
>>> count -= 1
>>> count
0
>>> count_var.set(1000)
<Token var=<ContextVar name='count_var' at ...> at ...>
>>> count
1000
```

## Ok, but what is this?

`commonvars` is a Python module for creating context-dependent proxy objects.

By 'proxy' we mean any object that forwards attribute access to another
object. By 'context-dependent' we mean that the object to which the proxy
forwards attribute access can change depending on the context in which the
proxy is used.

### Have you ever wondered how `flask.request` works?

How is it possible
that [`flask.request`](https://tedboy.github.io/flask/interface_api.incoming_request_data.html?highlight=request#flask.request)
is different for each request, despite being a global variable?

The answer is that `flask.request` is a such a proxy object as an instance of `werkzeug.local.LocalProxy`.
For every request, `flask.request` forwards attribute access to a different `flask.Request` object.

The functionality of `commonvars.commonvar()` (or, as you prefer, `commonvars.proxy()`) is a more generic version of `werkzeug.local.LocalProxy`.

It takes a `Manager` object and the class of the object to which the proxy points.

The `Manager` object must have `get` and `set` methods. The `get` method returns
the object to which the would forward attribute access. The `set` method sets it, obviously.
`set` is called when the proxy is being inplace modified, for example within the `+=` reassigning operator.
The class parameter is optional, but it is strongly recommended for some corner-cases.
The user might provide custom `getter` and `setter` functions that change the way 
`Manager.get()` and `Manage.set()` are called.
This might be useful when there is the need to keep track of the tokens
returned by `ContextVar.set()`, if using `ContextVar` as the manager.

## When would you use `commonvars`?

You could use `commonvars` when...
* ...writing a thread-safe application that operates on resources specific for separate threads.
* ...improving code readability by avoiding passing around the same object to every function.
* ...writing a web application that operates on resources specific per request.
* ...writing an asynchronous application that operates on resources specific between tasks.
* ...having any other case where you could use common variables that are context-dependent!

## Installation

### pip
```bash
$ pip install commonvars
```

### poetry

You can add `commonvars` as a dependency with the following command:

```bash
$ poetry add commonvars
```

Or by directly specifying it in the configuration like so:

```toml
[tool.poetry.dependencies]
"commonvars" = "^0.2.0"
```

Alternatively, you can add it directly from the source:

```toml
[tool.poetry.dependencies.commonvars]
git = "https://github.com/bswck/commonvars.git"
```

## Documentation

### `commonvars.commonvar(mgr, cls=None, getter=None, setter=None)`

Creates a context-dependent proxy object.

#### Parameters
* `manager`: Manager object. Must implement the `Manager` protocol. Matches `contextvars.ContextVar`.
* `cls`: The class of the underlying variable accessed within the manager. Optional.
* `getter`: A function that returns the underlying variable from the manager. Optional.
* `setter`: A function that sets the underlying variable within the manager. Optional.
