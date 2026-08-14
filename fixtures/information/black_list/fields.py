import pytest

from core.client import BaseHTTPClient
from services.information.black_list.fields import BlackListFieldsService


@pytest.fixture
def black_list_fields_service(api_client: BaseHTTPClient) -> BlackListFieldsService:
    return BlackListFieldsService(client=api_client)
