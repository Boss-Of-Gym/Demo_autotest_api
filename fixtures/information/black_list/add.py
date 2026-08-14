import pytest

from core.client import BaseHTTPClient
from services.information.black_list.add import BlackListAddService


@pytest.fixture
def black_list_add_service(api_client: BaseHTTPClient) -> BlackListAddService:
    return BlackListAddService(client=api_client)
