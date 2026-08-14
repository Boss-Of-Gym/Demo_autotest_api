import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_BLACK_LIST

BLACK_LIST_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='GET /black_list - valid session',
            test_id='crm_black_list_001',
            expected=EXPECTED_VALID_BLACK_LIST,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.black_list, pytest.mark.admin],
    ),
]
