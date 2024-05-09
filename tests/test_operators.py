from __future__ import annotations

from contextvars import ContextVar
from itertools import chain
from math import isinf
from random import choice
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest

from proxyvars import lookup_proxy

from tests.conftest import (
    booleans as booleans_fixture,
    integers as integers_fixture,
    floats as floats_fixture,
    strings as strings_fixture,
    lists as lists_fixture,
)

try:
    import numpy as np  # type: ignore[module-not-found]
except ImportError:
    np = None

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from typing import Any, TypeVar

    from tests.conftest import Objects

    R = TypeVar("R")


def lazy_fixture(fixture: Callable[..., Iterator[R]]) -> Iterator[R]:
    marker = fixture._pytestfixturefunction
    fixture_func = fixture.__wrapped__
    yield from (
        next(fixture_func(SimpleNamespace(param=param))) for param in marker.params
    )


integers_and_floats = pytest.mark.parametrize(
    "objects",
    chain(
        lazy_fixture(integers_fixture),
        lazy_fixture(floats_fixture),
    ),
)


strings_and_lists = pytest.mark.parametrize(
    "objects",
    chain(
        lazy_fixture(strings_fixture),
        lazy_fixture(lists_fixture),
    ),
)


@integers_and_floats
def test_abs(objects: Objects[int | float]) -> None:
    actual, _, proxy_var = objects
    assert abs(actual) == abs(proxy_var)


@integers_and_floats
def test_add(objects: Objects[int | float]) -> None:
    actual, _, proxy_var = objects
    assert actual + 1 == proxy_var + 1


