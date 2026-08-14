import httpx

from enums.endpoints import InformationEndpoints
from schemas.information.clients_accounts.clients_accounts_update.request import ClientsAccountsUpdateRequest
from services.base import BaseService


class ClientsAccountsUpdateService(BaseService):
    def post_clients_accounts_update(
        self,
        session_id: str,
        request: ClientsAccountsUpdateRequest,
        chain_id: int,
    ) -> httpx.Response:
        return self._client.request(
            method='post',
            endpoint=InformationEndpoints.CLIENTS_ACCOUNTS_UPDATE,
            headers={'authorization': f'Session {session_id}'},
            params={'chain_id': chain_id},
            json=request.model_dump(exclude_none=True),
        )
