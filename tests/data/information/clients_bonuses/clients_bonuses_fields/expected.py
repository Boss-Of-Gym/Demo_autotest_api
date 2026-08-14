from ....shared.types import ExpectedResult
from schemas.information.clients_bonuses.clients_bonuses_fields.response import ClientsBonusesFieldsResponse

EXPECTED_VALID_CLIENTS_BONUSES_FIELDS = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsBonusesFieldsResponse,
    description='Valid session → clients bonuses fields returned',
)
