__author__ = "Shane Drabing"
__license__ = "MIT"
__email__ = "shane.drabing@gmail.com"


# MODULE EXPOSURE


__all__ = [
    # constants
    "F",
    "Inf",
    "NA",
    "NaN",
    "T",

    # functions
    "acos",
    "asin",
    "atan",
    "c",
    "cos",
    "exp",
    "gextr",
    "gextrall",
    "grep",
    "grepl",
    "gsub",
    "identical",
    "ifelse",
    "is_na",
    "is_none",
    "isiter",
    "isnonstriter",
    "log",
    "match",
    "mean",
    "order",
    "paste",
    "rep",
    "rmax",
    "rmin",
    "seq",
    "sin",
    "sort",
    "sqrt",
    "tan",
    "unique",
    "vector",
    "which",
]


# IMPORTS


import concurrent.futures
import dataclasses
import functools
import itertools
import math
import operator as op
import re
import statistics

from pyrat.closure import catch, get, inv, nest, part


# NA CLASS


@dataclasses.dataclass(frozen=True)
class _NA:
    def __str__(self):
        return "NA"

    __repr__ = __str__
    
    def __bool__(self):
        # for itertools.compress?
        return False


# PSEUDO-CONSTANTS


NA = _NA()
T = True
F = False
Inf = float("inf")
NaN = float("nan")


# FUNCTIONS (GENERAL)


def _identity(x):
    return x


def _is_na_singular(x):
    return isinstance(x, _NA)


def _is_none_singular(x):
    return x is None


def _repeat(x):
    itr = itertools.repeat(x)
    if isnonstriter(x):
        itr = itertools.chain.from_iterable(itr)
    return itr


def _repeat_many(itr):
    try:
        maxlen = max(map(len, itr))
    except ValueError:
        return tuple()
    return tuple(itertools.islice(_repeat(x), maxlen) for x in itr)


def _ifelse_singular(test, yes, no):
    return yes if test else no


def isiter(x):
    return "__iter__" in dir(x)


def isnonstriter(x):
    return isiter(x) and not isinstance(x, str)


# FUNCTIONS (STATISTICS)


def _stat(f, x):
    if not isinstance(x, vector):
        return f(x)
    return x.apply(catch(f, TypeError, NA))


def sqrt(x):
    return _stat(math.sqrt, x)


def exp(x):
    return _stat(math.exp, x)


def sin(x):
    return _stat(math.sin, x)


def cos(x):
    return _stat(math.cos, x)


def tan(x):
    return _stat(math.tan, x)


def asin(x):
    return _stat(math.asin, x)


def acos(x):
    return _stat(math.acos, x)


def atan(x):
    return _stat(math.atan, x)


def log(x, base=math.exp(1)):
    if not isinstance(x, vector):
        return math.log(x, base)
    return x.apply(catch(part(math.log, base), TypeError, NA))


def rmin(*x, na_rm=False):
    x = c(x)
    if not x:
        return Inf
    if na_rm:
        x = x[~is_na(x)]
    elif any(is_na(x)):
        return NA
    return min(x)


def rmax(*x, na_rm=False):
    x = c(x)
    if not x:
        return -Inf
    if na_rm:
        x = x[~is_na(x)]
    elif any(is_na(x)):
        return NA
    return max(x)


def mean(x, na_rm=False):
    if not x:
        return NA
    if na_rm:
        x = x[~is_na(x)]
    elif any(is_na(x)):
        return NA
    return sum(x) / len(x)


# FUNCTIONS (VECTOR MANIPULATION)


def c(*itr):
    vec = vector(c(*x) if isnonstriter(x) else (x,) for x in itr)
    return vector(vec.astype(tuple).reduce(tuple.__add__, tuple()))


def is_na(x):
    if isinstance(x, vector):
        return x.apply(is_na)
    return _is_na_singular(x)


def is_none(x):
    if isinstance(x, vector):
        return x.apply(is_none)
    return _is_none_singular(x)


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


def rep(x=None, times=None, length_out=None, each=None):
    if x is None:
        return
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
    return vector(itertools.islice(cyc, length_out))


