"""
В этом файле реализованы функции, направленные на получение токена доступа для незарегистрированных пользователей.
"""

import json
import re
import requests
from configs.config import Config
from utils.endpoints import Authorization
from utils.signature import get_signature
from utils.request_logger import live_format_request_response
from typing import Optional
#import logging

class APIAuth:
    def __init__(self, make_uuid: str):
            self.base_url = Config.BASE_URL
            self.session = requests.Session()
            self.make_uuid = make_uuid # Генерируем uuid и передаем в функции авторизации и генерации сигнатуры
            self.headers = {
                # "signature": get_signature(),
                "User-Agent": Config.USER_AGENT,
                "platform": Config.PLATFORM,
                "manufacturer": Config.MANUFACTURER,
                "language": Config.LANGUAGE,
                "project": Config.PROJECT,
                "uuid": self.make_uuid,
                # "chain": Config.CHAIN,
                # "branch": Config.BRANCH,
                "token-authorization": Config.TOKEN_AUTHORIZATION,
                "token-device": Config.TOKEN_DEVICE,
                "city": Config.CITY,
                "account": Config.ACCOUNT_ID
            }
            self.refresh_signature(uuid=make_uuid)

    def extract_signature(self, response_text: str) -> Optional[str]:
        """
        Извлекает signature из ответа сервера вида:
        string(115) "signature: <новая сигнатура>"

        :param response_text: Текст сигнатуры из ответа сервера
        :type response_text: str
        :return: Optional[str]
        """
        match = re.search(r'signature:\s*([a-f0-9]+)', response_text)
        return match.group(1) if match else None
    
    def refresh_signature(self, uuid: str, token_access: Optional[str] = None) -> str:
        """Генерируем новую signature перед КАЖДЫМ запросом
        
        :param uuid: Генерация и передача в эту функцию UUID
        :type uuid: str
        :param token_access: Из ответа сервера записывается access-token и передается этой функции
        :type token_access: Optional[str]
        :return: str
        """
        sig = get_signature(token_access=token_access, uuid=uuid)
        self.headers["signature"] = sig
        return sig

    def get_access_token(self, make_uuid: str) -> str:
        """
            Получение токена доступа с автоматической обработкой динамической сигнатуры
            
            :param make_uuid: Генерация и передача в функцию uuid
            :type make_uuid: str
            :return: str
        """
        url = f"{self.base_url}{Authorization.APPLICATION.value}?action=authorization"
        max_attempts = 1 #количество попыток
        # print("Headers перед запросом:", self.headers)
        for _ in range(0, max_attempts):
            self.refresh_signature(uuid=make_uuid)
            try:
                response = self.session.post(url, headers=self.headers, timeout=10)
            except requests.RequestException as e:
                raise RuntimeError(f"[AUTH] HTTP error:\n{e}")
            
            live_format_request_response(response)

            try:
                data=response.json()
            except json.JSONDecodeError:
                raise ValueError(f"[AUTH] Ответ не JSON: {response.text}")

            # Если пришла ошибка "Неправильная подпись", обновляем сигнатуру
            if data.get("status") == "error" and "Неправильная подпись" in response.text:
                extracted = self.extract_signature(response_text=response.text)
                if extracted:
                    self.headers["signature"] = extracted
                    continue
                else:
                    raise RuntimeError("[AUTH] Не удалось извлечь новую signature")
            
            if data.get("status") == "success":
                return data["data"]["access_token"]

        raise RuntimeError("[AUTH] Authorization failed после повторной попытки")