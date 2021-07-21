__author__ = "Shane Drabing"
__license__ = "MIT"
__email__ = "shane.drabing@gmail.com"


# MODULE EXPOSURE


__all__ = [
    "catch",
    "get",
    "gettr",
    "got",
    "inv",
    "nest",
    "part",
    "unpack",
]


# FUNCTIONS


def catch(f, err, default=None):
    def catchf(x):
        try:
            return f(x)
        except err:
            return default
    return catchf


def get(key):
    def getf(itr):
        return itr[key]
    return getf


def gettr(key):
    def gettrf(itr):
        return getattr(itr, key)
    return gettrf


def got(itr):
    def gotf(key):
        return itr[key]
    return gotf


def inv(f):
    def invf(x):
        return not f(x)
    return invf


def nest(*fs):
    def nestf(x):
        for f in fs:
            x = f(x)
        return x
    return nestf


def part(f, *args, **kwargs):
    def partf(x):
        return f(x, *args, **kwargs)
    return partf


def unpack(f):
    def unpackf(x):
        return f(*x)
    return unpackf
