from contextvars import ContextVar
from math import isinf
from random import choice

import pytest
from pytest_lazyfixture import lazy_fixture

from proxyvars import lookup_proxy

try:
    import numpy as np  # type: ignore
except ImportError:
    np = None

integers_and_floats = pytest.mark.parametrize(
    "objects",
    [
        lazy_fixture("integers"),
        lazy_fixture("floats"),
    ],
)

strings_and_lists = pytest.mark.parametrize(
    "objects",
    [
        lazy_fixture("strings"),
        lazy_fixture("lists"),
    ],
)


@integers_and_floats
def test_abs(objects):
    actual, _, proxy_var = objects
    assert abs(actual) == abs(proxy_var)


@integers_and_floats
def test_add(objects):
    actual, _, proxy_var = objects
    assert actual + 1 == proxy_var + 1


def test_and_(integers):
    actual, _, proxy_var = integers
    assert actual & 1 == proxy_var & 1


def test_concat(strings):
    actual, _, proxy_var = strings
    assert actual + "a" == proxy_var + "a"


def test_contains(strings):
    actual, _, proxy_var = strings
    assert ("a" in actual) == ("a" in proxy_var)


def test_countOf(strings):
    actual, _, proxy_var = strings
    assert actual.count("a") == proxy_var.count("a")


def test_item_access(lists):
    # covers getitem, setitem and delitem
    actual, _, proxy_var = lists
    actual[:1] = [1]
    assert actual == proxy_var
    assert actual[0] is proxy_var[0]
    del actual[0]
    assert actual == proxy_var


@pytest.mark.parametrize(
    "objects",
    [
        lazy_fixture("integers"),
        lazy_fixture("floats"),
        lazy_fixture("strings"),
        lazy_fixture("booleans"),
        lazy_fixture("lists"),
    ],
)
def test_eq(objects):
    actual, _, proxy_var = objects
    assert actual == proxy_var


@integers_and_floats
def test_floordiv(objects):
    actual, _, proxy_var = objects
    assert isinf(actual) == isinf(proxy_var)
    if not isinf(actual):
        assert actual // 1 == proxy_var // 1


@integers_and_floats
def test_ge(objects):
    actual, _, proxy_var = objects
    assert (actual >= 1) == (proxy_var >= 1)


def test_gt(integers):
    actual, _, proxy_var = integers
    assert (actual > 1) == (proxy_var > 1)
    assert not actual > proxy_var  # they are equal


def test_iadd(integers):
    actual, mgr, proxy_var = integers

    actual += 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var -= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_iand(integers):
    actual, mgr, proxy_var = integers

    actual &= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var &= 0
    actual = mgr.get()
    assert actual == proxy_var


def test_iconcat(strings):
    actual, mgr, proxy_var = strings

    actual += "a"
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var += "a"
    actual = mgr.get()
    assert actual == proxy_var


def test_ifloordiv(integers):
    actual, mgr, proxy_var = integers

    actual //= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var //= 2
    actual = mgr.get()
    assert actual == proxy_var


def test_ilshift(integers):
    actual, mgr, proxy_var = integers

    actual <<= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var <<= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_imod(integers):
    actual, mgr, proxy_var = integers

    actual %= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var %= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_imul(integers):
    actual, mgr, proxy_var = integers

    actual *= 100
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var *= 0.6
    actual = mgr.get()
    assert actual == proxy_var


@strings_and_lists
def test_index(objects):
    actual, _, proxy_var = objects
    if actual:
        element = choice(actual)
        assert actual.index(element) == proxy_var.index(element)


def test_inv(integers):
    actual, _, proxy_var = integers
    assert ~actual == ~proxy_var


def test_ior(integers):
    actual, mgr, proxy_var = integers

    actual |= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var |= 128
    actual = mgr.get()
    assert actual == proxy_var


def test_ipow(integers):
    actual, mgr, proxy_var = integers

    actual **= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var **= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_irshift(integers):
    actual, mgr, proxy_var = integers

    actual >>= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var >>= 1
    actual = mgr.get()
    assert actual == proxy_var


def test_is_(integers):
    actual, _, proxy_var = integers
    with pytest.raises(AssertionError):
        # this should fail because the objects are not the same
        assert actual is proxy_var


