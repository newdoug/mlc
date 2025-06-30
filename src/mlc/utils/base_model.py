"""Slight improvements to pydantic BaseModel"""

from copy import deepcopy
import json

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):

    def to_json_dict(self) -> dict:
        return {k: v.hex() if isinstance(v, bytes) else v for k, v in self}

    def to_json(self, pretty: bool = False) -> str:
        return json.dumps(self.to_json_dict(), indent=2 if pretty else None)

    @classmethod
    def from_json_dict(cls, json_dict: dict):
        json_dict = deepcopy(json_dict)
        for field_name, field in cls.model_fields.items():
            if field.annotation is bytes and json_dict.get(field_name) is not None:
                json_dict[field_name] = bytes.fromhex(json_dict[field_name])
        return cls.model_validate(json_dict)

    @classmethod
    def from_json(cls, json_data: str):
        return cls.from_json_dict(json.loads(json_data))
