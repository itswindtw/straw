import unittest
import re

import straw


class TestCase(unittest.TestCase):
    def perform(self, specs, source, expected):
        def assertEqual(actual, expected):
            if isinstance(actual, dict) and isinstance(expected, dict):
                self.assertDictEqual(actual, expected)
            else:
                self.assertEqual(actual, expected)

        actual = straw.squeeze(specs, source)
        assertEqual(actual, expected)

        reversed_specs = [straw.StrawPair(s.end, s.start) for s in specs]
        actual = straw.squeeze(reversed_specs, expected)
        assertEqual(actual, source)


class StrawBasicTestCase(TestCase):
    def test_basic(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.field("a", straw.number()),
                    straw.field("upstream_a", straw.number())
                ),
                straw.StrawPair(
                    straw.field("b", straw.number()),
                    straw.field("upstream_b", straw.number())
                ),
            ],
            {
                "a": 1,
                "b": 2,
            },
            {
                "upstream_a": 1,
                "upstream_b": 2,
            }
        )

    def test_nested_fields(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.field(
                        "a",
                        straw.field(
                            "b",
                            straw.field(
                                "c",
                                straw.number()))),
                    straw.field("abc", straw.number())),
            ],
            {'a': {'b': {'c': 42}}},
            {'abc': 42},
        )

    def test_complex_nested_fields(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.field(
                        "a",
                        straw.field(
                            "b",
                            straw.field(
                                "c",
                                straw.number()))),
                    straw.field("ab", straw.field("c", straw.number()))),
            ],
            {'a': {'b': {'c': 42}}},
            {'ab': {'c': 42}},
        )

    def test_at(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.at(["a", "b", "c"], straw.number()),
                    straw.at(["ab", "c"], straw.number())),
            ],
            {'a': {'b': {'c': 42}}},
            {'ab': {'c': 42}},
        )

    def test_type(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.field("a", straw.number()),
                    straw.field("b", straw.string())
                )
            ],
            {'a': 3.14},
            {'b': "3.14"},
        )

    def test_spliter(self):
        def merge(ss):
            return ', '.join(ss)

        def split(s):
            return s.split(', ')

        self.perform(
            [
                straw.StrawPair(
                    straw.field("a", straw.string()),
                    straw.spliter(
                        merge,
                        split,
                        [
                            straw.field("aa", straw.string()),
                            straw.field("ab", straw.string()),
                            straw.field("ac", straw.string()),
                        ]
                    )
                )
            ],
            {'a': 'a, b, c'},
            {'aa': 'a',
             'ab': 'b',
             'ac': 'c'}
        )

    def test_spliter_more(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.spliter(
                        lambda x: x,
                        lambda x: x,
                        [
                            straw.field("aa", straw.string()),
                            straw.field("ab", straw.string()),
                            straw.field("ac", straw.string()),
                        ]
                    ),
                    straw.spliter(
                        lambda x: x,
                        lambda x: x,
                        [
                            straw.field("ba", straw.number()),
                            straw.field("bb", straw.number()),
                            straw.field("bc", straw.number()),
                        ]
                    )
                )
            ],
            {'aa': '1.0', 'ab': '2.0', 'ac': '3.0'},
            {'ba': 1., 'bb': 2., 'bc': 3.},
        )

    def test_const(self):
        actual = straw.squeeze(
            [
                straw.StrawPair(
                    straw.const(True),
                    straw.field("a", straw.boolean())
                )
            ],
            {},
        )
        self.assertDictEqual(actual, {'a': True})

    def test_index(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.index(4, straw.number()),
                    straw.field("a", straw.number())
                )
            ],
            [None, None, None, None, 42.],
            {'a': 42.},
        )


class StrawReadmeTestCase(TestCase):
    def test_readme(self):
        self.perform(
            [
                straw.StrawPair(
                    straw.field("Name", straw.field("First", straw.string())),
                    straw.field("first_name", straw.string())
                ),
                straw.StrawPair(
                    straw.field("Name", straw.field("Last", straw.string())),
                    straw.field("last_name", straw.string())
                ),
                straw.StrawPair(
                    straw.field(
                        "Birthday",
                        straw.spliter(
                            lambda xs: '/'.join([str(x) for x in xs]),
                            lambda s: s.split('/'),
                            [
                                straw.field("Year", straw.number()),
                                straw.field("Month", straw.number()),
                                straw.field("Day", straw.number()),
                            ]
                        )
                    ),
                    straw.field("birthday", straw.string())
                ),
                straw.StrawPair(
                    straw.field(
                        "WorkAddress",
                        straw.spliter(
                            lambda x: ', '.join(x),
                            lambda x: x.split(', '),
                            [
                                straw.field("Street", straw.string()),
                                straw.field("City", straw.string()),
                                straw.field("State", straw.string()),
                                straw.field("PostalCode", straw.string()),
                                straw.field("Country", straw.string()),
                            ]
                        )
                    ),
                    straw.field(
                        'addresses',
                        straw.field('work', straw.string())),
                )
            ],
            {
                "Name": {
                    "First": "Walter",
                    "Last": "Bishop"
                },
                "Birthday": {
                    "Year": 1946,
                    "Month": 8,
                    "Day": 20
                },
                "WorkAddress": {
                    "Street": "350 W Georgia St",
                    "City": "Vancouver",
                    "State": "BC",
                    "Country": "Canada",
                    "PostalCode": "V6B 6B1"
                }
            },
            {
                "first_name": "Walter",
                "last_name": "Bishop",
                "birthday": "1946/8/20",
                "addresses": {
                    "work": "350 W Georgia St, Vancouver, BC, V6B 6B1, Canada"
                }
            }
        )


if __name__ == "__main__":
    unittest.main()
