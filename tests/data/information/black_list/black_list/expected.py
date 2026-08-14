from ....shared.types import ExpectedResult
from schemas.information.black_list.black_list.response import BlackListResponse

EXPECTED_VALID_BLACK_LIST = ExpectedResult(
    status_code=200,
    status_body='success',
    model=BlackListResponse,
    description='Valid session → black list returned',
)
