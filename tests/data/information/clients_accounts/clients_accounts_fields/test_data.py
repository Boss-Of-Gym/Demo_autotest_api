import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_ACCOUNTS_FIELDS

CLIENTS_ACCOUNTS_FIELDS_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='GET /clients_accounts.fields - valid session',
            test_id='crm_clients_accounts_fields_001',
            expected=EXPECTED_VALID_CLIENTS_ACCOUNTS_FIELDS,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_accounts_fields, pytest.mark.admin],
    ),
]
