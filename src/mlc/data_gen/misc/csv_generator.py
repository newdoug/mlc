"""CSV generation functions and things"""

import shlex
from typing import List, Optional, Tuple

from mlc.data_gen.random_data import (
    rand_ascii_str,
    rand_element_in_list,
    rand_float,
    rand_int_in_range,
    rand_uint32,
)


DEFAULT_CSV_NUM_COLS: int = 8

CSV_VALUE_DATA_TYPES = [
    int,
    float,
    # Includes empty string
    str,
]

# Arbitrarily chosen as hopefully reasonably common
DEFAULT_CSV_HEADER_STR_SIZE_RANGE: Tuple[int] = (2, 12)
DEFAULT_CSV_RANDOM_STR_DATA_SIZE_RANGE: Tuple[int] = (0, 20)
# TODO: configurable?
DEFAULT_CSV_LINE_ENDING = "\n"


def _random_csv_data_type():
    return rand_element_in_list(CSV_VALUE_DATA_TYPES)


def _generate_random_csv_data(data_type):
    if data_type is int:
        return rand_uint32()
    if data_type is float:
        return rand_float()
    if data_type is str:
        return rand_ascii_str(
            DEFAULT_CSV_RANDOM_STR_DATA_SIZE_RANGE[0],
            DEFAULT_CSV_RANDOM_STR_DATA_SIZE_RANGE[1],
        )
    raise ValueError(f"Bad data type for CSV data generation: '{data_type}'")


def _quote_s(value) -> str:
    if isinstance(value, str):
        return shlex.quote(value) if value else ""
    return str(value)


def generate_random_csv_header(num_cols: int = DEFAULT_CSV_NUM_COLS) -> List[str]:
    """Generate a random CSV header. Column names are random ASCII."""
    header = [None] * num_cols
    for i in range(num_cols):
        header[i] = rand_ascii_str(
            rand_int_in_range(
                DEFAULT_CSV_HEADER_STR_SIZE_RANGE[0],
                DEFAULT_CSV_HEADER_STR_SIZE_RANGE[1],
            )
        )
    return header


def generate_random_csv_data(
    num_rows_range: Tuple[int, int],
    header: Optional[List[str]] = None,
    consistent_col_data_type: bool = True,
) -> str:
    """Generate random CSV data contents with `num_cols` rows.
    if `consistent_col_data_type` is `True`, each column will be assigned a
    data type. Then, data for each column will be randomly generated.
    """
    # TODO: sparsity value as input? Empty strings for sparse strings, 0 for
    #       ints&floats.
    if not header:
        csv_data = ""
        num_cols = DEFAULT_CSV_NUM_COLS
    else:
        csv_data = (
            f"{','.join([_quote_s(value) for value in header])}"
            f"{DEFAULT_CSV_LINE_ENDING}"
        )
        num_cols = len(header)
    # If None, a random data type will be chosen for each value
    data_types = [None] * num_cols
    if consistent_col_data_type:
        for idx in range(num_cols):
            data_types[idx] = _random_csv_data_type()

    for _ in range(num_rows_range[0], num_rows_range[1] + 1):
        row = [None] * num_cols
        for col_idx in range(num_cols):
            data_type = data_types[col_idx] or _random_csv_data_type()
            # We're going to convert to a full string anyways, so this case is
            # just a minor optimization to not have to loop the row again.
            row[col_idx] = _quote_s(_generate_random_csv_data(data_type))
        csv_data += f"{','.join(row)}{DEFAULT_CSV_LINE_ENDING}"
    if csv_data:
        return csv_data[: -len(DEFAULT_CSV_LINE_ENDING)]
    return csv_data


def generate_random_csv_header_and_data(
    num_rows_range: Tuple[int, int],
    num_cols: int = DEFAULT_CSV_NUM_COLS,
    consistent_col_data_type: bool = True,
) -> str:
    """Generate random CSV header of length `num_cols` and data"""
    header = generate_random_csv_header(num_cols)
    return generate_random_csv_data(
        num_rows_range,
        header,
        consistent_col_data_type,
    )
