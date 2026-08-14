from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


class ClientsAccountsUpdateRequest(BaseModel):
    id: int
    name: str
    gender: Literal['woman', 'man']
    date_of_birth: Optional[str] = None
    model_config = ConfigDict(extra='forbid', strict=True, frozen=True, validate_assignment=True, populate_by_name=True)