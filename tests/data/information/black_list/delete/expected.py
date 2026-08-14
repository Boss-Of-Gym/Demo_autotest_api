from ....shared.types import ExpectedResult
from schemas.information.black_list.delete.response import BlackListDeleteResponse

EXPECTED_VALID_BLACK_LIST_DELETE = ExpectedResult(
    status_code=200,
    status_body='success',
    model=BlackListDeleteResponse,
    description='Valid session → black list entry deleted successfully',
)
