from types import TracebackType
from typing import Any, Self

import httpx

from log.logger import get_logger

_logger = get_logger(__name__)


class BaseHTTPClient:
    def __init__(
        self,
        base_url: str,
        timeout: int,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=headers or {},
        )

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        response = self._client.request(
            method=method.upper(),
            url=endpoint,
            headers=headers,
            json=json,
            params=params,
        )
        _logger.log_http(response)
        return response

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()
