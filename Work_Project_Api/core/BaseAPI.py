"""
Базовый файл с основным методом отправки запросов
"""

import requests
import allure
import json
from typing import Dict, Optional

class HTTPClient:
    """
    Базовый класс для всех вызовов API страниц
    Здесь будут храниться основные методы которые используются во всех страницах вызова
    """

    def __init__(self, base_url: str, headers: Dict[str, str] | None = None, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(headers or {})

    def request(
            self,
            method: str,
            endpoint: str,
            *,
            json: Optional[Dict[str, str]] | None = None,
            data: Optional[Dict[str, str]] | None = None,
            files: Optional[Dict[str, str]] | None = None,
            params: Optional[Dict[str, str]] | None = None
            ) -> requests.Response:
        """
        Docstring для post
        
        :param method: Добавляем метод запроса
        :type method: str
        :param endpoint: Эндпоинт необходимого метода, например /client
        :type endpoint: str
        :param json: Тело запроса (json формат)
        :type json: Optional[Dict[str, str]] | None
        :param data: Тело запроса (не формат json)
        :type data: Optional[Dict[str, str]] | None
        :param files: Файл передаваемый при загрузке чего-либо (например изображений)
        :type files: Optional[Dict[str, str]] | None
        :param params: Параметр необходимого метода, например ?action="example"
        :type params: Optional[Dict[str, str]] | None
        """
        url = f"{self.base_url}{endpoint}"
                
        with allure.step(f"{method.upper()} {endpoint}"):
            response = self.session.request(
                method=method,
                url=url,
                json=json,
                data=data,
                files=files,
                params=params,
                timeout=self.timeout
                )

            self.log_request_response(response)

            return response

    def log_request_response(self, response: requests.Response):
        request = response.request

        safe_headers = self._mask_sensitive_headers(dict(request.headers))

        allure.attach(
            body=json.dumps({
                "method": request.method,
                "url": request.url,
                "headers": safe_headers,
                "body": self._safe_json(request.body)
            }, indent=2, ensure_ascii=False
            ),
            name="request",
            attachment_type=allure.attachment_type.JSON
        )

        try:
            body = response.json()
            allure.attach(
                json.dumps(body, indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
        except Exception:
            allure.attach(
                response.text,
                name="Response Body (text)",
                attachment_type=allure.attachment_type.TEXT
            )
    
    def _mask_sensitive_headers(self, headers: dict) -> dict:
        """
        Маскируем секретные значения в заголовках перед логированием
        """
        sensitive_keys = ["Authorization", "token-authorization", "token-access", "session", "token-device", "signature"]
        masked = headers.copy()
        for key in sensitive_keys:
            for header in masked:
                if header.lower() == key.lower():
                    masked[header] = "*****"  # заменяем на звездочки
        return masked

    def _safe_json(self, body):
        if not body:
            return None
        try:
            return json.loads(body)
        except Exception:
            return str(body)
