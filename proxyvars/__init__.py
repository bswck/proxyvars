"""
proxyvars - a simple and straight-forward Python library for proxy objects.

(C) 2023-present Bartosz Sławecki (bswck)
"""
from __future__ import annotations

import operator
import weakref
from contextlib import suppress
from functools import partial, reduce
from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    TypeVar,
    cast,
    runtime_checkable,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping


__all__ = (
    "proxy",
    "const_proxy",
    "lookup_proxy",
    "proxy_field_accessor",
    "proxy_item_accessor",
    "proxy_attribute_accessor",
)

_T = TypeVar("_T")
_MISSING = object()


class MissingStateError(RuntimeError):
    """Raised when a proxy object is accessed without a state."""


def proxy_descriptor(  # noqa: C901
    get_state: Callable[..., _T],
    overwrite_state: Callable[[_T], None],
    *,
    class_value: object = _MISSING,
    implementation: object = _MISSING,
    try_state_first: bool = False,
    on_missing_state: Callable[..., Any] | None = None,
    on_attribute_error: Callable[..., Any] | None = None,
    is_inplace_method: bool = False,
) -> Any:
    """Proxy descriptor factory for composing proxy classes on the fly."""
    attribute_name: str

    class ProxyDescriptor:
        """
        Descriptor that handles proxied attribute lookup.

        Similar to `werkzeug.local._ProxyLookup`.
        """

        def __set_name__(self, _: type[_T], name: str) -> None:
            nonlocal attribute_name
            attribute_name = name

        def __get__(self, instance: _T, _: type[_T] | None = None) -> Any:  # noqa: C901
            nonlocal attribute_name

            if instance is None and class_value is not _MISSING:
                return class_value

            if try_state_first:
                with suppress(MissingStateError):
                    return getattr(get_state(), attribute_name)

            if implementation is not _MISSING:
                return implementation

            try:
                state = get_state()

            except MissingStateError:
                if not callable(on_missing_state):
                    raise
                attribute = on_missing_state

            else:
                try:
                    attribute = getattr(state, attribute_name)
                except AttributeError:
                    if not callable(on_attribute_error):
                        raise

                    attribute = partial(on_attribute_error, state)

            if is_inplace_method:

                def inplace_method(*args: object, **kwargs: object) -> _T:
                    if not callable(attribute):
                        msg = (
                            f"Cannot overwrite object {state!r} "
                            f"because {attribute_name!r} is not a method "
                            "(must be callable)"
                        )
                        raise TypeError(msg)

                    new_state = attribute(*args, **kwargs)
                    overwrite_state(new_state)
                    return instance

                return inplace_method

            return attribute

        def __set__(self, _: object, value: object) -> None:
            nonlocal attribute_name
            setattr(get_state(), attribute_name, value)

        def __delete__(self, _: object) -> None:
            nonlocal attribute_name
            delattr(get_state(), attribute_name)

    return ProxyDescriptor()


def _binary_op_use_instead(
    operator_name: str,
) -> Callable[[object, object], object]:
    return lambda state, operand: getattr(state, operator_name)(operand)


def _try_classgetitem(
    cls: type[_T],
    name: str,
) -> object:
    if not isinstance(cls, type):
        msg = f"{cls!r} object has no attribute '__class_getitem__'"
        raise AttributeError(msg)  # noqa: TRY004
    try:
        class_getitem = cls.__class_getitem__  # type: ignore[attr-defined]
    except AttributeError:
        msg = f"{cls!r} is not generic (does not support class-item access)"
        raise TypeError(msg) from None
    return class_getitem(name)


