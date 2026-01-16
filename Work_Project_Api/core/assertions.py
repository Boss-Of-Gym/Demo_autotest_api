"""
Файл основных проверок - Проверка статус кода, статуса в теле ответе, валидация ответа, значение заголовка content-type
"""
import requests
from typing import Type
from pydantic import BaseModel, ValidationError

@staticmethod
def assert_status_code(response: requests.Response, expected_status: int) -> None:
    """
        Проверка кода статуса ответа сервера
          
        :param response: Полный ответ сервера
        :type response: requests.Response
        :param expected_status: Ожидаемый статус код сервера
        :type expected_status: int
    """
    assert response.status_code == expected_status, f"Ожидался код {expected_status}, а вернулся {response.status_code}"

@staticmethod
def assert_status_in_body(status_body: str, response: requests.Response) -> None:
    """
        Проверка статуса ответа, который находится в теле
            
        :param status_body: Ожидаемый статус ответа
        :type status_body: str
        :param response: Полный ответ сервера
        :type response: requests.Response
    """
    data = response.json()
    assert data["status"] == status_body, (
        f"Ожидался статус - {status_body}, а вернулся {data['status']}. "
        f"Код ошибки - {data['error']['code']}. "
        f"Описание ошибки - {data['error']['description']}"
    )

@staticmethod
def assert_content_type(response: requests.Response, expected_content_type: str) -> None:
    """
        Проверка что заголовок Content-Type соответствует ожидаемому формату
            
        :param response: Объект ответа от requests
        :type response: requests.Response
        :param expected_content_type: Ожидаемый формат (например 'application/json')
        :type expected_content_type: str
    """
    actual_content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
    assert actual_content_type == expected_content_type, (
        f'Ожидалось, что ответ вернулся в формате {expected_content_type}, '
        f"но вернулся формат {actual_content_type}"
    )

@staticmethod
def assert_scheme_response(response: requests.Response, scheme: Type[BaseModel]) -> None:
    """
        Проверка схемы ответа
            
        :param response: Ответ сервера
        :type response: requests.Response
        :param scheme: Ожидаемая схема ответа, которая сверяется с ответом сервера
        :type scheme: Type[BaseModel]
    """
    try:
        scheme.model_validate(response.json())
    except ValidationError as e:
        raise AssertionError(f"Ответ сервера не соответствует схеме:\n{e}")