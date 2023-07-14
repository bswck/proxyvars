"""`commonvars`.

A simple & straight-forward Python library for creating common variables
(context-dependent proxy objects).

(C) bswck, 2023
"""
import operator
from collections.abc import Callable
from contextlib import suppress
from functools import partial
from typing import Any, Protocol, TypeVar, cast, runtime_checkable

__all__ = ("commonvar", "proxy")

_T = TypeVar("_T")


@runtime_checkable
class Manager(Protocol[_T]):
    """Protocol for commonvars managers.

    Matches `contextvars.ContextVar`.
    """

    def get(self) -> _T:
        """Get the current value of the manager.

        Raises
        ------
        LookupError
            If no object is bound to the manager.
        """

    def set(self, value: _T) -> Any:
        """Set the current value of the manager."""


def commonvar_descriptor(
    cls: type[_T] | None,
    mgr: Manager[_T],
    getter: Callable[[Manager[_T]], _T],
    setter: Callable[[Manager[_T], _T], None],
    *,
    undefined: Callable[..., Any] | None = None,
    fallback: Callable[..., Any] | None = None,
    inplace: bool = False,
) -> Any:
    """Descriptor factory for commonvars.

    Parameters
    ----------
    cls
        The class of the underlying variable accessed within the manager.
    mgr
        Manager object.
    getter
        A function that returns the underlying variable from the manager.
    setter
        A function that sets the underlying variable within the manager.
    undefined
        Callable to be used as a fallback in case the variable is undefined
        (manager raises a `LookupError`).
    fallback
        Callable to be used as a fallback in case the attribute is undefined
        (the underlying variable raises an `AttributeError`).
    inplace
        Whether to treat the attribute as an inplace operator.
        Calls the setter with the result of the attribute call.

    Returns
    -------
    descriptor
        A descriptor object that can be used to create commonvars delegates.

    """

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
                with suppress(RuntimeError):
                    return getattr(getter(mgr), self.attr_name)

                def attribute() -> str:  # type: ignore[misc]
                    if cls is None:
                        return "<unbound commonvar>"
                    return f"<unbound {cls.__name__!r} object>"

            else:
                try:
                    obj = getter(mgr)
                except RuntimeError:
                    if callable(undefined):
                        attribute = undefined

                    else:
                        raise
                else:
                    try:
                        attribute = getattr(obj, self.attr_name)
                    except AttributeError:
                        if not callable(fallback):
                            raise

                        attribute = partial(fallback, obj)

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
        msg = f"No object in {mgr}"
        raise RuntimeError(msg) from None
    return obj


def _cv_setter(mgr: Manager[_T], value: _T) -> None:
    mgr.set(value)


def commonvar(
    mgr: Manager[_T],
    cls: type[_T] | None = None,
    getter: Callable[[Manager[_T]], _T] = None,  # type: ignore[assignment]
    setter: Callable[[Manager[_T], _T], None] = None,  # type: ignore[assignment]
) -> _T:
    """Create a common variable, i.e. a proxy object.

    Parameters
    ----------
    mgr
        Manager object. Must implement the `Manager` protocol.
        Matches `contextvars.ContextVar`.
    cls
        The class of the underlying variable accessed within the manager.
    getter
        A function that returns the underlying variable from the manager.
    setter
        A function that sets the underlying variable within the manager.

    Returns
    -------
    proxy
        A proxy object.
    """

    # pylint: disable=too-many-statements

    if getter is None:
        getter = _cv_getter

    if setter is None:
        setter = _cv_setter

    if cls is None:
        with suppress(RuntimeError):
            cls = type(getter(mgr))

    descriptor = partial(commonvar_descriptor, cls, mgr, getter, setter)

    class _CommonVarMeta:
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
        __bool__ = descriptor(undefined=lambda: False, fallback=operator.truth)
        __getattr__ = descriptor()
        __setattr__ = descriptor()
        __delattr__ = descriptor()
        if cls is None:
            __dir__ = descriptor()
            __class__ = descriptor()
        else:
            __dir__ = descriptor(undefined=lambda: dir(cls))
            __class__ = descriptor(undefined=lambda: cls)
        __call__ = descriptor()
        __instancecheck__ = descriptor()
        __subclasscheck__ = descriptor()
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

    if cls is not None:
        _CommonVarMeta.__name__ = _CommonVarMeta.__qualname__ = cls.__name__
    else:
        _CommonVarMeta.__name__ = _CommonVarMeta.__qualname__ = f"commonvar_{id(mgr):x}"
    return cast(_T, _CommonVarMeta())


proxy = commonvar
