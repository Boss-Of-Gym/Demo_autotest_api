import pytest

from core.client import BaseHTTPClient
from services.information.clients_addresses.clients_addresses import ClientsAddressesService


@pytest.fixture
def clients_addresses_service(api_client: BaseHTTPClient) -> ClientsAddressesService:
    return ClientsAddressesService(client=api_client)
