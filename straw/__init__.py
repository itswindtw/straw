import functools

from .base import StrawPair  # noqa
from .types import *  # noqa
from .combinator import *  # noqa


def squeeze(straw_pair_list, source):
    def func(result, straw_pair):
        from_straw, to_straw = straw_pair
        value = straw_pair.start.pull(source)
        return straw_pair.end.push(result, value)

    return functools.reduce(func, straw_pair_list, {})
