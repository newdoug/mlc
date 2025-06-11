from datetime import datetime as dt
from typing import Optional

from sqlmodel import DateTime, Field, SQLModel

from mlc.utils.dt import get_utc_now


class LogRecord(SQLModel, table=True):
    __tablename__ = "log_records"

    id: int = Field(primary_key=True)
    created: dt = Field(default_factory=get_utc_now)
    # TODO: consider making these saller fields like CHAR(50) or something because I think those are faster than just
    #       TEXT
    level: str
    name: str
    message: str
    pathname: str
    lineno: int
    func: str
    exception: Optional[str] = None
