"""
ZeugVars
~~~~~~~~
A simple & straight-forward Python module for creating context-dependent proxy objects.

(C) bswck, 2023

What is this?
-------------
`zeugvars` is a Python module for creating context-dependent proxy objects.

By 'proxy' we mean any object that forwards attribute access to another
object.  By 'context-dependent' we mean that the object to which the proxy
forwards attribute access can change depending on the context in which the
proxy is used.

Have you ever wondered how `flask.request` works?
------------------------------------------------
How is it possible that `flask.request` is different for each request, despite
being a global variable?

The answer is that `flask.request` is a proxy object: it forwards attribute
access to an object that is different for each request. With a little simplification,
the object to which `flask.request` forwards attribute access is stored
in a `werkzeug.local.LocalProxy` object. The functionality of `zeugvars.zeugvar()`
is roughly equivalent to `werkzeug.local.LocalProxy`. The `zeugvar` function
creates a proxy object that forwards attribute access to an object stored
in the provided manager, which could be any object that implements the
`Manager` protocol; for example, a `contextvars.ContextVar` object.

Description
-----------
The `zeugvar` function takes a `Manager` object and class (optional) as arguments.
The `Manager` object must have `get` and `set` methods.  The `get` method returns
the object to which the proxy forwards attribute access.  The `set` method sets
the object to which the proxy forwards attribute access.  `set` is called when
the proxy is being inplace modified.  The class is optional unless the `Manager`
is bound, i.e. `Manager.get` returns an instance of a class.
The user might provide custom `getter` and `setter` functions.
This might be useful when there is the need to keep track of the tokens
returned by `ContextVar.set()`, if using `ContextVar` as the manager.

Example
-------
The following example shows how to use `zeugvar` with `contextvars.ContextVar`:

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
"""

import contextlib
import functools
from collections.abc import Callable
from typing import TypeVar, Any, cast, Protocol, runtime_checkable

_T = TypeVar("_T")


@runtime_checkable
class Manager(Protocol[_T]):
    def get(self) -> _T:
        ...

    def set(self, value: _T) -> Any:
        ...


def zeugvar_descriptor(
    cls: type[_T],
    mgr: Manager[_T],
    getter: Callable[[Manager[_T]], _T],
    setter: Callable[[Manager[_T], _T], None],
    *,
    undefined: Callable[..., Any] | None = None,
    fallback: Callable[..., Any] | None = None,
    custom_mro: bool = False,
    inplace: bool = False,
) -> Any:
    """Descriptor factory for zeugvars.zeugvar() proxies."""

    class _ZeugVarDescriptor:
        attr_name: str

        def __init__(self) -> None:
            self.attr_name = None  # type: ignore[assignment]

        def __set_name__(self, owner: type[_T], name: str) -> None:
            self.attr_name = name

        def __get__(self, instance: _T, owner: type[_T] | None) -> Any:
            if self.attr_name == "__getattr__":

                def attribute(name: str) -> Any:
                    return getattr(getter(mgr), name)

            elif self.attr_name in ("__repr__", "__str__"):
                with contextlib.suppress(RuntimeError):
                    return getattr(getter(mgr), self.attr_name)

                def attribute() -> str:  # type: ignore[misc]
                    return f"<unbound {cls.__name__!r} object>"

            else:
                try:
                    obj = getter(mgr)
                except RuntimeError:
                    if self.attr_name == "__dir__" and not custom_mro:

                        def attribute() -> list[str]:  # type: ignore[misc]
                            return list(set(dir(cls)) - {"mro"})

                    elif callable(undefined):
                        attribute = undefined

                    else:
                        raise
                else:
                    try:
                        attribute = getattr(obj, self.attr_name)
                    except AttributeError:
                        if not callable(fallback):
                            raise

                        attribute = functools.partial(fallback, obj)

            if inplace:
                def _apply_inplace(*args: Any, **kwargs: Any) -> _T:
                    ret = attribute(*args, **kwargs)
                    setter(mgr, ret)
                    return instance

                return _apply_inplace
            return attribute

        def __set__(self, instance: _T, value: Any) -> None:
            setattr(getter(mgr), self.attr_name, value)

        def __delete__(self, instance: _T) -> None:
            delattr(getter(mgr), self.attr_name)

    return _ZeugVarDescriptor()


def _op_fallback(op_name: str) -> Callable[[Any, Any], Any]:
    return lambda obj, op: getattr(obj, op_name)(op)


def _cv_getter(mgr: Manager[_T]) -> _T:
    try:
        obj = mgr.get()
    except LookupError:
        raise RuntimeError("No object in context") from None
    return obj


def _cv_setter(mgr: Manager[_T], value: _T) -> None:
    mgr.set(value)


