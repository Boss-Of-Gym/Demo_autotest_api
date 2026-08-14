from pydantic import BaseModel, ConfigDict


class BlackListDeleteRequest(BaseModel):
    id: int
    model_config = ConfigDict(extra='forbid', strict=True, frozen=True, validate_assignment=True, populate_by_name=True)