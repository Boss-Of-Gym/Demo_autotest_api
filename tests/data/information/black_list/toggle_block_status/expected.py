from ....shared.types import ExpectedResult
from schemas.information.black_list.toggle_block_status.response import BlackListToggleBlockStatusResponse

EXPECTED_VALID_BLACK_LIST_TOGGLE_BLOCK_STATUS = ExpectedResult(
    status_code=200,
    status_body='success',
    model=BlackListToggleBlockStatusResponse,
    description='Valid session → black list block status toggled successfully',
)
