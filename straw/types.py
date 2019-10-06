import datetime

import dateutil.parser

from . import base


def value():
    return base.Straw(
        lambda data: data,
        lambda _, value: value)


def const(value):
    return base.Straw(
        lambda _: value,
        lambda data, _: data)


class _Stringlike(object):
    def __call__(self):
        return base.Straw(
            lambda data: str(data),
            lambda _, value: str(value))

    def iso8601(self):
        return base.Straw(
            lambda data: dateutil.parser.parse(data),
            lambda _, value: value.isoformat())

    def unix_timestamp(self):
        return base.Straw(
            lambda data: datetime.datetime.utcfromtimestamp(data),
            lambda _, value: datetime.datetime.timestamp(value)
        )


string = _Stringlike()


def boolean():
    return base.Straw(
        lambda data: bool(data),
        lambda _, value: bool(value))


def number():
    def parse(data):
        if isinstance(data, (int, float)):
            return data

        try:
            return int(data)
        except ValueError:
            return float(data)

    return base.Straw(parse, lambda _, value: parse(value))
