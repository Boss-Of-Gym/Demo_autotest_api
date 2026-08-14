import pytest

from core.client import BaseHTTPClient
from services.information.clients_accounts.update import ClientsAccountsUpdateService


@pytest.fixture
def clients_accounts_update_service(api_client: BaseHTTPClient) -> ClientsAccountsUpdateService:
    return ClientsAccountsUpdateService(client=api_client)
