import pytest

from core.client import BaseHTTPClient
from services.information.clients_bonuses.delete import ClientsBonusesDeleteService


@pytest.fixture
def clients_bonuses_delete_service(api_client: BaseHTTPClient) -> ClientsBonusesDeleteService:
    return ClientsBonusesDeleteService(client=api_client)
