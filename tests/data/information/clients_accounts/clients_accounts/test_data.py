import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_ACCOUNTS

CLIENTS_ACCOUNTS_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='GET /clients_accounts - valid session',
            test_id='crm_clients_accounts_001',
            expected=EXPECTED_VALID_CLIENTS_ACCOUNTS,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_accounts, pytest.mark.admin],
    ),
]
