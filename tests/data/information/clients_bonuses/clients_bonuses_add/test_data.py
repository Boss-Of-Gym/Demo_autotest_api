import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_BONUSES_ADD
from .request_body import CLIENTS_BONUSES_ADD_REQUEST

CLIENTS_BONUSES_ADD_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='POST /clients_bonuses.add - valid session',
            test_id='crm_clients_bonuses_add_001',
            expected=EXPECTED_VALID_CLIENTS_BONUSES_ADD,
            json=CLIENTS_BONUSES_ADD_REQUEST,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_bonuses_add, pytest.mark.admin],
    ),
]
