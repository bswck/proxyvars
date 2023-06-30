import inspect
from collections.abc import Callable
from contextvars import ContextVar
from typing import TypeVar, Any, cast

_T = TypeVar("_T")


def zeugvarize(
    attr: Any,
    fetch: Callable[[], _T],
) -> Any:
    attr_name = attr.name

    class _ZeugVarDescriptor:
        def __get__(self, instance: _T, owner: type[_T] | None) -> Any:
            return getattr(fetch(), attr_name)

        def __set__(self, instance: _T, value: Any) -> None:
            setattr(fetch(), attr_name, value)

        def __delete__(self, instance: _T) -> None:
            delattr(fetch(), attr_name)

    return _ZeugVarDescriptor()


def zeugvar(
    typ: type[_T],
    cv: ContextVar[_T],
) -> _T:
    class_attrs = inspect.classify_class_attrs(typ)

    def fetch() -> _T:
        try:
            obj = cv.get()
        except LookupError:
            raise RuntimeError("No object in context") from None
        return obj

    class _ZeugVarMeta(type):
        def __repr__(self) -> str:
            try:
                obj = fetch()
            except RuntimeError:
                return f"<ZeugVar {typ.__name__} (no object)>"
            else:
                return repr(obj)

    return cast(_T, _ZeugVarMeta(
        typ.__name__, (),
        {attr.name: zeugvarize(attr, fetch) for attr in class_attrs}
    ))
