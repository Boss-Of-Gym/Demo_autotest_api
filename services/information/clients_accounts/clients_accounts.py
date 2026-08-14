import httpx

from enums.endpoints import InformationEndpoints
from services.base import BaseService


class ClientsAccountsService(BaseService):
    def get_clients_accounts(self, session_id: str) -> httpx.Response:
        return self._client.request(
            method='get',
            endpoint=InformationEndpoints.CLIENTS_ACCOUNTS,
            headers={'authorization': f'Session {session_id}'},
        )
