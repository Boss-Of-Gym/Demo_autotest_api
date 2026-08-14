import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_BLACK_LIST_FIELDS

BLACK_LIST_FIELDS_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='GET /black_list.fields - valid session',
            test_id='crm_black_list_fields_001',
            expected=EXPECTED_VALID_BLACK_LIST_FIELDS,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.black_list_fields, pytest.mark.admin],
    ),
]
