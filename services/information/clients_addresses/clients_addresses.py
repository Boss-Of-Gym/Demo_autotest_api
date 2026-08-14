import httpx

from enums.endpoints import InformationEndpoints
from services.base import BaseService


class ClientsAddressesService(BaseService):
    def get_clients_addresses(self, session_id: str) -> httpx.Response:
        return self._client.request(
            method='get',
            endpoint=InformationEndpoints.CLIENTS_ADDRESSES,
            headers={'authorization': f'Session {session_id}'},
        )
