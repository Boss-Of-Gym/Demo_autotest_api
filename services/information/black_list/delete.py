import httpx

from enums.endpoints import InformationEndpoints
from schemas.information.black_list.delete.request import BlackListDeleteRequest
from services.base import BaseService


class BlackListDeleteService(BaseService):
    def post_black_list_delete(
        self,
        session_id: str,
        request: BlackListDeleteRequest,
    ) -> httpx.Response:
        return self._client.request(
            method='post',
            endpoint=InformationEndpoints.BLACK_LIST_DELETE,
            headers={'authorization': f'Session {session_id}'},
            json=request.model_dump(exclude_none=True),
        )
