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

    # __eq__ recycling weirdness (warning in R)
    assert_identical(v123 == v12, c(True, True, False))
    assert_identical(c(1, 2, 1) == v12, c(True, True, True))

    # __getitem__
    assert_identical(v123[0], 1)
    assert_identical(v123[0, 1], v12)
    assert_identical(v123[(0, 1)], v12)
    assert_identical(v123[[0, 1]], v12)
    assert_identical(v123[c(0, 1)], v12)
    assert_identical(v123[:2], v12)
    
    # __getitem__ with casting
    assert_identical(v123.astype(str)[0], "1")
    assert_identical(v123.astype(str)[c(0, 1)], v12.astype(str))

    # no named vectors!  :-(

    # ...and some cool methods
    assert_identical((v123 + 0.1).round(), v123)
    assert_identical(v123.reduce(operator.add), sum(v123))
    assert_identical(v123.accumulate(operator.add), c(1, 3, 6))
    assert_identical(v123.filter(lambda x: x < 3), v12)
    assert_eq(v123.tapply(v123 % 2 == 0, c), {False: c(1, 3), True: c(2)})
    assert_identical(v123.astype(str), c("1", "2", "3"))

    # different kinds of apply methods
    assert all(v123.astype(str).apply(str.isdigit))
    assert all(v123.astype(str).thread(str.isdigit))
    # assert all(v123.astype(str).proc(str.isdigit))

    # no pipe method! :-(
