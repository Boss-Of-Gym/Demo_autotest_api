import httpx

from enums.endpoints import InformationEndpoints
from services.base import BaseService


class ClientsAccountsFieldsService(BaseService):
    def get_clients_accounts_fields(self, session_id: str) -> httpx.Response:
        return self._client.request(
            method='get',
            endpoint=InformationEndpoints.CLIENTS_ACCOUNTS_FIELDS,
            headers={'authorization': f'Session {session_id}'},
        )
