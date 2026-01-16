import allure
import pytest
from tests.data.test_data_firm import (
    test_data_firm_about
    )
from core.assertions import (
    assert_content_type,
    assert_scheme_response,
    assert_status_code,
    assert_status_in_body
)
from fixtures.api import (
    add_delete_after_cancel,
    prepare_body
    )
from core.BaseAPI import HTTPClient
from typing import Dict, Any, Type
from pydantic import BaseModel, ValidationError
from utils.endpoints import Firm
from scheme.firm_scheme import FirmSpecialOffersGetPromoCodeResponse


@allure.epic('API/WorkProject')
@allure.feature('/firm')
@allure.parent_suite('Проверка Firm методов')
class TestFirm():

    @pytest.mark.parametrize(
            "method, endpoint, params, body, description, test_id, expected_results, expected_status_body, " \
            "expected_status_code, expected_scheme, expected_content_type, authorization_user", 
            test_data_firm_about
        )
    @allure.title("Описание филиала фирмы")
    @allure.suite("Проверка всех методов, за исключением методов курьера")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag(
        'firm',
        'about',
        'application',
        'uuid', 
        'branch',
        'chat',
        'document',
        'feedback',
        'geocoding',
        'notification',
        'order',
        'special_offers',
        'vacancies',
        'get',
        'post'
        )
    def test_firm(
        self,
        auth_headers: Dict[str, Any],
        endpoint: str,
        params: Dict[str, Any],
        body: Dict[str, Any],
        description: str,
        test_id: str,
        expected_results: str,
        expected_status_body: str,
        expected_status_code: int,
        expected_scheme: Type[BaseModel],
        expected_content_type: str,
        authorization_user: bool,
        login_with_phone: Dict[str, Any],
        method: str,
        api_client: HTTPClient,
        prepare_body: Dict[str, Any],
        add_delete_after_cancel
        ):
        """
        Docstring для test_firm_about
        
        :param endpoint: Передача endpoint в url
        :type endpoint: str
        :param auth_headers: Стандартные заголовки
        :type auth_headers: Dict[str, Any]
        :param params: Параметры для запроса
        :type params: Dict[str, str]
        :param body: Тело запроса
        :type body: Dict[str, Any]
        :param description: Описание теста
        :type description: str
        :param test_id: ID теста
        :type test_id: str
        :param expected_results: Ожидаемый результат
        :type expected_results: str
        :param expected_status_body: Ожидаемый статус тела ответа
        :type expected_status_body: str
        :param expected_status_code: Ожидаемый статус код в ответе
        :type expected_status_code: int
        :param expected_scheme: Валидация полей и общая схема ответа
        :type expected_scheme: Type[BaseModel]
        :param expected_content_type: Ожидаемый заголовок Content-Type
        :type expected_content_type: str
        :param authorization_user: Авторизация пользователя
        :type authorization_user: bool
        :param login_with_phone: Авторизация пользователя и прикрепление результата session_id к общим заголовкам и передача всех заголовков с session_id в запрос теста
        :type login_with_phone: Dict[str, Any]
        :param method: Метод запроса
        :type method: str
        :param api_client: Заголовки запроса
        :type api_client: HTTPClient
        :param prepare_body: Тело запроса с добавлением order_id
        :type prepare_body: Dict[str, Any]
        :param add_delete_after_cancel: Метод удаления order_id из store при использовании id в запросе
        :type add_delete_after_cancel: int
        """
        allure.dynamic.id(id=test_id)
        allure.dynamic.label("Endpoint", endpoint.value)
        allure.dynamic.description(description)
        allure.dynamic.story(expected_results)
        allure.dynamic.title(f"{endpoint}?{params} | {test_id}")

        headers = login_with_phone if authorization_user else auth_headers
        
        if endpoint.value == "/firm/order":
            headers["pickup"] = "***DEMO***"
            if test_id in ("shop_firm_103_1", "shop_firm_103_2"):
                headers["district"] = "55377"
                
        if test_id == "shop_firm_106":
            headers["pickup"] = ""
        elif test_id == "shop_firm_108":
            headers.pop("pickup")
        elif test_id == "shop_firm_109":
            headers["pickup"] = "pickup"
        elif test_id == "shop_firm_125":
            headers["pickup"] = "0"

        api_client.session.headers.update(headers)

        with allure.step(f"Отправка запроса на GET | {api_client.base_url}{endpoint.value}"):
            if endpoint == Firm.FIRM_CHAT_IMG and params.get("action") == "send_image":
                with open("tests/files/test_img_offers.png", "rb") as f:
                    files = {
                            "image": ("test_image.png", f, "image/png")
                            }
                    response = api_client.request(method=method, endpoint=endpoint.value, params=params, data=body, files=files)
            else:
                json_body = prepare_body(endpoint=endpoint, test_id=test_id, body=body, params=params)
                response = api_client.request(method=method, endpoint=endpoint.value, params=params, json=json_body)

        with allure.step(f"Полная проверка валидации ответа от сервера"):
            assert_status_code(response=response, expected_status=expected_status_code)
            assert_content_type(response=response, expected_content_type=expected_content_type)
            if expected_status_code == 200: 
                assert_status_in_body(response=response, status_body=expected_status_body)
                if expected_scheme == FirmSpecialOffersGetPromoCodeResponse:
                    try:
                        expected_scheme.model_validate(response.json(), context={"expected_promo_code": ["1111"]})
                    except ValidationError as e:
                        raise AssertionError(f"Ответ API не соответствует схеме:\n{e}")
                else:
                    assert_scheme_response(response=response, scheme=expected_scheme)
                
                add_delete_after_cancel["add_order"](
                        endpoint=endpoint,
                        expected_status_body=expected_status_body,
                        response=response
                        )

