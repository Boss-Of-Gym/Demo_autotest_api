import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_ADDRESSES

CLIENTS_ADDRESSES_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='GET /clients_addresses - valid session',
            test_id='crm_clients_addresses_001',
            expected=EXPECTED_VALID_CLIENTS_ADDRESSES,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_addresses, pytest.mark.admin],
    ),
]
