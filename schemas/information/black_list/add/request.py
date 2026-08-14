from typing import Literal

from pydantic import BaseModel, ConfigDict


class BlackListAddRequest(BaseModel):
    type_lock: Literal['phone_number', 'profile_id', 'account_id']
    model_config = ConfigDict(extra='forbid', strict=True, frozen=True, validate_assignment=True, populate_by_name=True)