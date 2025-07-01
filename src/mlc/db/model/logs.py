from datetime import datetime as dt
from typing import Optional

from sqlmodel import Field, SQLModel

from mlc.utils.dt import get_utc_now


class LogRecord(SQLModel, table=True):
    __tablename__ = "log_records"

    id: int = Field(primary_key=True)
    created: dt = Field(default_factory=get_utc_now)
    level: str = Field(max_length=10)
    name: str = Field(max_length=16)
    message: str
    pathname: Optional[str] = None
    lineno: Optional[int] = None
    func: Optional[str] = None
    exception: Optional[str] = None
