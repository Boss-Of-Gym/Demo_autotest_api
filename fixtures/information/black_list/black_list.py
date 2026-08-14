import pytest

from core.client import BaseHTTPClient
from services.information.black_list.black_list import BlackListService


@pytest.fixture
def black_list_service(api_client: BaseHTTPClient) -> BlackListService:
    return BlackListService(client=api_client)
