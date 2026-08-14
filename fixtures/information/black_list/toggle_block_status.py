import pytest

from core.client import BaseHTTPClient
from services.information.black_list.toggle_block_status import BlackListToggleBlockStatusService


@pytest.fixture
def black_list_toggle_block_status_service(api_client: BaseHTTPClient) -> BlackListToggleBlockStatusService:
    return BlackListToggleBlockStatusService(client=api_client)