def seq(start, end=None, step=1, length_out=None):
    if end is None:
        end = start
        start = 1
    flip = end < start
    if flip:
        start, end = end, start
        
    rng = (end - start)
    if length_out is None:
        nsteps = rng / step
        length_out = math.ceil(nsteps) + (nsteps == int(nsteps))
    else:
        step = (rng / (length_out - 1))
    vec = vector(start + (step * i) for i in range(length_out))
    return vec[::-1] if flip else vec


def sort(itr, key=None, reverse=False):
    return vector(sorted(itr, key=key, reverse=reverse))


def order(itr=None, key=None, reverse=False):
    if itr is None:
        return
    if key is None:
        key = _identity
    srt = sorted(enumerate(itr), key=nest(get(1), key), reverse=reverse)
    ind, _ = zip(*srt)
    return vector(ind)


def paste(*args, sep=" ", collapse=None):
    vecs = tuple(
        (x if isinstance(x, vector) else c(x)).astype(str)
        for x in args
    )
    vec = vector(map(sep.join, zip(*_repeat_many(vecs))))
    if isinstance(collapse, str):
        return collapse.join(vec)
    return vec


def ifelse(test, yes, no):
    return vector(map(_ifelse_singular, test, _repeat(yes), _repeat(no)))


def match(x, table, nomatch=NA):
    if not isinstance(x, vector):
        x = c(x)
    if not isinstance(table, vector):
        table = c(table)
    return vector(x).apply(catch(table.index, ValueError, nomatch))


def which(x):
    if not isinstance(x, vector):
        x = c(x)
    return vector(itertools.compress(range(len(x)), x))


def unique(itr):
    return vector(dict.fromkeys(itr))


# FUNCTIONS (REGEX)


def grepl(pattern, x):
    if not isinstance(pattern, re.Pattern):
        pattern = re.compile(pattern)
    return ~is_none(x.apply(pattern.search))


def grep(pattern, x):
    return which(grepl(pattern, x))


def gsub(pattern, repl, x, count=None):
    if not isinstance(pattern, re.Pattern):
        pattern = re.compile(pattern)
    if count:
        return x.apply(lambda s: pattern.sub(repl, s, count))
    return x.apply(lambda s: pattern.sub(repl, s))


def gextr(pattern, x):
    if not isinstance(pattern, re.Pattern):
        pattern = re.compile(pattern)
    return x.pipe(pattern.search, catch(re.Match.group, TypeError, NA))


def gextrall(pattern, x):
    if not isinstance(pattern, re.Pattern):
        pattern = re.compile(pattern)
    return x.pipe(pattern.findall, c)


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


# VECTOR CLASS


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
        f = catch(round, TypeError, NA)
        if ndigits is None:
            return vector(map(f, self))
        return vector(map(f, self, (ndigits,) * len(self)))

    def reduce(self, f, init=None):
        if init is None:
            return functools.reduce(f, self)
        return functools.reduce(f, self, init)

    def accumulate(self, f):
        return vector(itertools.accumulate(self, f))

    def filter(self, f, invert=False):
        if invert:
            return vector(filter(inv(f), self))
        return vector(filter(f, self))

    def astype(self, t):
        if str(type(t)) != "<class 'type'>":
            raise Exception("use vector.apply for functions")
        return self.apply(t)

    def apply(self, f, *args):
        f = catch(f, TypeError, NA)
        return vector(map(f, self, *args))

    def thread(self, f, *args):
        f = catch(f, TypeError, NA)
        with concurrent.futures.ThreadPoolExecutor() as exe:
            return vector(exe.map(f, self, *args))

    def proc(self, f, *args):
        if f.__name__ == "<lambda>":
            raise Exception("can't use a lambda here")
        f = catch(f, TypeError, NA)
        with concurrent.futures.ProcessPoolExecutor() as exe:
            return vector(exe.map(f, self, *args))

    def tapply(self, index, f):
        rng = seq(0, len(self))
        i = order(index)
        return {
            k: f(self[v])
            for k, v in itertools.groupby(rng[i], index.__getitem__)
        }

    def pipe(self, *fs):
        x = self
        for f in fs:
            x = vector(map(f, x))
        return x


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
