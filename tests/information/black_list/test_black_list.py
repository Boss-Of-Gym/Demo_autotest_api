import allure
import pytest

from services.information.black_list.black_list import BlackListService
from tests.data.information.black_list.black_list.test_data import BLACK_LIST_TEST_DATA
from tests.data.shared.types import GetCase
from utils.pytest_helpers import generate_test_ids
from validators.http import (
    validate_content_type,
    validate_headers,
    validate_response_time,
    validate_status_code,
)
from validators.response import (
    validate_body_status,
    validate_model,
    validate_schema,
)


@allure.epic('CRM API')
@allure.feature('Black list')
@allure.story('GET /black_list')
class TestBlackList:

    @pytest.mark.parametrize(
        'case',
        BLACK_LIST_TEST_DATA,
        ids=generate_test_ids(BLACK_LIST_TEST_DATA),
    )
    def test_black_list(
        self,
        case: GetCase,
        black_list_service: BlackListService,
        session_id: str,
    ) -> None:
        allure.dynamic.id(id=case.test_id)
        allure.dynamic.title(test_title=case.description)
        allure.dynamic.description(test_description=case.expected.description)

        with allure.step(f'{case.description}'):
            response = black_list_service.get_black_list(session_id=session_id)

        validate_status_code(response=response, expected=case.expected.status_code)
        validate_content_type(response=response, expected=case.expected.content_type)
        validate_response_time(response=response)
        validate_headers(response=response)
        validate_body_status(response=response, expected=case.expected.status_body)
        validate_model(response=response, model=case.expected.model)
        validate_schema(response=response, schema=case.expected.model.model_json_schema())
