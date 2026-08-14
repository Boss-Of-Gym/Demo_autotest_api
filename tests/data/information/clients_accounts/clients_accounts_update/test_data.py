import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_ACCOUNTS_UPDATE
from .request_body import CLIENTS_ACCOUNTS_UPDATE_REQUEST

CLIENTS_ACCOUNTS_UPDATE_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='POST /clients_accounts.update - valid session',
            test_id='crm_clients_accounts_update_001',
            expected=EXPECTED_VALID_CLIENTS_ACCOUNTS_UPDATE,
            json=CLIENTS_ACCOUNTS_UPDATE_REQUEST,
            params={'chain_id': 7156},
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_accounts_update, pytest.mark.admin],
    ),
]
