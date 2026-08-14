from pydantic import BaseModel, ConfigDict


class BlackListToggleBlockStatusRequest(BaseModel):
    id: int
    active: bool
    model_config = ConfigDict(extra='forbid', strict=True, frozen=True, validate_assignment=True, populate_by_name=True)