import httpx

from enums.endpoints import InformationEndpoints
from schemas.information.clients_bonuses.clients_bonuses_add.request import ClientsBonusesAddRequest
from services.base import BaseService


class ClientsBonusesAddService(BaseService):
    def post_clients_bonuses_add(
        self,
        session_id: str,
        request: ClientsBonusesAddRequest,
    ) -> httpx.Response:
        return self._client.request(
            method='post',
            endpoint=InformationEndpoints.CLIENTS_BONUSES_ADD,
            headers={'authorization': f'Session {session_id}'},
            json=request.model_dump(exclude_none=True),
        )
