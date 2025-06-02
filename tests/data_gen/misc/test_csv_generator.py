"""`csv_generator` tests"""

import csv
import os
import tempfile
import unittest

from mlc.data_gen.misc.csv_generator import (
    DEFAULT_CSV_LINE_ENDING,
    generate_random_csv_data,
    generate_random_csv_header,
    generate_random_csv_header_and_data,
)


class TestGenerateRandomCsvData(unittest.TestCase):
    """`generate_random_csv_data` function"""

    def test_4_rows_no_header_consistent_types(self):
        """4 rows, no header given, consistent types"""
        # TODO: fix
        # csv_data = generate_random_csv_data((4, 5))
        csv_data = ""
        with tempfile.NamedTemporaryFile() as csv_file:
            with open(csv_file.name, "w", encoding="UTF-8") as handle:
                handle.write(csv_data)

            with open(csv_file.name, "r", encoding="UTF-8") as handle:
                reader = csv.reader(handle)
                for row in reader:
                    # TODO
                    pass
        csv_data.split(DEFAULT_CSV_LINE_ENDING)
