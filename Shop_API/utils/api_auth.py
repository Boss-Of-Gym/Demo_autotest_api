"""
Авторизация в API через /application.authorization с использованием Playwright-эмуляции
для получения реального reCAPTCHA v3 токена.

Поведение:
- Получаем token через RecaptchaBrowserService
- Если token получен — выполняем POST авторизации
- Если token не получен — бросаем RuntimeError (чтобы не продолжать тесты с неверной капчей)
- После успешной авторизации сохраняем в session.headers: token-access и Authorization
"""

import json
import re
import requests
from configs.config import Config
from utils.endpoints import Authorization
from utils.signature import get_signature
from utils.request_logger import live_format_request_response

class APIAuth:
    def __init__(self):
            self.base_url = Config.BASE_URL
            self.headers = {
                "signature": get_signature(),
                "platform": Config.PLATFORM,
                "manufacturer": Config.MANUFACTURER,
                "language": Config.LANGUAGE,
                "project": Config.PROJECT,
                "uuid": Config.UUID,
                "chain": Config.CHAIN,
                "branch": Config.BRANCH,
                "token-authorization": Config.TOKEN_AUTHORIZATION,
                "token-device": Config.TOKEN_DEVICE
            }

    def extract_signature(self, response_text: str) -> str:
        """
        Извлекает signature из ответа сервера вида:
        string(115) "signature: <новая сигнатура>"
        """
        match = re.search(r'signature:\s*([a-f0-9]+)', response_text)
        if match:
            return match.group(1)
        return None
    
    def refresh_signature(self, token_access: str = None) -> str:
        """Генерируем новую signature перед КАЖДЫМ запросом"""
        new_sig = get_signature(token_access=token_access)
        self.headers["signature"] = new_sig
        return new_sig

    def get_access_token(self) -> str:
        """
            Получение токена доступа с автоматической обработкой динамической сигнатуры
        """
        url = f"{self.base_url}{Authorization.application}?action=authorization"
        # print("Headers перед запросом:", self.headers)
        for attempt in range(2):  # максимум 2 попытки
            self.refresh_signature()
            response = requests.post(url, headers=self.headers)

            # Если пришла ошибка "Неправильная подпись", обновляем сигнатуру
            if "Неправильная подпись" in response.text:
                extracted = self.extract_signature(response.text)
                if extracted:
                    print(f"[AUTH] Обнаружена новая signature: {extracted}")
                    self.headers["signature"] = extracted
                    continue  # повторяем запрос с новой сигнатурой
                else:
                    raise Exception("[AUTH] Не удалось извлечь новую signature")
                
            # Пробуем получить access_token
            try:
                data = response.json()
            except json.JSONDecodeError:
                raise Exception(f"[AUTH] Ответ не является JSON: {response.text}")

            if data.get("status") != "success":
                raise Exception(f"Authorization failed: {data}")
            
            token = data["data"]["access_token"]
            return token
        raise Exception("[AUTH] Authorization failed после повторной попытки")