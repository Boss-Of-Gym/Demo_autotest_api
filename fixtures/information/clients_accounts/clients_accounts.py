import pytest

from core.client import BaseHTTPClient
from services.information.clients_accounts.clients_accounts import ClientsAccountsService


@pytest.fixture
def clients_accounts_service(api_client: BaseHTTPClient) -> ClientsAccountsService:
    return ClientsAccountsService(client=api_client)
