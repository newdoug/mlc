from typing import Optional

from sqlmodel import Field, SQLModel

from mlc.utils.dt import get_utc_now


class GeneratedData(SQLModel, table=True):
    id: int = Field(primary_key=True)
    # TODO: proper foreign key to GeneratedData table
    generated_data_id: Optional[int] = None
    # TODO: best way to store bytes in SQLModel?
    # base64
    data: str
    # TODO: JSON/BJSON/whatever is best way
    features: dict
    # TODO: JSON/BJSON/whatever is best way
    metadata: dict
