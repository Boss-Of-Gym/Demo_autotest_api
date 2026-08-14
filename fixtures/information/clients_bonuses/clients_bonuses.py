import pytest

from core.client import BaseHTTPClient
from services.information.clients_bonuses.clients_bonuses import ClientsBonusesService


@pytest.fixture
def clients_bonuses_service(api_client: BaseHTTPClient) -> ClientsBonusesService:
    return ClientsBonusesService(client=api_client)
