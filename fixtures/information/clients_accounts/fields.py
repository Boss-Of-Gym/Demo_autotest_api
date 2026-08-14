import pytest

from core.client import BaseHTTPClient
from services.information.clients_accounts.fields import ClientsAccountsFieldsService


@pytest.fixture
def clients_accounts_fields_service(api_client: BaseHTTPClient) -> ClientsAccountsFieldsService:
    return ClientsAccountsFieldsService(client=api_client)
