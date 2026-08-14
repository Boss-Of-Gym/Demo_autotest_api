import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_BLACK_LIST_ADD
from .request_body import BLACK_LIST_ADD_REQUEST

BLACK_LIST_ADD_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='POST /black_list.add - valid session',
            test_id='crm_black_list_add_001',
            expected=EXPECTED_VALID_BLACK_LIST_ADD,
            json=BLACK_LIST_ADD_REQUEST,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.black_list_add, pytest.mark.admin],
    ),
]
