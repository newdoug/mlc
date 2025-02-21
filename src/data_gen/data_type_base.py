"""Types of data we can generate"""

from enum import auto
from typing import Optional

try:
    from ..utils.better_enum import BetterEnum
except (ImportError, ModuleNotFoundError):
    from utils.better_enum import BetterEnum


class DataTypeBase(BetterEnum):
    """Base data type class"""
    def generate(self, settings: Optional[dict] = None) -> bytes:
        raise NotImplementedError("No specific data type to generate")


class DataTypeSettingKey(BetterEnum):
    """Common settings for data type generation.
    Values are keys in a dict.
    """
    CSV_NUM_ROWS = auto()
    JSON_DEPTH = auto()
    LENGTH = auto()
    SPARSE_PERCENT = auto()
    SPARSE_BYTE = auto()
