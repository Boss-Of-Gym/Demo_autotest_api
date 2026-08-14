import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_CLIENTS_BONUSES_FIELDS

CLIENTS_BONUSES_FIELDS_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='GET /clients_bonuses.fields - valid session',
            test_id='crm_clients_bonuses_fields_001',
            expected=EXPECTED_VALID_CLIENTS_BONUSES_FIELDS,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.clients_bonuses_fields, pytest.mark.admin],
    ),
]
