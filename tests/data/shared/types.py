from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel


@dataclass(frozen=True)
class ExpectedResult:
    status_code: int
    status_body: str
    model: type[BaseModel]
    content_type: str = 'application/json'
    description: str = ''


@dataclass(frozen=True)
class GetCase:
    description: str
    test_id: str
    expected: ExpectedResult
    json: BaseModel | None = None
    params: dict[str, Any] | None = None
    headers: dict[str, str] | None = None