def proxy(
    get_state: Callable[..., _T],
    overwrite_state: Callable[[_T], None],
    cls: type[_T] | None = None,
    proxy_base_cls: type[object] = object,
    proxy_metaclass: type[type] = type,
    namespace_overwrites: Mapping[str, object] | None = None,
) -> _T:
    """
    Create a proxy object.

    Parameters
    ----------
    get_state
        A callable that returns the current state of the proxy.
    overwrite_state
        A callable that overwrites the current state of the proxy.
    cls
        The class of the object to be proxied.
    proxy_base_cls
        The base class of the proxy object (default: `object`).
        This is useful if you want add custom descriptors to the result proxy object.
    proxy_metaclass
        The metaclass of the proxy object (default: `type`).
        This is useful if you want add custom descriptors to the result proxy object.
    namespace_overwrites
        A mapping of attribute names to values that the namespace
        of the Proxy class will be updated with before the class's creation.
    """
    descriptor = partial(proxy_descriptor, get_state, overwrite_state)

    class Proxy(
        proxy_base_cls,  # type: ignore[misc,valid-type]
        metaclass=lambda name, bases, namespace: proxy_metaclass(  # type: ignore[misc]
            name,
            bases,
            {**namespace, **(namespace_overwrites or {})},
        ),
    ):
        """
        A class whose instance proxies %(cls_name)s.

        Similar to `werkzeug.local.LocalProxy`.
        """

        if cls is None:
            __doc__ = descriptor(  # noqa: A003
                class_value=__doc__ and __doc__ % {"cls_name": "other object"},
            )
            __dir__ = descriptor()
            __class__ = descriptor()
        else:
            __doc__ = descriptor(  # noqa: A003
                class_value=__doc__ and __doc__ % {"cls_name": repr(cls.__name__)},
            )
            __dir__ = descriptor(on_missing_state=lambda: dir(cls))
            __class__ = descriptor(implementation=cls)
        __wrapped__ = descriptor()
        __repr__, __str__ = [
            descriptor(
                implementation=lambda: (
                    "<object (no state)>"
                    if cls is None
                    else f"<{cls.__name__!r} object (no state)>"
                ),
                try_state_first=True,
            ),
        ] * 2
        __bytes__ = descriptor()
        __format__ = descriptor()
        __lt__ = descriptor()
        __le__ = descriptor()
        __eq__ = descriptor()
        __ne__ = descriptor()
        __gt__ = descriptor()
        __ge__ = descriptor()
        __hash__ = descriptor()
        __bool__ = descriptor(
            on_missing_state=lambda: False,
            on_attribute_error=operator.truth,
        )
        __getattr__ = descriptor(
            implementation=lambda name: getattr(get_state(), name),
        )
        __setattr__ = descriptor()
        __delattr__ = descriptor()
        __call__ = descriptor()
        __instancecheck__ = descriptor()
        __subclasscheck__ = descriptor()
        __len__ = descriptor()
        __length_hint__ = descriptor()
        __getitem__ = descriptor(on_attribute_error=_try_classgetitem)
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
        __iadd__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__add__"),
            is_inplace_method=True,
        )
        __isub__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__sub__"),
            is_inplace_method=True,
        )
        __imul__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__mul__"),
            is_inplace_method=True,
        )
        __imatmul__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__matmul__"),
            is_inplace_method=True,
        )
        __itruediv__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__truediv__"),
            is_inplace_method=True,
        )
        __ifloordiv__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__floordiv__"),
            is_inplace_method=True,
        )
        __imod__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__mod__"),
            is_inplace_method=True,
        )
        __ipow__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__pow__"),
            is_inplace_method=True,
        )
        __ilshift__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__lshift__"),
            is_inplace_method=True,
        )
        __irshift__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__rshift__"),
            is_inplace_method=True,
        )
        __iand__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__and__"),
            is_inplace_method=True,
        )
        __ixor__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__xor__"),
            is_inplace_method=True,
        )
        __ior__ = descriptor(
            on_attribute_error=_binary_op_use_instead("__or__"),
            is_inplace_method=True,
        )
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
        Proxy.__name__ = Proxy.__qualname__ = cls.__name__
    else:
        Proxy.__name__ = Proxy.__qualname__ = f"proxy_{id(Proxy):x}"
    return cast(_T, Proxy())


def _const_proxy_overwrite_state(_: _T) -> None:
    msg = "Cannot overwrite a constant proxy"
    raise TypeError(msg)


def _const_proxy_get_state(state: _T) -> _T:
    return state


def _const_proxy_get_state_weak(weak_ref: weakref.ReferenceType[_T]) -> _T:
    state = weak_ref()
    if state is None:
        msg = "Weak reference expired"
        raise MissingStateError(msg)
    return state


