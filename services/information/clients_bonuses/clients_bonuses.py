import httpx

from enums.endpoints import InformationEndpoints
from services.base import BaseService


class ClientsBonusesService(BaseService):
    def get_clients_bonuses(self, session_id: str) -> httpx.Response:
        return self._client.request(
            method='get',
            endpoint=InformationEndpoints.CLIENTS_BONUSES,
            headers={'authorization': f'Session {session_id}'},
        )
