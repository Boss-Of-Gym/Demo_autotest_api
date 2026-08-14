from typing import Literal

from pydantic import BaseModel, ConfigDict


class ClientsBonusesResponse(BaseModel):
    request_id: str
    status: Literal['success']
    data: dict
    model_config = ConfigDict(extra='forbid', strict=True, frozen=True, validate_assignment=True, populate_by_name=True)