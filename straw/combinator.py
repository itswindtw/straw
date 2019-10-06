import copy
import functools

from . import base


def field(key, straw):
    def pull(data):
        return straw.pull(data[key])

    def push(data, value):
        data = copy.deepcopy(data or {})
        data[key] = straw.push(data.get(key), value)
        return data

    return base.Straw(pull, push)


def at(keys, straw):
    def func(straw, key):
        return field(key, straw)
    return functools.reduce(
        lambda straw, key: field(key, straw), keys[::-1], straw)


def index(idx, straw):
    def pull(data):
        return straw.pull(data[idx])

    def push(data, value):
        data = copy.deepcopy(data or [])

        i = idx - len(data) + 1
        while i > 0:
            data.append(None)
            i -= 1

        data[idx] = straw.push(data[idx], value)
        return data

    return base.Straw(pull, push)


def spliter(merge, split, straw_list):
    def pull(data):
        return merge([s.pull(data) for s in straw_list])

    def push(data, value):
        def func(result, straw_value):
            straw, value = straw_value
            return straw.push(result, value)

        return functools.reduce(func, zip(straw_list, split(value)), data)

    return base.Straw(pull, push)
