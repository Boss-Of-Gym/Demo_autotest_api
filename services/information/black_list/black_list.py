import httpx

from enums.endpoints import InformationEndpoints
from services.base import BaseService


class BlackListService(BaseService):
    def get_black_list(self, session_id: str) -> httpx.Response:
        return self._client.request(
            method='get',
            endpoint=InformationEndpoints.BLACK_LIST,
            headers={'authorization': f'Session {session_id}'},
        )