def test_is_not(integers):
    actual, _, proxy_var = integers
    assert actual is not proxy_var


def test_isub(integers):
    actual, mgr, proxy_var = integers

    actual -= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var += 1
    actual = mgr.get()
    assert actual == proxy_var


def test_itruediv(integers):
    actual, mgr, proxy_var = integers

    actual /= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var /= 2
    actual = mgr.get()
    assert actual == proxy_var


def test_ixor(integers):
    actual, mgr, proxy_var = integers

    actual ^= 1
    mgr.set(actual)
    assert actual == proxy_var

    proxy_var ^= 1
    actual = mgr.get()
    assert actual == proxy_var


@integers_and_floats
def test_le(objects):
    actual, _, proxy_var = objects
    assert (actual <= 1) == (proxy_var <= 1)


@strings_and_lists
def test_length_hint(objects):
    actual, _, proxy_var = objects
    assert len(actual) == len(proxy_var)


def test_lshift(integers):
    actual, _, proxy_var = integers
    assert actual << 1 == proxy_var << 1


@integers_and_floats
def test_lt(objects):
    actual, _, proxy_var = objects
    assert (actual < 1) == (proxy_var < 1)
    assert not actual < proxy_var  # they are equal
    assert not proxy_var < actual  # they are equal


if np:

    def test_matmul():
        actual = np.array([[1, 2], [3, 4]])
        mgr = ContextVar("matrix")
        mgr.set(actual)
        proxy_var = lookup_proxy(mgr)
        matrix = [[9, 10], [11, 12]]
        assert ((actual @ matrix) == (proxy_var @ matrix)).all()

    def test_imatmul():
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


def test_methods(strings, integers):
    actual, _, proxy_var = strings
    assert actual.upper() == proxy_var.upper()

    actual, _, proxy_var = integers
    assert actual.bit_length() == proxy_var.bit_length()


def test_mod(integers):
    actual, _, proxy_var = integers
    assert actual % 1 == proxy_var % 1


def test_mul(strings):
    actual, _, proxy_var = strings
    assert actual * 2 == proxy_var * 2


def test_ne(integers):
    actual, _, proxy_var = integers
    assert (actual != 1) == (proxy_var != 1)


def test_neg(integers):
    actual, _, proxy_var = integers
    assert -actual == -proxy_var


def test_not_(integers):
    actual, _, proxy_var = integers
    assert (not not actual) == (not not proxy_var)


def test_or(integers):
    actual, _, proxy_var = integers
    assert actual | 1 == proxy_var | 1


def test_pos(integers):
    actual, _, proxy_var = integers
    assert +actual == +proxy_var


def test_pow(integers):
    actual, _, proxy_var = integers
    assert actual**1 == proxy_var**1


def test_rshift(integers):
    actual, _, proxy_var = integers
    assert actual >> 1 == proxy_var >> 1


def test_sub(integers):
    actual, _, proxy_var = integers
    assert actual - 1 == proxy_var - 1


def test_truediv(integers):
    actual, _, proxy_var = integers
    assert actual / 1 == proxy_var / 1


def test_truth(integers):
    # actual truth check is technically faster than bool()
    # but semantically equivalent
    actual, _, proxy_var = integers
    assert bool(actual) == bool(proxy_var)


def test_xor(integers):
    actual, _, proxy_var = integers
    assert actual ^ 1 == proxy_var ^ 1


def test_attrgetter():
    class A:
        def __init__(self, value):
            self.value = value

    actual = A(1)
    mgr = ContextVar("attrgetter")
    mgr.set(actual)
    proxy_var = lookup_proxy(mgr)

    assert actual.value == proxy_var.value


def test_delitem():
    actual = [1, 2, 3]
    mgr = ContextVar("delitem")
    mgr.set(actual)
    proxy_var = lookup_proxy(mgr)

    del actual[0]
    mgr.set(actual)
    assert actual == proxy_var


def test_eq_object():
    actual = object()
    mgr = ContextVar("eq")
    mgr.set(actual)
    proxy_var = lookup_proxy(mgr)

    assert actual == proxy_var
