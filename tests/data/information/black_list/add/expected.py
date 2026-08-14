from ....shared.types import ExpectedResult
from schemas.information.black_list.add.response import BlackListAddResponse

EXPECTED_VALID_BLACK_LIST_ADD = ExpectedResult(
    status_code=200,
    status_body='success',
    model=BlackListAddResponse,
    description='Valid session → black list entry added successfully',
)
