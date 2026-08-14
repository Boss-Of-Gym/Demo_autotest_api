import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_BONUSES_DELETE
from .request_body import CLIENTS_BONUSES_DELETE_REQUEST

CLIENTS_BONUSES_DELETE_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='POST /clients_bonuses.delete - valid session',
            test_id='crm_clients_bonuses_delete_001',
            expected=EXPECTED_VALID_CLIENTS_BONUSES_DELETE,
            json=CLIENTS_BONUSES_DELETE_REQUEST,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_bonuses_delete, pytest.mark.admin],
    ),
]
