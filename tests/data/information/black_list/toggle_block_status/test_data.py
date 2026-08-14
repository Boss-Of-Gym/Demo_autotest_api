import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_BLACK_LIST_TOGGLE_BLOCK_STATUS
from .request_body import BLACK_LIST_TOGGLE_BLOCK_STATUS_REQUEST

BLACK_LIST_TOGGLE_BLOCK_STATUS_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='POST /black_list.toggle_block_status - valid session',
            test_id='crm_black_list_toggle_block_status_001',
            expected=EXPECTED_VALID_BLACK_LIST_TOGGLE_BLOCK_STATUS,
            json=BLACK_LIST_TOGGLE_BLOCK_STATUS_REQUEST,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.black_list_toggle_block_status, pytest.mark.admin],
    ),
]
