import contextlib
import functools
from collections.abc import Callable
from contextvars import ContextVar
from typing import TypeVar, Any, cast

_T = TypeVar("_T")


def zeugvar_descriptor(
    typ: type[_T],
    fetch: Callable[[], _T],
) -> Any:
    class _ZeugVarDescriptor:
        def __init__(self) -> None:
            self.attr_name = None

        def __set_name__(self, owner, name):
            self.attr_name = name

        @functools.cached_property
        def is_printed(self) -> bool:
            return self.attr_name in ("__repr__", "__str__")

        def __get__(self, instance: _T, owner: type[_T] | None) -> Any:
            if self.attr_name == "__getattr__":
                return lambda name: getattr(fetch(), name)
            if self.is_printed:
                with contextlib.suppress(RuntimeError):
                    return getattr(fetch(), self.attr_name)
                return lambda: f"<unbound {typ.__name__!r} object>"
            return getattr(fetch(), self.attr_name)

        def __set__(self, instance: _T, value: Any) -> None:
            setattr(fetch(), self.attr_name, value)

        def __delete__(self, instance: _T) -> None:
            delattr(fetch(), self.attr_name)

    return _ZeugVarDescriptor()


def zeugvar(
    cv: ContextVar[_T],
    typ: type[_T] | None = None,
) -> _T:
    def fetch() -> _T:
        try:
            obj = cv.get()
        except LookupError:
            raise RuntimeError("No object in context") from None
        return obj

    if typ is None:
        typ = type(fetch())

    class _ZeugVarMeta(type):
        __doc__ = zeugvar_descriptor(typ, fetch)
        __wrapped__ = zeugvar_descriptor(typ, fetch)
        __repr__ = zeugvar_descriptor(typ, fetch)
        __str__ = zeugvar_descriptor(typ, fetch)
        __bytes__ = zeugvar_descriptor(typ, fetch)
        __format__ = zeugvar_descriptor(typ, fetch)
        __lt__ = zeugvar_descriptor(typ, fetch)
        __le__ = zeugvar_descriptor(typ, fetch)
        __eq__ = zeugvar_descriptor(typ, fetch)
        __ne__ = zeugvar_descriptor(typ, fetch)
        __gt__ = zeugvar_descriptor(typ, fetch)
        __ge__ = zeugvar_descriptor(typ, fetch)
        __hash__ = zeugvar_descriptor(typ, fetch)
        __bool__ = zeugvar_descriptor(typ, fetch)
        __getattr__ = zeugvar_descriptor(typ, fetch)
        __setattr__ = zeugvar_descriptor(typ, fetch)
        __delattr__ = zeugvar_descriptor(typ, fetch)
        __dir__ = zeugvar_descriptor(typ, fetch)
        __class__ = zeugvar_descriptor(typ, fetch)
        __instancecheck__ = zeugvar_descriptor(typ, fetch)
        __subclasscheck__ = zeugvar_descriptor(typ, fetch)
        __call__ = zeugvar_descriptor(typ, fetch)
        __len__ = zeugvar_descriptor(typ, fetch)
        __length_hint__ = zeugvar_descriptor(typ, fetch)
        __getitem__ = zeugvar_descriptor(typ, fetch)
        __setitem__ = zeugvar_descriptor(typ, fetch)
        __delitem__ = zeugvar_descriptor(typ, fetch)
        __iter__ = zeugvar_descriptor(typ, fetch)
        __next__ = zeugvar_descriptor(typ, fetch)
        __reversed__ = zeugvar_descriptor(typ, fetch)
        __contains__ = zeugvar_descriptor(typ, fetch)
        __add__ = zeugvar_descriptor(typ, fetch)
        __sub__ = zeugvar_descriptor(typ, fetch)
        __mul__ = zeugvar_descriptor(typ, fetch)
        __matmul__ = zeugvar_descriptor(typ, fetch)
        __truediv__ = zeugvar_descriptor(typ, fetch)
        __floordiv__ = zeugvar_descriptor(typ, fetch)
        __mod__ = zeugvar_descriptor(typ, fetch)
        __divmod__ = zeugvar_descriptor(typ, fetch)
        __pow__ = zeugvar_descriptor(typ, fetch)
        __lshift__ = zeugvar_descriptor(typ, fetch)
        __rshift__ = zeugvar_descriptor(typ, fetch)
        __and__ = zeugvar_descriptor(typ, fetch)
        __xor__ = zeugvar_descriptor(typ, fetch)
        __or__ = zeugvar_descriptor(typ, fetch)
        __radd__ = zeugvar_descriptor(typ, fetch)
        __rsub__ = zeugvar_descriptor(typ, fetch)
        __rmul__ = zeugvar_descriptor(typ, fetch)
        __rmatmul__ = zeugvar_descriptor(typ, fetch)
        __rtruediv__ = zeugvar_descriptor(typ, fetch)
        __rfloordiv__ = zeugvar_descriptor(typ, fetch)
        __rmod__ = zeugvar_descriptor(typ, fetch)
        __rdivmod__ = zeugvar_descriptor(typ, fetch)
        __rpow__ = zeugvar_descriptor(typ, fetch)
        __rlshift__ = zeugvar_descriptor(typ, fetch)
        __rrshift__ = zeugvar_descriptor(typ, fetch)
        __rand__ = zeugvar_descriptor(typ, fetch)
        __rxor__ = zeugvar_descriptor(typ, fetch)
        __ror__ = zeugvar_descriptor(typ, fetch)
        __iadd__ = zeugvar_descriptor(typ, fetch)
        __isub__ = zeugvar_descriptor(typ, fetch)
        __imul__ = zeugvar_descriptor(typ, fetch)
        __imatmul__ = zeugvar_descriptor(typ, fetch)
        __itruediv__ = zeugvar_descriptor(typ, fetch)
        __ifloordiv__ = zeugvar_descriptor(typ, fetch)
        __imod__ = zeugvar_descriptor(typ, fetch)
        __ipow__ = zeugvar_descriptor(typ, fetch)
        __ilshift__ = zeugvar_descriptor(typ, fetch)
        __irshift__ = zeugvar_descriptor(typ, fetch)
        __iand__ = zeugvar_descriptor(typ, fetch)
        __ixor__ = zeugvar_descriptor(typ, fetch)
        __ior__ = zeugvar_descriptor(typ, fetch)
        __neg__ = zeugvar_descriptor(typ, fetch)
        __pos__ = zeugvar_descriptor(typ, fetch)
        __abs__ = zeugvar_descriptor(typ, fetch)
        __invert__ = zeugvar_descriptor(typ, fetch)
        __complex__ = zeugvar_descriptor(typ, fetch)
        __int__ = zeugvar_descriptor(typ, fetch)
        __float__ = zeugvar_descriptor(typ, fetch)
        __index__ = zeugvar_descriptor(typ, fetch)
        __round__ = zeugvar_descriptor(typ, fetch)
        __trunc__ = zeugvar_descriptor(typ, fetch)
        __floor__ = zeugvar_descriptor(typ, fetch)
        __ceil__ = zeugvar_descriptor(typ, fetch)
        __enter__ = zeugvar_descriptor(typ, fetch)
        __exit__ = zeugvar_descriptor(typ, fetch)
        __await__ = zeugvar_descriptor(typ, fetch)
        __aiter__ = zeugvar_descriptor(typ, fetch)
        __anext__ = zeugvar_descriptor(typ, fetch)
        __aenter__ = zeugvar_descriptor(typ, fetch)
        __aexit__ = zeugvar_descriptor(typ, fetch)
        __copy__ = zeugvar_descriptor(typ, fetch)
        __deepcopy__ = zeugvar_descriptor(typ, fetch)

    return cast(_T, _ZeugVarMeta(typ.__name__, (), {}))
