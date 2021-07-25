__all__ = [
    "cov",
    "dev",
    "median",
    "na_omit",
    "ss",
    "var",
]


# IMPORTS


import statistics
from pyrat.base import mean, sqrt, is_na, vector, c, NA, isvector, sort
from pyrat.closure import inv


# FUNCTIONS


def na_omit(x):
    if not isvector(x):
        x = c(x)
    return x[~is_na(x)]


def median(x, na_rm=False):
    if not isvector(x):
        x = c(x)
    if na_rm:
        x = na_omit(x)
    elif any(is_na(x)):
        return NA
    srt = sort(x)
    n = len(srt)
    i = n // 2
    if n % 2 == 0:
        return sum(srt[i - 1:i + 1]) / 2
    return srt[i]


def ss(x, na_rm=False):
    if not isvector(x):
        x = c(x)
    if na_rm:
        x = na_omit(x)
    elif any(is_na(x)):
        return NA
    return sum(x ** 2)


def dev(x, f=mean, na_rm=False):
    if not isvector(x):
        x = c(x)
    if na_rm:
        x = na_omit(x)
    elif any(is_na(x)):
        return NA
    return x - f(x)


def var(x, y=None, na_rm=False):
    if y is not None:
        return cov(x, y)
    if not isvector(x):
        x = c(x)
    if na_rm:
        x = na_omit(x)
    elif any(is_na(x)):
        return NA
    if len(x) <= 1:
        return NA
    return ss(dev(x)) / (len(x) - 1)


def cov(x, y=None, na_rm=False):
    if y is None:
        return var(x)
    if not isvector(x):
        x = c(x)
    if not isvector(y):
        y = c(y)
    if na_rm:
        x = na_omit(x)
        y = na_omit(y)
    elif any(is_na(x)) or any(is_na(y)):
        return NA
    if len(x) != len(y):
        raise ValueError("vector lengths unequal")
    return sum(dev(x) * dev(y)) / (len(x) - 1)
