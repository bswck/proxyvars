from contextvars import ContextVar
from math import inf

import pytest

from proxyvars import lookup_proxy


@pytest.fixture(params=[-100, 0, 5, 100])
def integers(request):
    context_var: ContextVar[int] = ContextVar("integer")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=[-100.0, 0.0, 5.0, 100.0, inf])
def floats(request):
    context_var: ContextVar[float] = ContextVar("float")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=["", "a", "abc"])
def strings(request):
    context_var: ContextVar[str] = ContextVar("string")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=[True, False])
def booleans(request):
    context_var: ContextVar[bool] = ContextVar("boolean")
    context_var.set(request.param)
    proxy_var = lookup_proxy(context_var)
    yield request.param, context_var, proxy_var


@pytest.fixture(params=[[], [1], [1, 2], ["foo", "bar"]])
def lists(request):
    context_var: ContextVar[list] = ContextVar("list")
    param = request.param.copy()
    context_var.set(param)
    proxy_var = lookup_proxy(context_var)
    yield param, context_var, proxy_var
