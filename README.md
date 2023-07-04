## `zeugvars`

A simple & straight-forward Python module for creating type-safe, context-dependent proxy objects.

## Example

The following example shows how to use `zeugvar` with `contextvars.ContextVar`:

```python
>>> from contextvars import ContextVar
>>> from zeugvars import proxy
...
>>> count_var = ContextVar("count_var")
>>> count = proxy(counter, int)
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

`zeugvars` is a Python module for creating context-dependent proxy objects.

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

The functionality of `zeugvars.zeugvar()` (or, as you prefer, `zeugvars.proxy()`) is a more generic version of `werkzeug.local.LocalProxy`.

It takes a `Manager` object and the class of the object to which the proxy points.

The `Manager` object must have `get` and `set` methods. The `get` method returns
the object to which the would forward attribute access. The `set` method sets it, obviously.
`set` is called when the proxy is being inplace modified, for example within the `+=` reassigning operator.
The class parameter is optional, but it is strongly recommended for some corner-cases.
The user might provide custom `getter` and `setter` functions that change the way 
`Manager.get()` and `Manage.set()` are called.
This might be useful when there is the need to keep track of the tokens
returned by `ContextVar.set()`, if using `ContextVar` as the manager.

## When would you use `zeugvars`?

You could use `zeugvars` when...
* ...writing a thread-safe application that operates on fixed resource that are different per thread.
* ...improving code readability by avoiding passing around the same object to every function.
* ...writing a web application that operates on fixed resources per request.
* ...writing an asynchronous application that operates on fixed resources between tasks.
* ...having any other case where you could use global variables that are context-dependent!

## Why does it have such a weird name?

The name is a reference to the pallets' `werkzeug` library, which is a German word for 'tool'.
'zeug' is a German word for 'stuff' or 'things'. 'vars' is an abbreviation for 'variables'.
I think now you can see where the name comes from.

## Installation

### pip
```bash
$ pip install zeugvars
```

### poetry

You can add `zeugvars` as a dependency with the following command:

```bash
$ poetry add zeugvars
```

Or by directly specifying it in the configuration like so:

```toml
[tool.poetry.dependencies]
"zeugvars" = "^0.2.0"
```

Alternatively, you can add it directly from the source:

```toml
[tool.poetry.dependencies.zeugvars]
git = "https://github.com/bswck/zeugvars.git"
```

## Documentation

### `zeugvars.zeugvar(mgr, cls=None, getter=None, setter=None)`

Creates a context-dependent proxy object.

#### Parameters
* `manager`: Manager object. Must implement the `Manager` protocol. Matches `contextvars.ContextVar`.
* `cls`: The class of the underlying variable accessed within the manager. Optional.
* `getter`: A function that returns the underlying variable from the manager. Optional.
* `setter`: A function that sets the underlying variable within the manager. Optional.
