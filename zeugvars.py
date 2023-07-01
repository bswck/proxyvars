import contextlib
from collections.abc import Callable
from contextvars import ContextVar
from typing import TypeVar, Any, cast

_T = TypeVar("_T")


def zeugvar_descriptor(
    cls: type[_T],
    fetch: Callable[[], _T],
    *,
    undefined: Callable[..., Any] | None = None,
    fallback: Callable[..., Any] | None = None,
    custom_mro: bool = False
) -> Any:
    class _ZeugVarDescriptor:
        attr_name: str

        def __init__(self) -> None:
            self.attr_name = None  # type: ignore[assignment]

        def __set_name__(self, owner: type[_T], name: str) -> None:
            self.attr_name = name

        def __get__(self, instance: _T, owner: type[_T] | None) -> Any:
            if self.attr_name == "__getattr__":
                return lambda name: getattr(fetch(), name)
            if self.attr_name in ("__repr__", "__str__"):
                with contextlib.suppress(RuntimeError):
                    return getattr(fetch(), self.attr_name)
                return lambda: f"<unbound {cls.__name__!r} object>"
            try:
                obj = fetch()
            except RuntimeError:
                if self.attr_name == "__dir__" and not custom_mro:
                    return lambda: set(dir(cls)) - {"mro"}
                if callable(undefined):
                    return lambda *args, **kwargs: undefined(*args, **kwargs)
                raise
            else:
                try:
                    return getattr(obj, self.attr_name)
                except AttributeError:
                    if callable(fallback):
                        return lambda *args, **kwargs: fallback(obj, *args, **kwargs)
                    raise

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

    mro = object.__getattribute__(cls, "mro")
    custom_mro = not hasattr(mro, "__self__")

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
        __bool__ = zeugvar_descriptor(cls, fetch, undefined=lambda: False)
        __getattr__ = zeugvar_descriptor(cls, fetch)
        __setattr__ = zeugvar_descriptor(cls, fetch)
        __delattr__ = zeugvar_descriptor(cls, fetch)
        __dir__ = zeugvar_descriptor(cls, fetch, undefined=lambda: dir(cls), custom_mro=custom_mro)
        __class__ = zeugvar_descriptor(cls, fetch, undefined=lambda: cls)
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
        __iadd__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__add__")(op))
        __isub__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__sub__")(op))
        __imul__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__mul__")(op))
        __imatmul__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__matmul__")(op))
        __itruediv__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__truediv__")(op))
        __ifloordiv__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__floordiv__")(op))
        __imod__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__mod__")(op))
        __ipow__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__pow__")(op))
        __ilshift__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__lshift_")(op))
        __irshift__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__rshift__")(op))
        __iand__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__and__")(op))
        __ixor__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__xor__")(op))
        __ior__ = zeugvar_descriptor(cls, fetch, fallback=lambda obj, op: getattr(obj, "__or__")(op))
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

    zv = cast(_T, _ZeugVarMeta(cls.__name__, (), {}))
    if not custom_mro:
        def _mro_wrapper():
            try:
                fetch()
            except RuntimeError:
                return mro()
            else:
                raise AttributeError(f"{cls.__name__!r} object has no attribute 'mro'") from None

        type.__setattr__(zv, "mro", _mro_wrapper)
    return zv
