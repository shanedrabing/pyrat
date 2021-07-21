__author__ = "Shane Drabing"
__license__ = "MIT"
__email__ = "shane.drabing@gmail.com"


# MODULE EXPOSURE


__all__ = [
    "c",
    "flatten",
    "identical",
    "is_na",
    "isiter",
    "isnonstriter",
    "NA",
    "order",
    "rep",
    "seq",
    "vector",
]


# IMPORTS


import math
import functools
import itertools
import operator as op
import concurrent.futures

from pyrat.closure import part, get, nest


# FUNCTIONS (GENERAL)


def _identity(x):
    return x


def _is_na_singular(x):
    return isinstance(x, _NA)
    return itr


def _consume_n(itr, n):
    itr = iter(itr)
    return (next(itr) for _ in range(n))


def _repeat(x):
    itr = itertools.repeat(x)
    if isnonstriter(x):
        itr = itertools.chain.from_iterable(itr)


def isiter(x):
    return "__iter__" in dir(x)


def isnonstriter(x):
    return isiter(x) and not isinstance(x, str)


# FUNCTIONS (VECTOR MANIPULATION)


def flatten(itr):
    vec = vector(flatten(x) if isnonstriter(x) else (x,) for x in itr)
    return vector(vec.astype(tuple).reduce(tuple.__add__, tuple()))


def c(*args):
    return flatten(args)


def is_na(x):
    if isinstance(x, vector):
        return x.apply(is_na)
    return _is_na_singular(x)


def identical(x, y):
    xt, yt = map(type, (x, y))
    if not xt == yt:
        return False
    xi, yi = map(isnonstriter, (x, y))
    if not xi == yi:
        return False
    if not xi:
        return x == y
    if not len(x) == len(y):
        return False
    return all(map(identical, x, y))


def rep(x, times=None, length_out=None, each=None):
    if not isnonstriter(x):
        x = c(x)
    if each is None:
        each = 1
    if times is None:
        times = 1
    if length_out is None:
        length_out = len(x) * times * each
    itr = x if isnonstriter(x) else c(x)
    gen = map(part(itertools.repeat, each), itr)
    chn = itertools.chain.from_iterable(gen)
    cyc = itertools.cycle(chn)
    return vector(_consume_n(cyc, length_out))


def seq(start, end=None, step=1, length_out=None):
    if end is None:
        end = start
        start = 1
    rng = (end - start)
    if length_out is None:
        nsteps = rng / step
        length_out = math.ceil(nsteps) + (nsteps == int(nsteps))
    else:
        step = (rng / (length_out - 1))
    return vector(start + (step * i) for i in range(length_out))


def order(itr, key=None, reverse=False):
    if key is None:
        key = _identity
    srt = sorted(enumerate(itr), key=nest(get(1), key), reverse=reverse)
    ind, _ = zip(*srt)
    return vector(ind)


# FUNCTIONS (VECTOR LOADING)


def _nanot(x):
    if _is_na_singular(x):
        return NA
    return not x


def _operate(f, flip=False, singular=False):
    if singular:
        def operatef(self):
            return vector(map(f, self))
    elif flip:
        def operatef(self, other):
            return vector(map(f, _repeat(other), self))
    else:
        def operatef(self, other):
            return vector(map(f, self, _repeat(other)))
    return operatef


# CLASSES


class _NA:
    def __str__(self):
        return "NA"
    
    __repr__ = __str__
    
    def __getattr__(self, *args):
        pass
    
    def __setattr__(self, *args):
        pass


class vector(tuple):
    def __repr__(self):
        return "c" + super().__repr__()

    def __neg__(self):
        # get pylint to shut up
        return vector(map(op.neg, self))

    def __invert__(self):
        return vector(map(_nanot, self))

    def __getitem__(self, i):
        if _is_na_singular(i):
            return NA
        if isinstance(i, slice):
            return vector(super().__getitem__(i))

        try:
            return super().__getitem__(i)
        except TypeError as err:
            if isiter(i):
                i = tuple(i)
                t = type(next(iter(i)))
                if t is bool:
                    return vector(itertools.compress(self, i))
                return vector(map(self.__getitem__, i))
            raise err

    def round(self, ndigits=None):
        if ndigits is None:
            return vector(map(round, self))
        return vector(map(round, self, (ndigits,) * len(self)))

    def reduce(self, f, init=None):
        if init is None:
            return functools.reduce(f, self)
        return functools.reduce(f, self, init)

    def accumulate(self, f):
        return vector(itertools.accumulate(self, f))

    def filter(self, f):
        return vector(filter(f, self))

    def apply(self, f, *args):
        return vector(map(f, self, *args))

    def tapply(self, index, f):
        rng = seq(0, len(self))
        i = order(index)
        return {
            k: f(self[v])
            for k, v in itertools.groupby(rng[i], index.__getitem__)
        }

    def astype(self, t):
        if str(type(t)) != "<class 'type'>":
            raise Exception("use vector.apply for functions")
        return self.apply(t)

    def thread(self, f, *args):
        with concurrent.futures.ThreadPoolExecutor() as exe:
            return vector(exe.map(f, self, *args))

    def proc(self, f, *args):
        if f.__name__ == "<lambda>":
            raise Exception("can't use a lambda here")
        with concurrent.futures.ProcessPoolExecutor() as exe:
            return vector(exe.map(f, self, *args))



# CLASS INSTANCES (WEIRD)


NA = _NA()


# CLASS LOADING (VECTOR, MUST RUN)


singular = (
    op.abs,
    op.neg,
    op.pos,
)

multiple = (
    op.add,
    op.eq,
    op.floordiv,
    op.ge,
    op.gt,
    op.le,
    op.lt,
    op.mod,
    op.mul,
    op.ne,
    op.pow,
    op.sub,
    op.truediv,
    op.xor,
)

for f in singular:
    lname = "__{}__".format(f.__name__)
    setattr(vector, lname, _operate(f, singular=True))

for f in multiple:
    lname = "__{}__".format(f.__name__)
    rname = "__r{}__".format(f.__name__)
    setattr(vector, lname, _operate(f))
    setattr(vector, rname, _operate(f, flip=True))
