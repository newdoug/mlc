"""Tools for generating JSON"""

import json
from typing import Union

from mlc.data_gen.random_data import (
    rand_ascii_str,
    rand_element_in_list,
    rand_float,
    rand_int_in_range,
    rand_int64,
)


__all__ = [
    "JsonGenerator",
    "rand_json",
    "rand_json_str",
]


class JsonGenerator:
    """Generates random JSON"""

    NON_RECURSIVE_TYPES = [
        int,
        float,
        str,
        None,
    ]
    LIST_DATA_TYPES = [dict, list] + NON_RECURSIVE_TYPES
    DICT_DATA_TYPES = [dict, list] + NON_RECURSIVE_TYPES
    # The most common types for the outer most element type. The others are
    # valid, but don't really produce interesting JSON.
    OUTER_TYPES = [
        dict,
        list,
    ]
    # These are all valid
    TRUE_OUTER_TYPES = OUTER_TYPES + NON_RECURSIVE_TYPES

    def __init__(
        self,
        max_depth: int = 5,
        max_num_keys: int = 20,
        max_list_length: int = 20,
        min_key_length: int = 2,
        max_key_length: int = 16,
    ) -> Union[dict, list]:
        self.max_depth = max_depth
        self.max_num_keys = max_num_keys
        self.max_list_length = max_list_length
        self.min_key_length = min_key_length
        self.max_key_length = max_key_length

    def _gen_dict(self, depth: int) -> dict:
        if depth >= self.max_depth:
            return {}
        return {
            self._gen_key(): self._gen_element(
                depth + 1, rand_element_in_list(JsonGenerator.DICT_DATA_TYPES)
            )
            for _ in range(rand_int_in_range(0, self.max_num_keys))
        }

    def _gen_list(self, depth: int) -> list:
        if depth >= self.max_depth:
            return []
        return [
            self._gen_element(depth + 1, rand_element_in_list(JsonGenerator.LIST_DATA_TYPES))
            for _ in range(rand_int_in_range(0, self.max_list_length))
        ]

    def _gen_key(self) -> str:
        # range arbitrarily chosen
        return rand_ascii_str(rand_int_in_range(self.min_key_length, self.max_key_length + 1))

    def _gen_element(self, depth: int, type_):
        if type_ is None:
            return None
        if type_ is int:
            return rand_int64()
        if type_ is float:
            return rand_float()
        if type_ is str:
            return rand_ascii_str(rand_int_in_range(2, 13))
        if type_ is dict:
            return self._gen_dict(depth)
        if type_ is list:
            return self._gen_list(depth)
        raise ValueError(f"Invalid JSON element type: {type_}")

    def gen_data(self) -> Union[dict, list]:
        """Returns randon JSON data"""
        # 1% percent chance of using a boring outer type
        if rand_int_in_range(0, 100) >= 1:
            outer_types = JsonGenerator.OUTER_TYPES
        else:
            outer_types = JsonGenerator.TRUE_OUTER_TYPES
        outer_type = rand_element_in_list(outer_types)
        return self._gen_element(0, outer_type)

    def gen_str(self, indent: int = 2) -> str:
        """Returns random JSON formatted as a string"""
        return json.dumps(self.gen_data(), indent=indent)


def rand_json(max_depth: int) -> Union[dict, list]:
    """Generate random JSON data"""
    return JsonGenerator(max_depth).gen_data()


def rand_json_str(max_depth: int, indent: int = 2) -> str:
    """Generates random JSON data and formats it as a string"""
    return json.dumps(rand_json(max_depth), indent=indent)
