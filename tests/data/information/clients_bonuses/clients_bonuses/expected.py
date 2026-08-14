from ....shared.types import ExpectedResult
from schemas.information.clients_bonuses.clients_bonuses.response import ClientsBonusesResponse

EXPECTED_VALID_CLIENTS_BONUSES = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsBonusesResponse,
    description='Valid session → clients bonuses returned',
)
