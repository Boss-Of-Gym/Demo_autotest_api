import httpx

from enums.endpoints import InformationEndpoints
from services.base import BaseService


class BlackListFieldsService(BaseService):
    def get_black_list_fields(self, session_id: str) -> httpx.Response:
        return self._client.request(
            method='get',
            endpoint=InformationEndpoints.BLACK_LIST_FIELDS,
            headers={'authorization': f'Session {session_id}'},
        )
