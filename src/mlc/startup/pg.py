from typing import Optional

from mlc.db.manager import DbManager
from mlc.db.urls import make_pg_url
from mlc.utils.env import EnvVar, get_env


DEFAULT_PORT: int = 5432
DEFAULT_HOST: str = "localhost"


def set_up_db(
    db_name: Optional[str] = None,
    db_user: Optional[str] = None,
    db_pass: Optional[str] = None,
    db_port: Optional[int] = None,
    db_host: Optional[str] = None,
) -> DbManager:
    url = make_pg_url(
        db_name or get_env(EnvVar.DB_NAME),
        db_user or get_env(EnvVar.DB_USER),
        db_pass or get_env(EnvVar.DB_PASS),
        db_port or int(get_env(EnvVar.DB_PORT, DEFAULT_PORT)),
        db_host or get_env(EnvVar.DB_HOST, DEFAULT_HOST),
    )
    return DbManager(url)
