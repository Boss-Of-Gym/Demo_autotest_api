from ....shared.types import ExpectedResult
from schemas.information.clients_accounts.clients_accounts.response import ClientsAccountsResponse

EXPECTED_VALID_CLIENTS_ACCOUNTS = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsAccountsResponse,
    description='Valid session → clients accounts returned',
)
