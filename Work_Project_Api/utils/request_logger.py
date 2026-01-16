"""
Файл логирования запросов и ответов в читаемом формате
"""
import json
from datetime import datetime
import allure

SENSITIVE_HEADERS = {
    "authorization", 
    "token-access",
    "access-token",
    "token-authorization", 
    "signature", 
    "uuid",
    "recaptcha_token", 
    "cookie", 
    "set-cookie", 
    "x-api-key",
    "session",
    "session_id"
}
MAX_BODY_LOG = 10_000

def _mask_header_value(name: str, value: str) -> str:
    """
    Скрывает заголовки имя которых содержится в словаре - SENSITIVE_HEADERS

    :param name: Название (ключ) заголовка
    :type name: str
    :param value: Значение заголовка
    :type value: str
    :return: str
    """
    if value is None:
        return ""
    if name.lower() in SENSITIVE_HEADERS or len(value) > 100:
        return "****"
    return value

SENSITIVE_FIELDS = {
    "login",
    "password",
    "pass",
    "pwd",
    "captcha",
    "token",
    "access_token",
}

def _mask_body(body: str, mask_access_token: bool = False) -> str:
    """
    Маскирует чувствительные поля в JSON-теле.
    Работает рекурсивно, если в теле вложенные структуры.

    :param body: Тело ответа в формате текста
    :type body: str
    :return: str
    """

    def mask(value):
        """Возвращает замаскированное значение."""
        return "***"

    def recursive_mask(obj):
        """Рекурсивная маскировка любых вложенных структур."""
        if isinstance(obj, dict):
            return {
                k: mask(v) if k.lower() in SENSITIVE_FIELDS else recursive_mask(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [recursive_mask(i) for i in obj]
        else:
            return obj

    try:
        parsed = json.loads(body)
        masked = recursive_mask(parsed)
        return json.dumps(masked, ensure_ascii=False, indent=2)
    except Exception:
        # если body не JSON — вернуть как есть
        return body

def _truncate(text: str) -> str: #limit: int = MAX_BODY_LOG
    if text is None:
        return ""
    else:
        return text #if len(text) <= limit else text[:limit] + f"\n...[truncated {len(text)-limit} bytes]..."

def _safe_text(obj) -> str:
    if obj is None:
        return ""
    if isinstance(obj, (bytes, bytearray)):
        try:
            return obj.decode("utf-8", errors="replace")
        except Exception:
            return f"<binary {len(obj)} bytes>"
    return str(obj)

def live_format_request_response(resp, mask_access_token: bool = False) -> str:
    """
    Логирование в понятном, читаемом формате, которое прикрепляется к отчету Alure CLI
    
    :param resp: Ответ сервера в формате request.Response (Можно также использовать httpx.Response)
    :type resp: request.Response
    :param mask_access_token: Если в теле или заголовке есть access-token - маскируем
    :type mask_access_token: bool
    :return: str
    """
    req = resp.request
    lines = ["\n===== HTTP TRACE START ====="]
    lines.append(f"{req.method} {req.url}")

    # Заголовки запроса
    lines.append("Request headers:")
    for k, v in (req.headers or {}).items():
        lines.append(f"  {k}: {_mask_header_value(k, v)}")

    # Тело запроса
    body = getattr(req, "body", None)
    if body:
        text = _safe_text(body)
        text = _mask_body(text, mask_access_token)  # маскировка чувствительных полей
        lines.append("Request body:")
        lines.append(_truncate(text))
    else:
        lines.append("Request body: <empty>")

    # Ответ
    lines.append("\nResponse:")
    lines.append(f"HTTP {resp.status_code}")
    lines.append("Response headers:")
    for k, v in (resp.headers or {}).items():
        lines.append(f"  {k}: {_mask_header_value(k, v)}")

    resp_text = _safe_text(resp.text)
    # маскируем токены и подписи в ответе
    resp_text = _mask_body(resp_text, mask_access_token)
    lines.append("Response body:")
    lines.append(_truncate(resp_text))

    lines.append(f"Logged at: {datetime.now().isoformat()}")
    lines.append("===== HTTP TRACE END =====\n")

    content = "\n".join(lines)
    print(content)  # вывод в консоль
    try:
        allure.attach(content, name="HTTP live trace", attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass

    return resp
