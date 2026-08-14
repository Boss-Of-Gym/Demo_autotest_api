from ....shared.types import ExpectedResult
from schemas.information.black_list.fields.response import BlackListFieldsResponse

EXPECTED_VALID_BLACK_LIST_FIELDS = ExpectedResult(
    status_code=200,
    status_body='success',
    model=BlackListFieldsResponse,
    description='Valid session → black list fields returned',
)
