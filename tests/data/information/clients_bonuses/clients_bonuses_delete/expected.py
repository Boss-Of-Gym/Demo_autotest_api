from ....shared.types import ExpectedResult
from schemas.information.clients_bonuses.clients_bonuses_delete.response import ClientsBonusesDeleteResponse

EXPECTED_VALID_CLIENTS_BONUSES_DELETE = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsBonusesDeleteResponse,
    description='Valid session → client bonuses deleted successfully',
)
