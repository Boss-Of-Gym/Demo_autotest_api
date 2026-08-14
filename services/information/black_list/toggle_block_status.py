import httpx

from enums.endpoints import InformationEndpoints
from schemas.information.black_list.toggle_block_status.request import BlackListToggleBlockStatusRequest
from services.base import BaseService


class BlackListToggleBlockStatusService(BaseService):
    def post_black_list_toggle_block_status(
        self,
        session_id: str,
        request: BlackListToggleBlockStatusRequest,
    ) -> httpx.Response:
        return self._client.request(
            method='post',
            endpoint=InformationEndpoints.BLACK_LIST_TOGGLE_BLOCK_STATUS,
            headers={'authorization': f'Session {session_id}'},
            json=request.model_dump(exclude_none=True),
        )
