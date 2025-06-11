from typing import Optional

from sqlmodel import Field, SQLModel

from mlc.utils.dt import get_utc_now


class GeneratedData(SQLModel, table=True):
    id: int = Field(primary_key=True)
    data_type: str
    # TODO: consider foreign key to `id` field. E.g., ciphertexts would reference the plaintext that came before it in a
    # chain of transformations. Or compressed data, etc.
    prev_data_id: Optional[int] = None
    # TODO: best way to store bytes in SQLModel?
    # base64
    data: str
    created: dt = Field(default_factory=get_utc_now)
    # TODO: JSON/BJSON/whatever is best way
    metadata: dict
    seed: Optional[int] = None
    method: Optional[str] = None
    # Version of software used to generated this data. TODO: default to current version (after doing version stuff)
    sw_version: str
