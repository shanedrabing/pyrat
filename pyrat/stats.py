__all__ = [
    # "cor",
    "cov",
    "dev",
    # "lm",
    # "na_omit",
    # "predict",
    # "rmse",
    # "sd",
    "ss",
    "var",
]


# IMPORTS


import statistics
from pyrat.base import mean, sqrt, is_na, vector, c, NA
from pyrat.closure import inv


# FUNCTIONS


def ss(x):
    return sum(x ** 2)


def dev(x, f=mean):
    return x - f(x)


def var(x, y=None):
    if y is not None:
        return cov(x, y)
    if not isinstance(x, vector):
        x = c(x)
    if len(x) <= 1:
        return NA
    return ss(dev(x)) / (len(x) - 1)


def cov(x, y=None):
    if y is None:
        return var(x)
    if not isinstance(x, vector):
        x = c(x)
    if not isinstance(y, vector):
        y = c(y)
    if len(x) != len(y):
        raise ValueError("vector lengths unequal")
    return sum(dev(x) * dev(y)) / (len(x) - 1)