def const_proxy(
    state: object,
    cls: type[_T],
    *,
    proxy_base_cls: type[object] = object,
    proxy_metaclass: type[type] = type,
    namespace_overwrites: Mapping[str, object] | None = None,
    weak: bool = False,
    weakref_callback: Callable[[object], None] | None = None,
) -> _T:
    """
    Create a proxy object that cheats class/instance checks with the given cls.

    This proxy is guaranteed to refer to a state object with a constant ID.

    Parameters
    ----------
    state
        The state of the proxy to point to.
    cls
        The class of the object to cheat class/instance checks with.
    proxy_base_cls
        The base class of the proxy object (default: `object`).
        This is useful if you want add custom descriptors to the result proxy object.
    weak
        Whether to use a weak reference to the state.
    weakref_callback
        A callback that is called when the weak reference to the state is about
        to expire. See the `weakref.ref` documentation for details.
    proxy_metaclass
        The metaclass of the proxy object (default: `type`).
        This is useful if you want add custom descriptors to the result proxy object.
    namespace_overwrites
        A mapping of attribute names to values that the namespace
        of the Proxy class will be updated with before the class's creation.
    """
    if weakref_callback and not weak:
        msg = "weakref_callback requires weak=True"
        raise ValueError(msg)

    if weak:
        get_state = partial(
            _const_proxy_get_state_weak,
            weakref.ref(state, weakref_callback),
        )
    else:
        get_state = partial(_const_proxy_get_state, state)

    return proxy(
        cls=cls,
        get_state=get_state,
        overwrite_state=_const_proxy_overwrite_state,
        proxy_base_cls=proxy_base_cls,
        proxy_metaclass=proxy_metaclass,
        namespace_overwrites=namespace_overwrites,
    )


@runtime_checkable
class ProxyStateLookup(Protocol[_T]):
    """
    A protocol for objects that looks up the state of a proxy every time it is accessed.

    If the state lookup fails, a `LookupError` must be raised.
    It is then converted to `MissingStateError` and handled by the proxy instance,
    which might be finally propagated to the caller.

    Note:
    ----
    All `contextvars.ContextVar` objects are valid proxy state lookups.
    """

    def get(self) -> _T:
        """Get the current state of the proxy."""

    def set(self, value: _T, /) -> Any:  # noqa: A003
        """Overwrite the current state of the proxy."""


def _lookup_proxy_get_state(state_lookup: ProxyStateLookup[_T]) -> _T:
    try:
        state = state_lookup.get()
    except LookupError as exc:
        note = ""
        if exc.args:
            note = f" ({exc.args[0]})"
        msg = f"No object in {state_lookup!r}{note}"
        raise MissingStateError(msg) from None
    return state


def _lookup_proxy_overwrite_state(
    state_lookup: ProxyStateLookup[_T],
    value: _T,
) -> None:
    state_lookup.set(value)


def lookup_proxy(
    state_lookup: ProxyStateLookup[_T],
    cls: type[_T] | None = None,
    state_lookup_get_state: Callable[[ProxyStateLookup[_T]], _T] | None = None,
    state_lookup_overwrite_state: Callable[[ProxyStateLookup[_T], _T], None]
    | None = None,
    *,
    proxy_base_cls: type[object] = object,
    proxy_metaclass: type[type] = type,
    namespace_overwrites: Mapping[str, object] | None = None,
) -> _T:
    """
    Create a proxy object that uses a `ProxyStateLookup` to lookup the state.

    Parameters
    ----------
    state_lookup
        The state lookup object. Must implement the `ProxyStateLookup` protocol.
        It will be used to lookup the state of the proxy every time it is accessed.
    cls
        The class of the object to be proxied.
    proxy_base_cls
        The base class of the proxy object (default: `object`).
        This is useful if you want add custom descriptors to the result proxy object.
    proxy_metaclass
        The metaclass of the proxy object (default: `type`).
        This is useful if you want add custom descriptors to the result proxy object.
    namespace_overwrites
        A mapping of attribute names to values that the namespace
        of the Proxy class will be updated with before the class's creation.
    state_lookup_get_state
        A callable that returns the current state of the proxy.
        Defaults to `state_lookup.get`.
    state_lookup_overwrite_state
        A callable that overwrites the current state of the proxy.
    """
    if state_lookup_get_state is None:
        state_lookup_get_state = _lookup_proxy_get_state
    get_state = partial(state_lookup_get_state, state_lookup)

    if state_lookup_overwrite_state is None:
        state_lookup_overwrite_state = _lookup_proxy_overwrite_state
    overwrite_state = partial(state_lookup_overwrite_state, state_lookup)

    if cls is None:
        with suppress(MissingStateError):
            cls = type(get_state())

    return proxy(
        cls=cls,
        get_state=get_state,
        overwrite_state=overwrite_state,
        proxy_base_cls=proxy_base_cls,
        proxy_metaclass=proxy_metaclass,
        namespace_overwrites=namespace_overwrites,
    )


