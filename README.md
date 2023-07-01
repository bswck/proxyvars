## ZeugVars

A simple & straight-forward Python module for creating context-dependent proxy objects.

## Short Description

_ZeugVars_ is a Python module for creating context-dependent proxy objects.

By 'proxy' we mean any object that forwards attribute access to another
object. By 'context-dependent' we mean that the object to which the proxy
forwards attribute access can change depending on the context in which the
proxy is used.

### Have you ever wondered how `flask.request` works?

How is it possible that [`flask.request`](https://tedboy.github.io/flask/interface_api.incoming_request_data.html?highlight=request#flask.request) is different for each request, despite being a global variable?

The answer is that `flask.request` is a proxy object: it forwards attribute
access to an object that is different for each request. With a little simplification,
the object to which `flask.request` forwards attribute access is stored
in a `werkzeug.local.LocalProxy` object. The functionality of `zeugvars.zeugvar()`
is roughly equivalent to `werkzeug.local.LocalProxy`. The `zeugvar` function
creates a proxy object that forwards attribute access to an object stored
in the provided manager, which could be any object that implements the
`Manager` protocol; for example, a `contextvars.ContextVar` object.

## Description

The `zeugvar` function takes a `Manager` object and class (optional) as arguments.
The `Manager` object must have `get` and `set` methods. The `get` method returns
the object to which the proxy forwards attribute access. The `set` method sets
the object to which the proxy forwards attribute access.  `set` is called when
the proxy is being inplace modified. The class is optional unless the `Manager`
is bound, i.e. `Manager.get` returns an instance of a class.
The user might provide custom `getter` and `setter` functions.
This might be useful when there is the need to keep track of the tokens
returned by `ContextVar.set()`, if using `ContextVar` as the manager.

## Example

The following example shows how to use `zeugvar` with `contextvars.ContextVar`:

```python
>>> from contextvars import ContextVar
>>> from zeugvars import zeugvar
...
>>> counter: ContextVar[int] = ContextVar("counter")
>>> count = zeugvar(counter, int)
...
>>> counter.set(0)
>>> count += 1
>>> count
1
>>> count -= 1
>>> count
0
>>> counter.set(1000)
<Token var=<ContextVar name='counter' at ...> at ...>
>>> count
1000
```