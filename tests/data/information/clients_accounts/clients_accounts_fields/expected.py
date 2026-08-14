from ....shared.types import ExpectedResult
from schemas.information.clients_accounts.clients_accounts_fields.response import ClientsAccountsFieldsResponse

EXPECTED_VALID_CLIENTS_ACCOUNTS_FIELDS = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsAccountsFieldsResponse,
    description='Valid session → clients accounts fields returned',
)
