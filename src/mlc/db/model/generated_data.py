from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from mlc.utils.dt import get_utc_now
from mlc.utils.version import CURRENT_VERSION


class GeneratedData(SQLModel, table=True):
    __tablename__ = "generated_data"

    id: int = Field(primary_key=True)
    data_type: str
    tags: str
    # E.g., ciphertexts would reference the plaintext that came before it in a
    # chain of transformations. Or compressed data, etc.
    prev_data_id: Optional[int] = Field(default=None, foreign_key="generated_data.id")
    prev_data: Optional[GeneratedData] = Relationship(back_populates="prev_data_id")
    # base64
    data: str
    # JSON
    features: Optional[str] = None
    created: dt = Field(default_factory=get_utc_now)
    seed: Optional[int] = None
    method: Optional[str] = None
    # Version of software used to generated this data
    sw_version: Optional[str] = Field(default=CURRENT_VERSION)
    # JSON
    metadata: Optional[str] = None