def zeugvar(
    mgr: Manager[_T],
    cls: type[_T] = None,  # type: ignore[assignment]
    getter: Callable[[Manager[_T]], _T] = None,  # type: ignore[assignment]
    setter: Callable[[Manager[_T], _T], None] = None,  # type: ignore[assignment]
) -> _T:
    """See `zeugvars` module docstring for usage and example."""

    if getter is None:
        getter = _cv_getter

    if setter is None:
        setter = _cv_setter

    if cls is None:
        cls = type(getter(mgr))

    mro: Callable[[], tuple[type[Any], ...]] = object.__getattribute__(cls, "mro")
    custom_mro = not hasattr(mro, "__self__")
    descriptor = functools.partial(
        zeugvar_descriptor, cls, mgr, getter, setter, custom_mro=custom_mro
    )

    class _ZeugVarMeta(type):
        __doc__ = descriptor()
        __wrapped__ = descriptor()
        __repr__ = descriptor()
        __str__ = descriptor()
        __bytes__ = descriptor()
        __format__ = descriptor()
        __lt__ = descriptor()
        __le__ = descriptor()
        __eq__ = descriptor()
        __ne__ = descriptor()
        __gt__ = descriptor()
        __ge__ = descriptor()
        __hash__ = descriptor()
        __bool__ = descriptor(undefined=lambda: False)
        __getattr__ = descriptor()
        __setattr__ = descriptor()
        __delattr__ = descriptor()
        __dir__ = descriptor(undefined=lambda: dir(cls))
        __class__ = descriptor(undefined=lambda: cls)
        __instancecheck__ = descriptor()
        __subclasscheck__ = descriptor()
        __call__ = descriptor()
        __len__ = descriptor()
        __length_hint__ = descriptor()
        __getitem__ = descriptor()
        __setitem__ = descriptor()
        __delitem__ = descriptor()
        __iter__ = descriptor()
        __next__ = descriptor()
        __reversed__ = descriptor()
        __contains__ = descriptor()
        __add__ = descriptor()
        __sub__ = descriptor()
        __mul__ = descriptor()
        __matmul__ = descriptor()
        __truediv__ = descriptor()
        __floordiv__ = descriptor()
        __mod__ = descriptor()
        __divmod__ = descriptor()
        __pow__ = descriptor()
        __lshift__ = descriptor()
        __rshift__ = descriptor()
        __and__ = descriptor()
        __xor__ = descriptor()
        __or__ = descriptor()
        __radd__ = descriptor()
        __rsub__ = descriptor()
        __rmul__ = descriptor()
        __rmatmul__ = descriptor()
        __rtruediv__ = descriptor()
        __rfloordiv__ = descriptor()
        __rmod__ = descriptor()
        __rdivmod__ = descriptor()
        __rpow__ = descriptor()
        __rlshift__ = descriptor()
        __rrshift__ = descriptor()
        __rand__ = descriptor()
        __rxor__ = descriptor()
        __ror__ = descriptor()
        __iadd__ = descriptor(fallback=_op_fallback("__add__"), inplace=True)
        __isub__ = descriptor(fallback=_op_fallback("__sub__"), inplace=True)
        __imul__ = descriptor(fallback=_op_fallback("__mul__"), inplace=True)
        __imatmul__ = descriptor(fallback=_op_fallback("__matmul__"), inplace=True)
        __itruediv__ = descriptor(fallback=_op_fallback("__truediv__"), inplace=True)
        __ifloordiv__ = descriptor(fallback=_op_fallback("__floordiv__"), inplace=True)
        __imod__ = descriptor(fallback=_op_fallback("__mod__"), inplace=True)
        __ipow__ = descriptor(fallback=_op_fallback("__pow__"), inplace=True)
        __ilshift__ = descriptor(fallback=_op_fallback("__lshift_"), inplace=True)
        __irshift__ = descriptor(fallback=_op_fallback("__rshift__"), inplace=True)
        __iand__ = descriptor(fallback=_op_fallback("__and__"), inplace=True)
        __ixor__ = descriptor(fallback=_op_fallback("__xor__"), inplace=True)
        __ior__ = descriptor(fallback=_op_fallback("__or__"), inplace=True)
        __neg__ = descriptor()
        __pos__ = descriptor()
        __abs__ = descriptor()
        __invert__ = descriptor()
        __complex__ = descriptor()
        __int__ = descriptor()
        __float__ = descriptor()
        __index__ = descriptor()
        __round__ = descriptor()
        __trunc__ = descriptor()
        __floor__ = descriptor()
        __ceil__ = descriptor()
        __enter__ = descriptor()
        __exit__ = descriptor()
        __await__ = descriptor()
        __aiter__ = descriptor()
        __anext__ = descriptor()
        __aenter__ = descriptor()
        __aexit__ = descriptor()
        __copy__ = descriptor()
        __deepcopy__ = descriptor()

    zv = cast(_T, _ZeugVarMeta(cls.__name__, (), {}))
    if not custom_mro:

        def _mro_wrapper() -> tuple[type[Any], ...]:
            try:
                getter(mgr)
            except RuntimeError:
                return mro()
            else:
                raise AttributeError(
                    f"{cls.__name__!r} object has no attribute 'mro'"
                ) from None

        type.__setattr__(zv, "mro", _mro_wrapper)
    return zv
