import allure
import pytest

from services.information.clients_accounts.update import ClientsAccountsUpdateService
from tests.data.information.clients_accounts.clients_accounts_update.test_data import CLIENTS_ACCOUNTS_UPDATE_TEST_DATA
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
@allure.feature('Clients Accounts')
@allure.story('POST /clients_accounts.update')
class TestClientsAccountsUpdate:

    @pytest.mark.parametrize(
        'case',
        CLIENTS_ACCOUNTS_UPDATE_TEST_DATA,
        ids=generate_test_ids(CLIENTS_ACCOUNTS_UPDATE_TEST_DATA),
    )
    def test_clients_accounts_update(
        self,
        case: GetCase,
        clients_accounts_update_service: ClientsAccountsUpdateService,
        session_id: str,
    ) -> None:
        allure.dynamic.id(id=case.test_id)
        allure.dynamic.title(test_title=case.description)
        allure.dynamic.description(test_description=case.expected.description)

        with allure.step(f'{case.description}'):
            response = clients_accounts_update_service.post_clients_accounts_update(
                session_id=session_id,
                request=case.json,
                chain_id=case.params['chain_id'],
            )

        validate_status_code(response=response, expected=case.expected.status_code)
        validate_content_type(response=response, expected=case.expected.content_type)
        validate_response_time(response=response)
        validate_headers(response=response)
        validate_body_status(response=response, expected=case.expected.status_body)
        validate_model(response=response, model=case.expected.model)
        validate_schema(response=response, schema=case.expected.model.model_json_schema())
