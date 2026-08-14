from ....shared.types import ExpectedResult
from schemas.information.clients_accounts.clients_accounts_update.response import ClientsAccountsUpdateResponse

EXPECTED_VALID_CLIENTS_ACCOUNTS_UPDATE = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsAccountsUpdateResponse,
    description='Valid session → client account updated successfully',
)
