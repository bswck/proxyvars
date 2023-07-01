import contextlib
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

                def attribute() -> str:
                    return f"<unbound {cls.__name__!r} object>"

            else:
                try:
                    obj = fetch()
                except RuntimeError:
                    if self.attr_name == "__dir__" and not custom_mro:

                        def attribute():
                            return set(dir(cls)) - {"mro"}

                    elif callable(undefined):

                        def attribute(*args: Any, **kwargs: Any) -> Any:
                            return undefined(*args, **kwargs)

                    else:
                        raise
                else:
                    try:
                        attribute = getattr(obj, self.attr_name)
                    except AttributeError:
                        if not callable(fallback):
                            raise

                        def attribute(*args: Any, **kwargs: Any) -> Any:
                            return fallback(obj, *args, **kwargs)

            if inplace:
                def _apply_inplace(*args, **kwargs):
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

    mro = object.__getattribute__(cls, "mro")
    custom_mro = not hasattr(mro, "__self__")

    class _ZeugVarMeta(type):
        __doc__ = zeugvar_descriptor(cls, fetch, cv)
        __wrapped__ = zeugvar_descriptor(cls, fetch, cv)
        __repr__ = zeugvar_descriptor(cls, fetch, cv)
        __str__ = zeugvar_descriptor(cls, fetch, cv)
        __bytes__ = zeugvar_descriptor(cls, fetch, cv)
        __format__ = zeugvar_descriptor(cls, fetch, cv)
        __lt__ = zeugvar_descriptor(cls, fetch, cv)
        __le__ = zeugvar_descriptor(cls, fetch, cv)
        __eq__ = zeugvar_descriptor(cls, fetch, cv)
        __ne__ = zeugvar_descriptor(cls, fetch, cv)
        __gt__ = zeugvar_descriptor(cls, fetch, cv)
        __ge__ = zeugvar_descriptor(cls, fetch, cv)
        __hash__ = zeugvar_descriptor(cls, fetch, cv)
        __bool__ = zeugvar_descriptor(cls, fetch, cv, undefined=lambda: False)
        __getattr__ = zeugvar_descriptor(cls, fetch, cv)
        __setattr__ = zeugvar_descriptor(cls, fetch, cv)
        __delattr__ = zeugvar_descriptor(cls, fetch, cv)
        __dir__ = zeugvar_descriptor(cls, fetch, cv, undefined=lambda: dir(cls), custom_mro=custom_mro)
        __class__ = zeugvar_descriptor(cls, fetch, cv, undefined=lambda: cls)
        __instancecheck__ = zeugvar_descriptor(cls, fetch, cv)
        __subclasscheck__ = zeugvar_descriptor(cls, fetch, cv)
        __call__ = zeugvar_descriptor(cls, fetch, cv)
        __len__ = zeugvar_descriptor(cls, fetch, cv)
        __length_hint__ = zeugvar_descriptor(cls, fetch, cv)
        __getitem__ = zeugvar_descriptor(cls, fetch, cv)
        __setitem__ = zeugvar_descriptor(cls, fetch, cv)
        __delitem__ = zeugvar_descriptor(cls, fetch, cv)
        __iter__ = zeugvar_descriptor(cls, fetch, cv)
        __next__ = zeugvar_descriptor(cls, fetch, cv)
        __reversed__ = zeugvar_descriptor(cls, fetch, cv)
        __contains__ = zeugvar_descriptor(cls, fetch, cv)
        __add__ = zeugvar_descriptor(cls, fetch, cv)
        __sub__ = zeugvar_descriptor(cls, fetch, cv)
        __mul__ = zeugvar_descriptor(cls, fetch, cv)
        __matmul__ = zeugvar_descriptor(cls, fetch, cv)
        __truediv__ = zeugvar_descriptor(cls, fetch, cv)
        __floordiv__ = zeugvar_descriptor(cls, fetch, cv)
        __mod__ = zeugvar_descriptor(cls, fetch, cv)
        __divmod__ = zeugvar_descriptor(cls, fetch, cv)
        __pow__ = zeugvar_descriptor(cls, fetch, cv)
        __lshift__ = zeugvar_descriptor(cls, fetch, cv)
        __rshift__ = zeugvar_descriptor(cls, fetch, cv)
        __and__ = zeugvar_descriptor(cls, fetch, cv)
        __xor__ = zeugvar_descriptor(cls, fetch, cv)
        __or__ = zeugvar_descriptor(cls, fetch, cv)
        __radd__ = zeugvar_descriptor(cls, fetch, cv)
        __rsub__ = zeugvar_descriptor(cls, fetch, cv)
        __rmul__ = zeugvar_descriptor(cls, fetch, cv)
        __rmatmul__ = zeugvar_descriptor(cls, fetch, cv)
        __rtruediv__ = zeugvar_descriptor(cls, fetch, cv)
        __rfloordiv__ = zeugvar_descriptor(cls, fetch, cv)
        __rmod__ = zeugvar_descriptor(cls, fetch, cv)
        __rdivmod__ = zeugvar_descriptor(cls, fetch, cv)
        __rpow__ = zeugvar_descriptor(cls, fetch, cv)
        __rlshift__ = zeugvar_descriptor(cls, fetch, cv)
        __rrshift__ = zeugvar_descriptor(cls, fetch, cv)
        __rand__ = zeugvar_descriptor(cls, fetch, cv)
        __rxor__ = zeugvar_descriptor(cls, fetch, cv)
        __ror__ = zeugvar_descriptor(cls, fetch, cv)
        __iadd__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__add__"), inplace=True)
        __isub__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__sub__"), inplace=True)
        __imul__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__mul__"), inplace=True)
        __imatmul__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__matmul__"), inplace=True)
        __itruediv__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__truediv__"), inplace=True)
        __ifloordiv__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__floordiv__"), inplace=True)
        __imod__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__mod__"), inplace=True)
        __ipow__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__pow__"), inplace=True)
        __ilshift__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__lshift_"), inplace=True)
        __irshift__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__rshift__"), inplace=True)
        __iand__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__and__"), inplace=True)
        __ixor__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__xor__"), inplace=True)
        __ior__ = zeugvar_descriptor(cls, fetch, cv, fallback=_op_fallback("__or__"), inplace=True)
        __neg__ = zeugvar_descriptor(cls, fetch, cv)
        __pos__ = zeugvar_descriptor(cls, fetch, cv)
        __abs__ = zeugvar_descriptor(cls, fetch, cv)
        __invert__ = zeugvar_descriptor(cls, fetch, cv)
        __complex__ = zeugvar_descriptor(cls, fetch, cv)
        __int__ = zeugvar_descriptor(cls, fetch, cv)
        __float__ = zeugvar_descriptor(cls, fetch, cv)
        __index__ = zeugvar_descriptor(cls, fetch, cv)
        __round__ = zeugvar_descriptor(cls, fetch, cv)
        __trunc__ = zeugvar_descriptor(cls, fetch, cv)
        __floor__ = zeugvar_descriptor(cls, fetch, cv)
        __ceil__ = zeugvar_descriptor(cls, fetch, cv)
        __enter__ = zeugvar_descriptor(cls, fetch, cv)
        __exit__ = zeugvar_descriptor(cls, fetch, cv)
        __await__ = zeugvar_descriptor(cls, fetch, cv)
        __aiter__ = zeugvar_descriptor(cls, fetch, cv)
        __anext__ = zeugvar_descriptor(cls, fetch, cv)
        __aenter__ = zeugvar_descriptor(cls, fetch, cv)
        __aexit__ = zeugvar_descriptor(cls, fetch, cv)
        __copy__ = zeugvar_descriptor(cls, fetch, cv)
        __deepcopy__ = zeugvar_descriptor(cls, fetch, cv)

    zv = cast(_T, _ZeugVarMeta(cls.__name__, (), {}))
    if not custom_mro:

        def _mro_wrapper():
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
