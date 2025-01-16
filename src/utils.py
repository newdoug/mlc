"""General utilities, will probably organize/split up better later"""

import enum
from typing import List


__ALL__ = [
    "BetterEnum",
]


class BetterEnum(enum.Enum):
    """Slightly improved enum class. Just adds a couple conveniences"""

    @classmethod
    def values(cls) -> List:
        """Returns members/values of the enum"""
        return list(cls.__members__.keys())
