from collections.abc import Generator

import pytest

from config.settings import get_settings
from core.client import BaseHTTPClient


@pytest.fixture(scope='session')
def api_client() -> Generator[BaseHTTPClient, None, None]:
    settings = get_settings()
    client = BaseHTTPClient(
        base_url=settings.base_url,
        timeout=settings.timeout,
        headers=settings.default_headers,
    )
    yield client
    client.close()
