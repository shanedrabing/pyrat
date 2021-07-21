__author__ = "Shane Drabing"
__license__ = "MIT"
__email__ = "shane.drabing@gmail.com"


# MODULE EXPOSURE


__all__ = [
    "assert_eq",
    "assert_is",
    "assert_identical",
    "assert_not_identical",
    "none",
]


# IMPORTS


from pyrat.base import identical, vector


# FUNCTIONS


def assert_eq(a, b):
    test = (a == b)
    if isinstance(test, vector):
        raise ValueError("assert_eq is incorrect for vectors")
    assert test, "%s != %s" % tuple(map(repr, (a, b)))


def assert_identical(a, b):
    test = identical(a, b)
    assert test, "%s != %s" % tuple(map(repr, (a, b)))


def assert_not_identical(a, b):
    test = not identical(a, b)
    assert test, "%s == %s" % tuple(map(repr, (a, b)))


def none(x):
    return not any(x)


# SCRIPT


if __name__ == "__main__":
    import itertools
    import operator

    from pyrat.base import *
    from pyrat.closure import *

    # VARIABLES

    t12 = (1, 2)
    t123 = (1, 2, 3)
    v12 = c(1, 2)
    v123 = c(1, 2, 3)
    v213 = c(2, 1, 3)

    # VECTOR TESTS
    
    # identical ensures that tuples are truly the same
    assert_identical(t123, t123)
    assert_not_identical(t123, t12)

    # identical ensures that vectors are truly the same
    assert_identical(v123, v123)
    assert_not_identical(v123, v12)

    # vector is a class...
    assert_identical(c(1, 2, 3), v123)
    assert_identical(vector([1, 2, 3]), v123)
    assert_identical(vector((1, 2, 3)), v123)

    # ...with vectorized operators...
    # math operators
    assert_identical(-v123, c(-1, -2, -3))
    assert_identical(abs(-v123), v123)
    assert_identical(v123 + v123, c(2, 4, 6))
    assert_identical(v123 * v123, c(1, 4, 9))
    assert_identical(v123 - v123, rep(0, 3))
    assert_identical(v123 / v123, rep(1.0, 3))
    assert_identical(v123 // v123, rep(1, 3))
    assert_identical(v123 ** v123, c(1, 4, 27))

    # equivalence operators
    assert all(v123 == v123)
    assert all(v123 <= v123)
    assert all(v123 >= v123)
    assert none(v123 != v123)
    assert none(v123 < v123)
    assert none(v123 > v123)

    # __invert__ has a new usage (like ! from R)
    assert none(~(v123 == v123))
    assert all(~(v123 != v123))

    # __eq__ recycling weirdness (gives warning in R)
    assert_identical(v123 == v12, c(True, True, False))
    assert_identical(c(1, 2, 1) == v12, c(True, True, True))

    # __getitem__
    assert_identical(v123[0], 1)
    assert_identical(v123[0, 1], v12)
    assert_identical(v123[(0, 1)], v12)
    assert_identical(v123[[0, 1]], v12)
    assert_identical(v123[c(0, 1)], v12)
    assert_identical(v123[1, 0, 1], c(2, 1, 2))
    assert_identical(v123[1, NA, 1], c(2, NA, 2))
    assert_identical(v123[:2], v12)

    # __getitem__ with casting
    assert_identical(v123.astype(str)[0], "1")
    assert_identical(v123.astype(str)[c(0, 1)], v12.astype(str))

    # no named vectors!  :-(
    # tuple is immutable, must override __new__,
    # but cannot set attributes on tuples anyways

    # ...and some cool methods
    assert_identical((v123 + 0.1).round(), v123)
    assert_identical(v123.reduce(operator.add), sum(v123))
    assert_identical(v123.accumulate(operator.add), c(1, 3, 6))
    assert_identical(v123.filter(lambda x: x < 3), v12)
    assert_identical(v123.filter(lambda x: x < 3, invert=True), c(3))
    assert_eq(v123.tapply(v123 % 2 == 0, c), {False: c(1, 3), True: c(2)})
    assert_identical(v123.astype(str), c("1", "2", "3"))

    # different kinds of apply methods,
    # which can take multiple inputs
    assert_identical(v123.apply(int.__mul__, v123), v123 * v123)
    assert all(v123.astype(str).apply(str.isdigit))
    assert all(v123.astype(str).thread(str.isdigit))
    # assert all(v123.astype(str).proc(str.isdigit))

    # a ridiculuous example
    tmp = (
        v123
        .astype(str)
        .apply(str.replace, v123.astype(str), v213.astype(str))
        .astype(int)
    )
    assert_identical(tmp, v213)

    # pipe method can take multiple functions,
    # to continuously transform the results
    assert_identical(
        v123.pipe(str, ord, part(int.__add__, 1), chr, int),
        c(2, 3, 4)
    )

    # BASE TESTS

    # c(ombine) will make new vectors,
    # or flatten vectors for concatenation
    assert_identical(c(), vector())
    assert_identical(c(1, c(2, 3)), c(1, 2, 3))

    # is_na is both singular and multiple,
    # NA is not None
    assert_eq(is_na(NA), True)
    assert_eq(is_na(None), False)
    assert_identical(is_na(c(NA, None)), c(True, False))

    # is_none is both singular and multiple,
    # None is not NA,
    # this is a little different than is.null in R
    assert_eq(is_none(None), True)
    assert_eq(is_none(NA), False)
    assert_identical(is_none(c(None, NA)), c(True, False))

    "identical",
    "is_na",
    "isiter",
    "isnonstriter",
    "NA",
    "order",
    "rep",
    "seq",
    "vector",
