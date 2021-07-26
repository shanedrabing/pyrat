__all__ = [
    "auto_cast",
    "head",
    "read_csv",
    "struct",
    "tail",
    "try_cast",
]


# IMPORTS


import csv

from pyrat.base import c, isiter, vector
from pyrat.closure import get, unpack


# FUNCTIONS (GENERAL)


def _type_str(x):
    return str(type(x)).split("'")[1]


def head(x, n=6):
    if isiter(x):
        return x[:n]


def tail(x, n=6):
    if isiter(x):
        return x[-n:]


def try_cast(t, x):
    try:
        return t(x)
    except ValueError:
        return


# FUNCTIONS (READ-CSV, DOL MANIPULATION)


def _lod_to_dol(itr):
    dct = dict()
    for x in itr:
        for k, v in x.items():
            try:
                dct[k] += v,
            except KeyError:
                dct[k] = v,
    return dct


def auto_cast(itr):
    x = itr[0]
    t = str

    types = (str, float, int)
    dct = dict(zip(types, len(types) * (True,)))

    for x in itr:
        if try_cast(float, x) is None:
            dct[float] = False
        elif try_cast(int, x) != float(x):
            dct[int] = False

    for t in types:
        if not dct[t]:
            break
        ty = t

    return tuple(map(ty, itr))


def read_csv(filename):
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {
            k: vector(auto_cast(v))
            for k, v in _lod_to_dol(reader).items()
        }


def struct(dct, echo=True):
    k, v = map(vector, zip(*dct.items()))
    k_pad = max(k.apply(len))
    keys = k.apply(str.rjust, k_pad)

    t = v.apply(get(0)).apply(_type_str)
    t_pad = max(t.apply(len))
    types = t.apply(str.ljust, t_pad)

    peek = v.apply(lambda x: ", ".join(c(x[:10]).apply(str)))

    rows = vector(zip(keys, types, peek))
    out = "\n".join(rows.apply(unpack("{} : {}  {} ...".format)))

    if echo:
        print(out)
    return out
