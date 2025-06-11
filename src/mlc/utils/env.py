import os
from typing import Optional, Union

from mlc.utils.better_enum import BetterEnum


class EnvVar(BetterEnum):
    DB_NAME = "DB_NAME"
    DB_USER = "DB_USER"
    DB_PASS = "DB_PASS"
    DB_PORT = "DB_PORT"
    DB_HOST = "DB_HOST"


def get_env(var: Union[str, EnvVar], default: Optional = None) -> Optional[str]:
    if isinstance(var, EnvVar):
        var = var.name
    return os.getenv(var, default=default)