def test_and_(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual & 1 == proxy_var & 1


def test_concat(strings: Objects[str]) -> None:
    actual, _, proxy_var = strings
    assert actual + "a" == proxy_var + "a"


def test_contains(strings: Objects[str]) -> None:
    actual, _, proxy_var = strings
    assert ("a" in actual) == ("a" in proxy_var)


def test_countOf(strings: Objects[str]) -> None:
    actual, _, proxy_var = strings
    assert actual.count("a") == proxy_var.count("a")


def test_item_access(lists: Objects[list[Any]]) -> None:
    # covers getitem, setitem and delitem
    actual, _, proxy_var = lists
    actual[:1] = [1]
    assert actual == proxy_var
    assert actual[0] is proxy_var[0]
    del actual[0]
    assert actual == proxy_var


@pytest.mark.parametrize(
    "objects",
    chain.from_iterable(
        map(
            lazy_fixture,
            (
                integers_fixture,
                floats_fixture,
                strings_fixture,
                booleans_fixture,
                lists_fixture,
            ),
        )
    ),
)
def test_eq(objects: Objects[object]) -> None:
    actual, _, proxy_var = objects
    assert actual == proxy_var


@integers_and_floats
def test_floordiv(objects: Objects[int | float]) -> None:
    actual, _, proxy_var = objects
    assert isinf(actual) == isinf(proxy_var)
    if not isinf(actual):
        assert actual // 1 == proxy_var // 1


@integers_and_floats
def test_ge(objects: Objects[int | float]) -> None:
    actual, _, proxy_var = objects
    assert (actual >= 1) == (proxy_var >= 1)


def test_gt(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert (actual > 1) == (proxy_var > 1)
    assert not actual > proxy_var  # they are equal


def test_iadd(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual += 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var -= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_iand(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual &= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var &= 0
    actual = mgr.get()
    assert actual == proxy_var


def test_iconcat(strings: Objects[str]) -> None:
    actual, mgr, proxy_var = strings

    actual += "a"
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var += "a"
    actual = mgr.get()
    assert actual == proxy_var


def test_ifloordiv(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual //= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var //= 2
    actual = mgr.get()
    assert actual == proxy_var


def test_ilshift(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual <<= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var <<= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_imod(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual %= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var %= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_imul(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual *= 100
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var *= 0.6
    actual = mgr.get()
    assert actual == proxy_var


@strings_and_lists
def test_index(objects: Objects[str | list[Any]]) -> None:
    actual, _, proxy_var = objects
    if actual:
        element = choice(actual)
        assert actual.index(element) == proxy_var.index(element)


def test_inv(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert ~actual == ~proxy_var


def test_ior(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual |= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var |= 128
    actual = mgr.get()
    assert actual == proxy_var


def test_ipow(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual **= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var **= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_irshift(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual >>= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var >>= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_is_(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    with pytest.raises(AssertionError):
        # this should fail because the objects are not the same
        assert actual is proxy_var


def test_is_not(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual is not proxy_var


def test_isub(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual -= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var += 1
    actual = mgr.get()
    assert actual == proxy_var


def test_itruediv(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual /= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var /= 2
    actual = mgr.get()
    assert actual == proxy_var


def test_ixor(integers: Objects[int]) -> None:
    actual, mgr, proxy_var = integers

    actual ^= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var ^= 1
    actual = mgr.get()
    assert actual == proxy_var


@integers_and_floats
def test_le(objects: Objects[int | float]) -> None:
    actual, _, proxy_var = objects
    assert (actual <= 1) == (proxy_var <= 1)


@strings_and_lists
def test_length_hint(objects: Objects[str | list[Any]]) -> None:
    actual, _, proxy_var = objects
    assert len(actual) == len(proxy_var)


def test_lshift(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual << 1 == proxy_var << 1


@integers_and_floats
def test_lt(objects) -> None:
    actual, _, proxy_var = objects
    assert (actual < 1) == (proxy_var < 1)
    assert not actual < proxy_var  # they are equal
    assert not proxy_var < actual  # they are equal


if np:

    def test_matmul() -> None:
        actual = np.array([[1, 2], [3, 4]])
        mgr = ContextVar("matrix")
        mgr.set(actual)
        proxy_var = lookup_proxy(mgr)
        matrix = [[9, 10], [11, 12]]
        assert ((actual @ matrix) == (proxy_var @ matrix)).all()

    def test_imatmul() -> None:
        actual = np.array([[1, 2], [3, 4]])
        mgr = ContextVar("matrix")
        mgr.set(actual)
        proxy_var = lookup_proxy(mgr)

        actual @= [[5, 6], [7, 8]]  # type: ignore
        mgr.set(actual)
        assert (actual == proxy_var).all()

        proxy_var @= [[9, 10], [11, 12]]
        actual = mgr.get()
        assert (actual == proxy_var).all()


def test_methods(strings: Objects[str], integers: Objects[int]) -> None:
    actual, _, proxy_var = strings
    assert actual.upper() == proxy_var.upper()

    actual, _, proxy_var = integers
    assert actual.bit_length() == proxy_var.bit_length()


def test_mod(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual % 1 == proxy_var % 1


def test_mul(strings: Objects[str]) -> None:
    actual, _, proxy_var = strings
    assert actual * 2 == proxy_var * 2


def test_ne(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert (actual != 1) == (proxy_var != 1)


def test_neg(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert -actual == -proxy_var


def test_not_(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert (not not actual) == (not not proxy_var)


def test_or(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual | 1 == proxy_var | 1


def test_pos(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert +actual == +proxy_var


def test_pow(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual**1 == proxy_var**1


def test_rshift(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual >> 1 == proxy_var >> 1


def test_sub(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual - 1 == proxy_var - 1


def test_truediv(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual / 1 == proxy_var / 1


def test_truth(integers: Objects[int]) -> None:
    # actual truth check is technically faster than bool()
    # but semantically equivalent
    actual, _, proxy_var = integers
    assert bool(actual) == bool(proxy_var)


def test_xor(integers: Objects[int]) -> None:
    actual, _, proxy_var = integers
    assert actual ^ 1 == proxy_var ^ 1


def test_attrgetter() -> None:
    class A:
        def __init__(self, value) -> None:
            self.value = value

    actual = A(1)
    mgr = ContextVar("attrgetter")
    mgr.set(actual)
    proxy_var = lookup_proxy(mgr)

    assert actual.value == proxy_var.value


def test_delitem() -> None:
    actual = [1, 2, 3]
    mgr = ContextVar("delitem")
    mgr.set(actual)
    proxy_var = lookup_proxy(mgr)

    del actual[0]
    mgr.set(actual)
    assert actual == proxy_var


def test_eq_object() -> None:
    actual = object()
    mgr = ContextVar("eq")
    mgr.set(actual)
    proxy_var = lookup_proxy(mgr)

    assert actual == proxy_var
