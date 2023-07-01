import contextlib
import functools
from collections.abc import Callable
from contextvars import ContextVar
from typing import TypeVar, Any, cast

_T = TypeVar("_T")


def zeugvar_descriptor(
    cls: type[_T],
    fetch: Callable[[], _T],
    cv: ContextVar[_T],
    *,
    undefined: Callable[..., Any] | None = None,
    fallback: Callable[..., Any] | None = None,
    custom_mro: bool = False,
    inplace: bool = False,
) -> Any:
    class _ZeugVarDescriptor:
        attr_name: str

        def __init__(self) -> None:
            self.attr_name = None  # type: ignore[assignment]

        def __set_name__(self, owner: type[_T], name: str) -> None:
            self.attr_name = name

        def __get__(self, instance: _T, owner: type[_T] | None) -> Any:
            if self.attr_name == "__getattr__":

                def attribute(name: str) -> Any:
                    return getattr(fetch(), name)

            elif self.attr_name in ("__repr__", "__str__"):
                with contextlib.suppress(RuntimeError):
                    return getattr(fetch(), self.attr_name)

                def attribute() -> str:  # type: ignore[misc]
                    return f"<unbound {cls.__name__!r} object>"

            else:
                try:
                    obj = fetch()
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
                    cv.set(ret)
                    return instance

                return _apply_inplace
            return attribute

        def __set__(self, instance: _T, value: Any) -> None:
            setattr(fetch(), self.attr_name, value)

        def __delete__(self, instance: _T) -> None:
            delattr(fetch(), self.attr_name)

    return _ZeugVarDescriptor()


def _op_fallback(op_name: str) -> Callable[[Any, Any], Any]:
    return lambda obj, op: getattr(obj, op_name)(op)


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

    mro: Callable[[], tuple[type[Any], ...]] = object.__getattribute__(cls, "mro")
    custom_mro = not hasattr(mro, "__self__")
    descriptor = functools.partial(zeugvar_descriptor, cls, fetch, cv, custom_mro=custom_mro)

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
                fetch()
            except RuntimeError:
                return mro()
            else:
                raise AttributeError(
                    f"{cls.__name__!r} object has no attribute 'mro'"
                ) from None

        type.__setattr__(zv, "mro", _mro_wrapper)
    return zv
