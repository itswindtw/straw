# pyStraw 🥤

* Declaratively to write your mapping once to handle
    * nested fields
    * fields with one - to - one, one - to - many, many - to - many relationships
    * reversible transform

# Getting started

Let's say you have an object.

```json
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
}
```

and you would like to transform it back and forth to the following:

```json
{
    "first_name": "Walter",
    "last_name": "Bishop",
    "birthday": "1946/8/20",
    "addresses": {
        "work": "350 W Georgia St, Vancouver, BC, V6B 6B1, Canada"
    }
}
```

You can do that with the following:

```python
import straw

spec = [
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
                lambda s: [int(x) for x in s.split('/')],
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
        straw.field('addresses',
                    straw.field('work', straw.string())),
    )
]

source = {
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
}

expected = {
    "first_name": "Walter",
    "last_name": "Bishop",
    "birthday": "1946/8/20",
    "addresses": {
        "work": "350 W Georgia St, Vancouver, BC, V6B 6B1, Canada"
    }
}

assertDictEqual(straw.squeeze(spec, source), expected)  # passed

reversed_specs = [straw.StrawPair(s.end, s.start) for s in specs]
assertDictEqual(straw.squeeze(reversed_specs, expected), source)  # passed
```


# Note

This is still in POC phase. Please refer to `test_straw.py` for more usage.
