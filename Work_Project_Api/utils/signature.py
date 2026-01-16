"""
Файл который генерирует валидные сигнатуры. Каждый тест - новая сигнатура
"""
import hashlib
from configs.config import Config


def is_falsy(value) -> bool:
    """Проверяет, является ли значение 'ложным'."""
    return value is None or value == ''


def remove_falsy_values_from_object(obj: dict) -> dict:
    """
    Удаляет ключи с пустыми ('', None) значениями.
    """
    return {k: v for k, v in obj.items() if not is_falsy(v)}

def get_signature(uuid: str, token_access: str = "") -> str:
    """
    Генерация подписи на основе заголовков

    :param uuid: Передача сгенерированной uuid
    :type uuid: str
    :param token_access: Использование token_access в генерации сигнатуры, если сервер вернул его значение
    :type token_access: str
    :return: str
    """

    # формируем словарь в строго заданном порядке
    values = {
        'user-agent': Config.USER_AGENT,
        # 'BranchID': Config.BRANCH,
        # 'ChainID': Config.CHAIN,
        'account': Config.ACCOUNT_ID,
        'city': Config.CITY,
        'Platform': Config.PLATFORM,
        'UUID-Device': uuid,
        'Manufacturer': Config.MANUFACTURER,
        'Project': Config.PROJECT,
        'Token-Access': token_access,
        'Token-Device': Config.TOKEN_DEVICE,
        'Token-Authorization': Config.TOKEN_AUTHORIZATION
    }

    # print(values)

    # Удаляем пустые значения
    cleaned = remove_falsy_values_from_object(values)

    # Склеиваем значения через "::", исключая '0'
    joined_data = "::".join(
        str(v).strip() for v in cleaned.values() if str(v).strip() != '0'
    )

    # print(joined_data)

    if not joined_data:
        return ''

    # Делим строку пополам
    middle = len(joined_data) // 2

    # Хэш-функции
    def sha1(data: str) -> str:
        return hashlib.sha1(data.encode('utf-8')).hexdigest()

    def sha256(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    # Генерация подписи
    signature = (
        sha256(sha1(joined_data) + sha1(joined_data[:middle]))
        + sha1(joined_data[middle: middle * 2])
    )

    # print(signature)

    return signature