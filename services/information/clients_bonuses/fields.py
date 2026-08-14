import httpx

from enums.endpoints import InformationEndpoints
from services.base import BaseService


class ClientsBonusesFieldsService(BaseService):
    def get_clients_bonuses_fields(self, session_id: str) -> httpx.Response:
        return self._client.request(
            method='get',
            endpoint=InformationEndpoints.CLIENTS_BONUSES_FIELDS,
            headers={'authorization': f'Session {session_id}'},
        )
