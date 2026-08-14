from schemas.application.authorization.response import ErrorResponse
from tests.data.shared.types import ExpectedResult

EXPECTED_ERROR = ExpectedResult(
    status_code=200,
    status_body='error',
    model=ErrorResponse,
    description='API returns HTTP 200 with status=error for business-level failures',
)
