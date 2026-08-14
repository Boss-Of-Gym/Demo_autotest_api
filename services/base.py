from core.client import BaseHTTPClient


class BaseService:
    def __init__(self, client: BaseHTTPClient) -> None:
        self._client = client
