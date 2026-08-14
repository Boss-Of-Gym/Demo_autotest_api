import pytest

from ....shared.types import GetCase
from .expected import EXPECTED_VALID_BLACK_LIST_DELETE
from .request_body import BLACK_LIST_DELETE_REQUEST

BLACK_LIST_DELETE_TEST_DATA: list[pytest.param] = [
    pytest.param(
        GetCase(
            description='POST /black_list.delete - valid session',
            test_id='crm_black_list_delete_001',
            expected=EXPECTED_VALID_BLACK_LIST_DELETE,
            json=BLACK_LIST_DELETE_REQUEST,
        ),
        marks=[pytest.mark.smoke, pytest.mark.positive, pytest.mark.black_list_delete, pytest.mark.admin],
    ),
]
