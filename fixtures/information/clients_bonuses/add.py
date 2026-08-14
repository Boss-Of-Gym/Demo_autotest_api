import pytest

from core.client import BaseHTTPClient
from services.information.clients_bonuses.add import ClientsBonusesAddService


@pytest.fixture
def clients_bonuses_add_service(api_client: BaseHTTPClient) -> ClientsBonusesAddService:
    return ClientsBonusesAddService(client=api_client)
