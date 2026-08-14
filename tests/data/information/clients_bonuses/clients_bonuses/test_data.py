import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_BONUSES

CLIENTS_BONUSES_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='GET /clients_bonuses - valid session',
            test_id='crm_clients_bonuses_001',
            expected=EXPECTED_VALID_CLIENTS_BONUSES,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_bonuses, pytest.mark.admin],
    ),
]
