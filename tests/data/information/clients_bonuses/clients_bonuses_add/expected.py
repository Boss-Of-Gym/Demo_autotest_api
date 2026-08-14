from ....shared.types import ExpectedResult
from schemas.information.clients_bonuses.clients_bonuses_add.response import ClientsBonusesAddResponse

EXPECTED_VALID_CLIENTS_BONUSES_ADD = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsBonusesAddResponse,
    description='Valid session → client bonuses added successfully',
)
