import pytest

from core.client import BaseHTTPClient
from services.information.black_list.delete import BlackListDeleteService


@pytest.fixture
def black_list_delete_service(api_client: BaseHTTPClient) -> BlackListDeleteService:
    return BlackListDeleteService(client=api_client)
