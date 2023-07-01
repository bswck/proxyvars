import contextlib
import functools
from collections.abc import Callable
from contextvars import ContextVar
from typing import TypeVar, Any, cast

_T = TypeVar("_T")


def zeugvar_descriptor(
    cls: type[_T],
    fetch: Callable[[], _T],
) -> Any:
    class _ZeugVarDescriptor:
        attr_name: str

        def __init__(self) -> None:
            self.attr_name = None  # type: ignore[assignment]

        def __set_name__(self, owner: type[_T], name: str) -> None:
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
                return lambda: f"<unbound {cls.__name__!r} object>"
            return getattr(fetch(), self.attr_name)

        def __set__(self, instance: _T, value: Any) -> None:
            setattr(fetch(), self.attr_name, value)

        def __delete__(self, instance: _T) -> None:
            delattr(fetch(), self.attr_name)

    return _ZeugVarDescriptor()


def zeugvar(
    cv: ContextVar[_T],
    cls: type[_T] = None,  # type: ignore[assignment]
) -> _T:
    def fetch() -> _T:
        try:
            obj = cv.get()
        except LookupError:
            raise RuntimeError("No object in context") from None
        return obj

    if cls is None:
        cls = type(fetch())

    class _ZeugVarMeta(type):
        __doc__ = zeugvar_descriptor(cls, fetch)
        __wrapped__ = zeugvar_descriptor(cls, fetch)
        __repr__ = zeugvar_descriptor(cls, fetch)
        __str__ = zeugvar_descriptor(cls, fetch)
        __bytes__ = zeugvar_descriptor(cls, fetch)
        __format__ = zeugvar_descriptor(cls, fetch)
        __lt__ = zeugvar_descriptor(cls, fetch)
        __le__ = zeugvar_descriptor(cls, fetch)
        __eq__ = zeugvar_descriptor(cls, fetch)
        __ne__ = zeugvar_descriptor(cls, fetch)
        __gt__ = zeugvar_descriptor(cls, fetch)
        __ge__ = zeugvar_descriptor(cls, fetch)
        __hash__ = zeugvar_descriptor(cls, fetch)
        __bool__ = zeugvar_descriptor(cls, fetch)
        __getattr__ = zeugvar_descriptor(cls, fetch)
        __setattr__ = zeugvar_descriptor(cls, fetch)
        __delattr__ = zeugvar_descriptor(cls, fetch)
        __dir__ = zeugvar_descriptor(cls, fetch)
        __class__ = zeugvar_descriptor(cls, fetch)
        __instancecheck__ = zeugvar_descriptor(cls, fetch)
        __subclasscheck__ = zeugvar_descriptor(cls, fetch)
        __call__ = zeugvar_descriptor(cls, fetch)
        __len__ = zeugvar_descriptor(cls, fetch)
        __length_hint__ = zeugvar_descriptor(cls, fetch)
        __getitem__ = zeugvar_descriptor(cls, fetch)
        __setitem__ = zeugvar_descriptor(cls, fetch)
        __delitem__ = zeugvar_descriptor(cls, fetch)
        __iter__ = zeugvar_descriptor(cls, fetch)
        __next__ = zeugvar_descriptor(cls, fetch)
        __reversed__ = zeugvar_descriptor(cls, fetch)
        __contains__ = zeugvar_descriptor(cls, fetch)
        __add__ = zeugvar_descriptor(cls, fetch)
        __sub__ = zeugvar_descriptor(cls, fetch)
        __mul__ = zeugvar_descriptor(cls, fetch)
        __matmul__ = zeugvar_descriptor(cls, fetch)
        __truediv__ = zeugvar_descriptor(cls, fetch)
        __floordiv__ = zeugvar_descriptor(cls, fetch)
        __mod__ = zeugvar_descriptor(cls, fetch)
        __divmod__ = zeugvar_descriptor(cls, fetch)
        __pow__ = zeugvar_descriptor(cls, fetch)
        __lshift__ = zeugvar_descriptor(cls, fetch)
        __rshift__ = zeugvar_descriptor(cls, fetch)
        __and__ = zeugvar_descriptor(cls, fetch)
        __xor__ = zeugvar_descriptor(cls, fetch)
        __or__ = zeugvar_descriptor(cls, fetch)
        __radd__ = zeugvar_descriptor(cls, fetch)
        __rsub__ = zeugvar_descriptor(cls, fetch)
        __rmul__ = zeugvar_descriptor(cls, fetch)
        __rmatmul__ = zeugvar_descriptor(cls, fetch)
        __rtruediv__ = zeugvar_descriptor(cls, fetch)
        __rfloordiv__ = zeugvar_descriptor(cls, fetch)
        __rmod__ = zeugvar_descriptor(cls, fetch)
        __rdivmod__ = zeugvar_descriptor(cls, fetch)
        __rpow__ = zeugvar_descriptor(cls, fetch)
        __rlshift__ = zeugvar_descriptor(cls, fetch)
        __rrshift__ = zeugvar_descriptor(cls, fetch)
        __rand__ = zeugvar_descriptor(cls, fetch)
        __rxor__ = zeugvar_descriptor(cls, fetch)
        __ror__ = zeugvar_descriptor(cls, fetch)
        __iadd__ = zeugvar_descriptor(cls, fetch)
        __isub__ = zeugvar_descriptor(cls, fetch)
        __imul__ = zeugvar_descriptor(cls, fetch)
        __imatmul__ = zeugvar_descriptor(cls, fetch)
        __itruediv__ = zeugvar_descriptor(cls, fetch)
        __ifloordiv__ = zeugvar_descriptor(cls, fetch)
        __imod__ = zeugvar_descriptor(cls, fetch)
        __ipow__ = zeugvar_descriptor(cls, fetch)
        __ilshift__ = zeugvar_descriptor(cls, fetch)
        __irshift__ = zeugvar_descriptor(cls, fetch)
        __iand__ = zeugvar_descriptor(cls, fetch)
        __ixor__ = zeugvar_descriptor(cls, fetch)
        __ior__ = zeugvar_descriptor(cls, fetch)
        __neg__ = zeugvar_descriptor(cls, fetch)
        __pos__ = zeugvar_descriptor(cls, fetch)
        __abs__ = zeugvar_descriptor(cls, fetch)
        __invert__ = zeugvar_descriptor(cls, fetch)
        __complex__ = zeugvar_descriptor(cls, fetch)
        __int__ = zeugvar_descriptor(cls, fetch)
        __float__ = zeugvar_descriptor(cls, fetch)
        __index__ = zeugvar_descriptor(cls, fetch)
        __round__ = zeugvar_descriptor(cls, fetch)
        __trunc__ = zeugvar_descriptor(cls, fetch)
        __floor__ = zeugvar_descriptor(cls, fetch)
        __ceil__ = zeugvar_descriptor(cls, fetch)
        __enter__ = zeugvar_descriptor(cls, fetch)
        __exit__ = zeugvar_descriptor(cls, fetch)
        __await__ = zeugvar_descriptor(cls, fetch)
        __aiter__ = zeugvar_descriptor(cls, fetch)
        __anext__ = zeugvar_descriptor(cls, fetch)
        __aenter__ = zeugvar_descriptor(cls, fetch)
        __aexit__ = zeugvar_descriptor(cls, fetch)
        __copy__ = zeugvar_descriptor(cls, fetch)
        __deepcopy__ = zeugvar_descriptor(cls, fetch)

    return cast(_T, _ZeugVarMeta(cls.__name__, (), {}))
