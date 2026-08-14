from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


class ClientsBonusesAddRequest(BaseModel):
    mode: Literal['one', 'all']
    type: Literal['accrual', 'withdraw']
    sum: float
    chain_id: int
    date_available: Optional[str] = None
    date_expiration: Optional[str] = None
    description: Optional[str] = None
    phone_format_id: Optional[int] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    model_config = ConfigDict(extra='forbid', strict=True, frozen=True, validate_assignment=True, populate_by_name=True)