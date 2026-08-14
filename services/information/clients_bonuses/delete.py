import httpx

from enums.endpoints import InformationEndpoints
from schemas.information.clients_bonuses.clients_bonuses_delete.request import ClientsBonusesDeleteRequest
from services.base import BaseService


class ClientsBonusesDeleteService(BaseService):
    def post_clients_bonuses_delete(
        self,
        session_id: str,
        request: ClientsBonusesDeleteRequest,
    ) -> httpx.Response:
        return self._client.request(
            method='post',
            endpoint=InformationEndpoints.CLIENTS_BONUSES_DELETE,
            headers={'authorization': f'Session {session_id}'},
            json=request.model_dump(exclude_none=True),
        )
