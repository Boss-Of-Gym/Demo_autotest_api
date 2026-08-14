import httpx

from enums.endpoints import InformationEndpoints
from schemas.information.black_list.add.request import BlackListAddRequest
from services.base import BaseService


class BlackListAddService(BaseService):
    def post_black_list_add(
        self,
        session_id: str,
        request: BlackListAddRequest,
    ) -> httpx.Response:
        return self._client.request(
            method='post',
            endpoint=InformationEndpoints.BLACK_LIST_ADD,
            headers={'authorization': f'Session {session_id}'},
            json=request.model_dump(exclude_none=True),
        )
