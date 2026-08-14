from ....shared.types import ExpectedResult
from schemas.information.clients_addresses.clients_addresses.response import ClientsAddressesResponse

EXPECTED_VALID_CLIENTS_ADDRESSES = ExpectedResult(
    status_code=200,
    status_body='success',
    model=ClientsAddressesResponse,
    description='Valid session → clients addresses returned',
)
