# kuromon

[![PyPI version](https://badge.fury.io/py/kuromon.svg)](https://badge.fury.io/py/kuromon)
[![Python CI](https://github.com/ninoseki/kuromon/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/kuromon/actions/workflows/test.yml)

Convert a list of dict, dataclass, Pydantic or POPO objects into a string represented table.

## Requirements

- Python 3.7+

## Installation

```bash
pip install kuromon
# or if you want to use Pydantic along with kuromon
pip install kuromon[pydantic]
```

## Usage

```py
from kuromon import to_table

dict_data = [
    {"id": 1, "name": "foo", "tags": None},
    {"id": 2, "name": "bar", "tags": ["a"]},
]
print(to_table(dict_data))
# |    |   id | name   | tags   |
# |----|------|--------|--------|
# |  0 |    1 | foo    |        |
# |  1 |    2 | bar    | ['a']  |

# Disable indexing by setting index=False
print(to_table(dict_data, index=False))
# |   id | name   | tags   |
# |------|--------|--------|
# |    1 | foo    |        |
# |    2 | bar    | ['a']  |

# Change the table format via tablefmt
# NOTE: You can use the following tabulate formats
#       https://github.com/astanin/python-tabulate#table-format
print(to_table(dict_data, tablefmt="plain"))
# 0     1  foo
# 1     2  bar     ['a']
```

The above example uses a list of dict objects. You can also use a list of dataclass or Pydantic objects.

```py
from dataclasses import dataclass
from typing import List, Optional

from dacite import from_dict
from pydantic import BaseModel

from kuromon import to_table


class TestModel(BaseModel):
    id: int
    name: str
    tags: Optional[List[str]]


@dataclass
class TestDataClass:
    id: int
    name: str
    tags: Optional[List[str]]


dict_data = [
    {"id": 1, "name": "foo", "tags": None},
    {"id": 2, "name": "bar", "tags": ["a"]},
]
pydantic_data = [TestModel.parse_obj(obj) for obj in dict_data]
dataclass_data = [from_dict(data_class=TestDataClass, data=obj) for obj in dict_data]

print(to_table(pydantic_data))
print(to_table(dataclass_data))
```
