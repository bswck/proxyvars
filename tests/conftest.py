from __future__ import annotations

from contextvars import ContextVar
from math import inf

import pytest
from typing import TYPE_CHECKING

from proxyvars import lookup_proxy

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, TypeVar

    from pytest import FixtureRequest
    from typing_extensions import TypeAlias

    Object = TypeVar("Object")
    Objects: TypeAlias = "tuple[Object, ContextVar[Object], Object]"


@pytest.fixture(params=[-100, 0, 5, 100])
def integers(request: FixtureRequest) -> Iterator[Objects[int]]:
    context_var: ContextVar[int] = ContextVar("integer")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=[-100.0, 0.0, 5.0, 100.0, inf])
def floats(request: FixtureRequest) -> Iterator[Objects[float]]:
    context_var: ContextVar[float] = ContextVar("float")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=["", "a", "abc"])
def strings(request: FixtureRequest) -> Iterator[Objects[str]]:
    context_var: ContextVar[str] = ContextVar("string")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=[True, False])
def booleans(request: FixtureRequest) -> Iterator[Objects[bool]]:
    context_var: ContextVar[bool] = ContextVar("boolean")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=[[], [1], [1, 2], ["foo", "bar"]])
def lists(request: FixtureRequest) -> Iterator[Objects[list[Any]]]:
    context_var: ContextVar[list[Any]] = ContextVar("list")
    param = request.param.copy()
    context_var.set(param)
    proxy_var = lookup_proxy(context_var)
    yield param, context_var, proxy_var