def _proxy_field_get_state(
    obj: Any,
    field: object,
) -> object:
    if isinstance(field, str):
        return getattr(obj, field)
    return obj[field]


def _proxy_field_overwrite_state(
    obj: Any,
    field: object,
    value: object,
) -> None:
    if isinstance(field, str):
        setattr(obj, field, value)
    else:
        obj[field] = value


def proxy_field_accessor(
    *path: object,
    proxy_var: object,
    cls: type[_T] | None = None,
    field_get_state: Callable[[Any, object], object] = _proxy_field_get_state,
    field_overwrite_state: Callable[
        [Any, object, object],
        None,
    ] = _proxy_field_overwrite_state,
    proxy_base_cls: type[object] = object,
    proxy_metaclass: type[type] = type,
    namespace_overwrites: Mapping[str, object] | None = None,
) -> _T:
    """
    Create a proxy that accesses a (maybe nested) field of another proxy.

    The valid usage of this function resembles the way to use the `AliasPath` class
    from [pydantic 2](https://docs.pydantic.dev/2.3/).

    Parameters
    ----------
    path
        The path to the field to be accessed.
        Each item in the path can be either a string (for attribute access)
        or a custom object (for item access).
        This behavior that treats strings specially might be customized
        by passing custom `field_get_state` and `field_overwrite_state` functions.

        For example, the path `("a", 0, "b")` would be equivalent to
        `proxy_var.a[0].b`. To change it the behavior to `proxy_var["a"][0]["b"]`,
        simply use `proxy_item_accessor` directly
        or  pass `field_get_state=lambda o, f: o[f]`
        and `field_overwrite_state=lambda o, f, v: o.__setitem__(o, f, v)`
        to this function.
    proxy_var
        The proxy object to be accessed.
    cls
        The class of the object to be proxied.
    field_get_state
        A callable that gets a field from an object.
        Defaults to `getattr` for strings and `.__getitem__()` otherwise.
    field_overwrite_state
        A callable that overwrites a field of an object.
        Defaults to `setattr` for strings and `.__setitem__()` otherwise.
    proxy_base_cls
        The base class of the proxy object (default: `object`).
        This is useful if you want add custom descriptors to the result proxy object.
    proxy_metaclass
        The metaclass of the proxy object (default: `type`).
        This is useful if you want add custom descriptors to the result proxy object.
    namespace_overwrites
        A mapping of attribute names to values that the namespace
        of the Proxy class will be updated with before the class's creation.
    """
    if not path:
        msg = "proxy field path must not be empty"
        raise ValueError(msg)

    def get_state() -> _T:
        return cast(_T, reduce(field_get_state, path, proxy_var))

    def overwrite_state(state: _T) -> None:
        *path_there, last_field = path
        last_item = proxy_var
        if path_there:
            last_item = reduce(field_get_state, path_there, proxy_var)
        field_overwrite_state(last_item, last_field, state)

    return proxy(
        get_state,
        overwrite_state,
        cls=cls,
        proxy_base_cls=proxy_base_cls,
        proxy_metaclass=proxy_metaclass,
        namespace_overwrites=namespace_overwrites,
    )


def _proxy_item_get_state(
    obj: Any,
    field: object,
) -> object:
    return obj[field]


def _proxy_item_overwrite_state(
    obj: Any,
    field: object,
    value: object,
) -> None:
    obj[field] = value


