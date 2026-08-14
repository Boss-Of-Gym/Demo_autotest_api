import pytest

from core.client import BaseHTTPClient
from services.information.clients_bonuses.fields import ClientsBonusesFieldsService


@pytest.fixture
def clients_bonuses_fields_service(api_client: BaseHTTPClient) -> ClientsBonusesFieldsService:
    return ClientsBonusesFieldsService(client=api_client)
