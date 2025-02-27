"""Enum-related tools"""

import enum
from typing import List


__all__ = [
    "BetterEnum",
]


class BetterEnum(enum.Enum):
    """Slightly improved enum class. Just adds a couple conveniences"""

    @classmethod
    def names(cls) -> List[str]:
        """Returns names of the members of the enum"""
        return list(el.name for el in cls)

    @classmethod
    def values(cls) -> List:
        """Returns values of the members of the enum"""
        return list(el.value for el in cls)

    @classmethod
    def to_dict(cls) -> dict:
        """Names to values dictionary"""
        return dict(zip(cls.names, cls.values))