def proxy_item_accessor(
    *path: object,
    proxy_var: object,
    cls: type[_T] | None = None,
    proxy_base_cls: type[object] = object,
    proxy_metaclass: type[type] = type,
    namespace_overwrites: Mapping[str, object] | None = None,
) -> _T:
    """
    Create a proxy that accesses a (maybe nested) item of another proxy.

    The valid usage of this function resembles the way to use the `AliasPath` class
    from [pydantic 2](https://docs.pydantic.dev/2.3/).

    Parameters
    ----------
    path
        The path to the item to be accessed.
        Every item in the path will be used as a key to access the next item.
        For example, the path `("a", 0, "b")` would be equivalent to
        `proxy_var["a"][0]["b"]`.

        To change this behavior to `proxy_var.a[0].b`, simply use `proxy_field_accessor`
        instead.
    proxy_var
        The proxy object to be accessed.
    cls
        The class of the object to be proxied.
    proxy_base_cls
        The base class of the proxy object (default: `object`).
        This is useful if you want add custom descriptors to the result proxy object.
    proxy_metaclass
        The metaclass of the proxy object (default: `type`).
        This is useful if you want add custom descriptors to the result proxy object.
    namespace_overwrites
        A mapping of attribute names to values that the namespace
        of the Proxy class will be updated with before the class's creation.
    """
    return proxy_field_accessor(
        *path,
        proxy_var=proxy_var,
        cls=cls,
        field_get_state=_proxy_field_get_state,
        field_overwrite_state=_proxy_field_overwrite_state,
        proxy_base_cls=proxy_base_cls,
        proxy_metaclass=proxy_metaclass,
        namespace_overwrites=namespace_overwrites,
    )


def _proxy_attribute_get_state(
    obj: Any,
    field: object,
) -> object:
    if not isinstance(field, str):
        msg = "attribute access requires a string field"
        raise TypeError(msg)
    return getattr(obj, field)


def _proxy_attribute_overwrite_state(
    obj: Any,
    field: object,
    value: object,
) -> None:
    if not isinstance(field, str):
        msg = "attribute access requires a string field"
        raise TypeError(msg)
    setattr(obj, field, value)


def proxy_attribute_accessor(
    *path: str,
    proxy_var: object,
    cls: type[_T] | None = None,
    proxy_base_cls: type[object] = object,
    proxy_metaclass: type[type] = type,
    namespace_overwrites: Mapping[str, object] | None = None,
) -> _T:
    """
    Create a proxy that accesses a (maybe nested) attribute of another proxy.

    The valid usage of this function resembles the way to use the `AliasPath` class
    from [pydantic 2](https://docs.pydantic.dev/2.3/).

    Parameters
    ----------
    path
        The path to the item to be accessed.
        Every item in the path will be used as a key to access the next item.
        For example, the path `("a", 0, "b")` would be invalid
        and result in a TypeError, because `0` is not
        a string. The path `("a", "0", "b")` would be then equivalent to
        `getattr(proxy_var.a, "0").b`.

        To change this behavior to `proxy_var.a[0].b`, simply use `proxy_field_accessor`
        instead. If you need to change this behavior to `proxy_var["a"][0]["b"]` though,
        consider using `proxy_item_accessor` instead.
    proxy_var
        The proxy object to be accessed.
    cls
        The class of the object to be proxied.
    proxy_base_cls
        The base class of the proxy object (default: `object`).
        This is useful if you want add custom descriptors to the result proxy object.
    proxy_metaclass
        The metaclass of the proxy object (default: `type`).
        This is useful if you want add custom descriptors to the result proxy object.
    namespace_overwrites
        A mapping of attribute names to values that the namespace
        of the Proxy class will be updated with before the class's creation.
    """
    return proxy_field_accessor(
        *path,
        proxy_var=proxy_var,
        cls=cls,
        field_get_state=_proxy_attribute_get_state,
        field_overwrite_state=_proxy_attribute_overwrite_state,
        proxy_base_cls=proxy_base_cls,
        proxy_metaclass=proxy_metaclass,
        namespace_overwrites=namespace_overwrites,
    )
