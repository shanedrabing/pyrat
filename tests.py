__author__ = "Shane Drabing"
__license__ = "MIT"
__email__ = "shane.drabing@gmail.com"


# MODULE EXPOSURE


__all__ = [
    "assert_eq",
    "assert_identical",
    "assert_is",
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


def assert_is(a, b):
    test = (a is b)
    assert test, "%s is not %s" % tuple(map(repr, (a, b)))


def assert_error(f, err):
    try:
        f()
    except err:
        pass


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
    import operator

    from pyrat.base import *
    from pyrat.closure import *
    from pyrat.stats import *

    # VARIABLES

    t12 = (1, 2)
    t123 = (1, 2, 3)
    v12 = c(1, 2)
    v123 = c(1, 2, 3)
    v213 = c(2, 1, 3)
    ptrn = r"[Aa]"
    vstr = c("python", "a rat", "pirate")

    # VECTOR TESTS
    
    # empty calls to identical
    assert_error(lambda: identical(), TypeError)
    assert_error(lambda: identical(None), TypeError)
    assert identical(None, None)

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

    # ...some tuple methods...
    assert_eq(v123.index(1), 0)
    assert_eq(v123.count(1), 1)

    # ...and some cool methods
    assert_identical((v123 + 0.1).round(), v123)
    assert_identical(v123.reduce(operator.add), sum(v123))
    assert_identical(v123.accumulate(operator.add), c(1, 3, 6))
    assert_identical(v123.filter(lambda x: x < 3), v12)
    assert_identical(v123.filter(lambda x: x < 3, invert=True), c(3))
    assert_eq(v123.tapply(v123 % 2 == 0, c), {False: c(1, 3), True: c(2)})
    assert_identical(v123.astype(str), c("1", "2", "3"))

    # transform works on the whole vector
    assert_identical(v213.transform(sort), v123)
    assert_identical(v213.sort(), v123)

    # different kinds of apply methods,
    # which can take multiple inputs
    assert_identical(v123.apply_map(int.__mul__, v123), v123 * v123)
    assert all(v123.astype(str).apply(str.isdigit))
    assert all(v123.astype(str).apply_map(str.isdigit))
    assert all(v123.astype(str).thread(str.isdigit))
    assert all(v123.astype(str).thread_map(str.isdigit))
    # assert all(v123.astype(str).proc_map(str.isdigit))

    # apply partial function
    assert_identical(
        vstr.apply(str.split, " "),
        vector((["python"], ["a", "rat"], ["pirate"]))
    )

    # a ridiculuous example
    tmp = (
        v123
        .astype(str)
        .apply_map(str.replace, v123.astype(str), v213.astype(str))
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

    # na_safe makes a function safe to use with NAs
    assert_eq(na_safe(round)(NA), NA)

    # c(ombine) will make new vectors,
    # or flatten vectors for concatenation
    assert_identical(c(), vector())
    assert_identical(c(1, c(2, 3)), c(1, 2, 3))

    # isiter: is the object iterable?
    assert all(map(isiter, (dict(), list(), set(), str(), tuple())))
    assert none(map(isiter, (bool(), complex(), float(), int())))

    # isnonstriter: is it a non-str iterable?
    assert all(map(isnonstriter, (dict(), list(), set(), tuple())))
    assert none(map(isnonstriter, (bool(), complex(), float(), int(), str())))

    # is_na is both singular and multiple,
    # NA is not None
    assert_error(is_na, TypeError)
    assert_eq(is_na(NA), True)
    assert_eq(is_na(None), False)
    assert_identical(is_na(c(NA, None)), c(True, False))

    # any_na is both singular and multiple,
    assert_error(is_na, TypeError)
    assert_eq(any_na(NA), True)
    assert_eq(any_na(None), False)
    assert_eq(any_na(c(NA, None)), True)

    # is_none is both singular and multiple,
    # None is not NA,
    # this is a little different than is.null in R
    assert_error(is_none, TypeError)
    assert_eq(is_none(None), True)
    assert_eq(is_none(NA), False)
    assert_identical(is_none(c(None, NA)), c(True, False))

    # rep can repeat a vector
    assert_is(rep(), None)
    assert_identical(rep(0, 2), c(0, 0))
    assert_identical(rep("hi", 2), c("hi", "hi"))
    assert_identical(rep(v12), v12)
    assert_identical(rep(v12, times=2), c(v12, v12))
    assert_identical(rep(v12, times=2), rep(v12, 4, 4))
    assert_identical(rep(v12, each=2), c(1, 1, 2, 2))
    assert_identical(rep(v12, each=3, length_out=4), c(1, 1, 1, 2))

    # seq is used for making ranges,
    # it is inclusive, unlike Python's range
    vec = c(0.00, 0.25, 0.50, 0.75, 1.00)
    assert_identical(seq(3), v123)
    assert_identical(seq(0), c(1, 0))
    assert_identical(seq(0, 9), c(range(10)))
    assert_identical(seq(0, 1, 0.25), vec)
    assert_identical(seq(1, 0, 0.25), vec[::-1])
    assert_identical(seq(0, 1, length_out=5), vec)
    assert_identical(seq(3, 1), c(3, 2, 1))

    # sort returns a sorted vector
    assert_error(sort, TypeError)
    assert_identical(sort(v213), v123)

    # order returns the sorted indices based on the data
    assert_is(order(), None)
    assert_identical(order(v213), c(1, 0, 2))
    assert_identical(v213[order(v213)], sort(v213))

    # paste is useful for joining str vectors...
    assert_identical(paste(), vector())
    assert_identical(paste(0), c("0"))
    assert_identical(paste(0, 1), c("0 1"))
    assert_identical(paste(c(0, 1)), c("0", "1"))
    assert_identical(paste(0, c(1, 1)), c("0 1", "0 1"))

    # ...use the collapse argument to return a str
    assert_identical(paste(collapse="."), "")
    assert_identical(paste(0, 1, collapse="."), "0 1")
    assert_identical(paste(c(0, 1), collapse="."), "0.1")
    assert_identical(paste(0, c(1, 1), collapse="."), "0 1.0 1")

    # ifelse works along a vector
    assert_error(ifelse, TypeError)
    assert_identical(v123 > 1, c(False, True, True))
    assert_identical(ifelse(v123 > 1, v123, NA), c(NA, 2, 3))
    assert_identical(ifelse(v123 > 1, 1, 0), c(0, 1, 1))

    # match up a vector with an index,
    # NA if not found in index
    assert_error(match, TypeError)
    assert_error(lambda: match(v123), TypeError)
    assert_identical(match(v123, 0), rep(NA, 3))
    assert_identical(match(v123, 0, "hi"), rep("hi", 3))
    assert_identical(match(v123, 1), c(0, NA, NA))
    assert_identical(match(1, seq(3, 1)), c(2))
    assert_identical(match(v12, v123), c(0, 1))
    assert_identical(match(v123, v12), c(0, 1, NA))
    assert_identical(match(c(1, 2, NA), c(1, NA)), c(0, NA, 1))

    # which gives the indices of True values
    assert_error(which, TypeError)
    assert_identical(which(True), c(0))
    assert_identical(which(v123 > 1), c(1, 2))
    assert_identical(which(c(True, NA, False, True)), c(0, 3))

    # unique dedupes a vector
    assert_error(which, TypeError)
    assert_identical(unique(rep(v213, times=2)), v213)
    assert_identical(unique(rep(v213, each=2)), v213)
    assert_identical(unique(c(1, NA, 1, NA, 2)), c(1, NA, 2))

    # grepl
    assert_error(grepl, TypeError)
    assert_identical(grepl(ptrn, vstr), c(False, True, True))

    # grep
    assert_error(grep, TypeError)
    assert_identical(grep(ptrn, vstr), c(1, 2))

    # gsub
    assert_error(gsub, TypeError)
    assert_identical(gsub(ptrn, "", vstr), c("python", " rt", "pirte"))
    assert_identical(gsub(ptrn, "", vstr, 1), c("python", " rat", "pirte"))

    # gextr
    assert_error(gextr, TypeError)
    assert_identical(gextr(ptrn, vstr), c(NA, "a", "a"))

    # gextrall
    assert_error(gextrall, TypeError)
    assert_identical(gextrall(ptrn, vstr), vector((c(), rep("a", 2), c("a"))))

    # sqrt is a vectorized sqrt function
    assert_error(sqrt, TypeError)
    assert_eq(sqrt(4), 2)
    assert_identical(sqrt(c(1, NA, 4)).round(), c(1, NA, 2))
    assert_identical(sqrt(v123).round(6), (v123 ** (1 / 2)).round(6))

    # mean (you know this one)
    assert_error(mean, TypeError)
    assert_identical(mean(c()), NA)
    assert_identical(mean(c(1, 2)), 1.5)
    assert_identical(mean(c(1, 2, NA)), NA)
    assert_identical(mean(c(1, 2, NA), na_rm=True), 1.5)

    # rmin
    assert_eq(rmin(), Inf)
    assert_eq(rmin(1, c(NA, 2)), NA)
    assert_eq(rmin(1, NA, 2, na_rm=True), 1)

    # rmax
    assert_eq(rmax(), -Inf)
    assert_eq(rmax(1, c(NA, 2)), NA)
    assert_eq(rmax(1, NA, 2, na_rm=True), 2)

    # exp
    assert_error(exp, TypeError)
    assert_eq(exp(0), 1)
    assert_identical(exp(c(0, NA)).astype(int), c(1, NA))

    # log
    assert_error(log, TypeError)
    assert_eq(log(1), 0)
    assert_identical(log(c(1, NA)).astype(int), c(0, NA))

    # sin
    assert_error(sin, TypeError)
    assert_eq(sin(0), 0)
    assert_identical(sin(c(0, NA)), c(0.0, NA))
    
    # tan
    assert_error(tan, TypeError)
    assert_eq(tan(0), 0)
    assert_identical(tan(c(0, NA)), c(0.0, NA))
    
    # cos
    assert_error(cos, TypeError)
    assert_eq(cos(0), 1)
    assert_identical(cos(c(0, NA)), c(1.0, NA))
    
    # acos
    assert_error(acos, TypeError)
    assert_eq(acos(1), 0)
    assert_identical(acos(c(1, NA)), c(0.0, NA))
    
    # asin
    assert_error(asin, TypeError)
    assert_eq(asin(0), 0)
    assert_identical(asin(c(0, NA)), c(0.0, NA))
    
    # atan
    assert_error(atan, TypeError)
    assert_eq(atan(0), 0)
    assert_identical(atan(c(0, NA)), c(0.0, NA))

    # STATS TESTS

    # na_omit
    assert_error(na_omit, TypeError)
    assert_identical(na_omit(0), c(0))
    assert_identical(na_omit(NA), c())
    assert_identical(na_omit(c(1, 2, NA)), v12)

    # median
    assert_error(median, TypeError)
    assert_identical(median(0), 0)
    assert_identical(median(NA), NA)
    assert_identical(median(v12), 1.5)
    assert_identical(median(v123), 2)
    assert_identical(median(c(1, 2, NA)), NA)
    assert_identical(median(c(1, 2, NA), na_rm=True), 1.5)

    # ss, sum of squares
    assert_error(ss, TypeError)
    assert_eq(ss(0), 0)
    assert_eq(ss(c(0)), 0)
    assert_eq(ss(v123), 14)
    assert_eq(ss(c(1, 2, NA)), NA)
    assert_eq(ss(c(1, 2, NA), na_rm=True), 5)

    # dev(iance)
    assert_error(dev, TypeError)
    assert_identical(dev(v123).astype(int), c(-1, 0, 1))
    assert_identical(dev(v123, median).astype(int), c(-1, 0, 1))
    assert_identical(dev(c(1, 2, 3, NA)), NA)
    assert_identical(dev(c(1, 2, 3, NA), na_rm=True), c(-1.0, 0.0, 1.0))

    # var(iance)
    assert_error(var, TypeError)
    assert_eq(var(0), NA)
    assert_eq(var(c(0)), NA)
    assert_eq(var(v123), 1)
    assert_eq(var(v123, v213), 0.5)
    assert_eq(var(c(1, 2, NA)), NA)
    assert_eq(var(c(1, 2, NA), na_rm=True), 0.5)
    assert_error(lambda: var(v123, v12), ValueError)

    # sd, standard deviation
    assert_error(sd, TypeError)
    assert_eq(sd(0), NA)
    assert_eq(sd(v123), 1)
    assert_eq(sd(c(1, 2, 3, NA)), NA)
    assert_eq(sd(c(1, 2, 3, NA), na_rm=True), 1)

    # cov(ariance)
    assert_error(cov, TypeError)
    assert_eq(cov(0), NA)
    assert_eq(cov(c(0)), NA)
    assert_eq(cov(v123), 1)
    assert_eq(cov(v123, v213), 0.5)
    assert_eq(cov(c(1, 2, NA)), NA)
    assert_eq(cov(c(1, 2, NA), na_rm=True), 0.5)
    assert_error(lambda: cov(v123, v12), ValueError)

    # cor(relation)
    assert_error(cor, TypeError)
    assert_eq(cor(v123, v123), 1)
    assert_eq(cor(v123, v213), 0.5)
    assert_eq(cor(v123, c(1, 2, 3, NA)), NA)
    assert_eq(cor(v123, c(1, 2, 3, NA), na_rm=True), 1)

    # mad, median absolute deviation
    assert_error(mad, TypeError)
    assert_eq(mad(0), 0)
    assert_eq(mad(NA), NA)
    assert_eq(mad(v123), 1.4826)
    assert_eq(mad(v123, constant=1), 1)
    assert_eq(mad(c(NA, v123)), NA)
    assert_eq(mad(c(NA, v123), na_rm=True), 1.4826)
