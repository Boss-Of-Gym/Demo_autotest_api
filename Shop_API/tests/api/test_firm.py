import allure
import re
import pytest
from configs.config import Config
from pages.firm_page import FirmPage
from fixtures.api import (
    random_values_for_other_task, random_location, random_location_and_order_status
    )

# Используем фикстуру root_dir для тестового имени (если нужно)

@allure.epic('Shop')
@allure.feature(f'{Config.APP_ENV}')
@allure.suite('Проверка Firm методов')
class TestFirm():


    @pytest.mark.parametrize(
        "action, description, test_id",
        [
            pytest.param("about", "Метод (about) - возвращает email филиала, реквизиты", "shop_firm_002", 
                        marks=pytest.mark.smoke),
            pytest.param("init", "Метод (init) - возвращает настройки темы, ссылки на приложения", "shop_firm_003", 
                        marks=[pytest.mark.smoke]),
            pytest.param("settings", "Mетод (settings) - настроки темы для сайта", "shop_firm_004", 
                        marks=[pytest.mark.smoke])
        ]
    )
    @allure.title("Данные филиала")
    @allure.tag('firm_application', 'post')
    def test_firm_application(self, auth_headers, description, action, test_id):
        allure.dynamic.label('Test_ID', test_id)
        allure.dynamic.description(description)
        firm_page = FirmPage(Config.BASE_URL, auth_headers)

        with allure.step(f"Отправка запроса на {firm_page.base_url}{firm_page.post.__name__}"):
            response = firm_page.post_application(action=action)
            allure.attach(
                response.text,
                name="Ответ сервера firm_application_about",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step(f"Проверка статуса и данных для метода {action}"):
            assert response.status_code == 200, f"Ожидался код 200, а вернулся {response.status_code}"
            data = response.json()
            assert data["status"] == "success", (
                f"Ожидался статус - success, а вернулся {data['status']}. "
                f"Код ошибки - {data["error"]["code"]}. "
                f"Описание ошибки - {data["error"]["description"]}"
            )
        with allure.step(f"Проверка наличия и валидации полей метода - {action}"):
            firm_page.validation_fields_application(data=data, action=action)


    @pytest.mark.smoke
    @allure.title("возвращает информацию об филиале, категория блюд, список блюд")
    @allure.tag('firm_branch', 'get')
    @allure.description(
        "возвращает информацию об филиале, категория блюд, список блюд, данные из таблиц: " \
        "firms_branches, firms_chains, map_zones.automations, vacancies, firms_categories, firms_special_offers, ..."
        )
    def test_firm_branch(self, auth_headers):
        allure.dynamic.label('Test_ID', 'shop_firm_007')
        firm_page = FirmPage(Config.BASE_URL, auth_headers)

        with allure.step(f"Отправка запроса на {firm_page.base_url}{firm_page.post.__name__}"):
            response = firm_page.get_branch()
            allure.attach(
                response.text,
                name="Ответ сервера firm_branch",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step("Проверка статуса и данных"):
            firm_page.assert_status_code(response=response, expected_status=200)

            data = response.json()
            assert data["status"] == "success", (
                f"Ожидался статус - success, а вернулся {data['status']}. "
                f"Код ошибки - {data["error"]["code"]}. "
                f"Описание ошибки - {data["error"]["description"]}"
                )
            assert isinstance(data, dict), f"Ожидался dict, получили {type(data)}"
            assert "data" in data
        
        with allure.step("Валидация полной структуры и типов всех полей"):
            firm_page.validation_fields_branch(data=data)


    @pytest.mark.parametrize(
        "action, description, test_id",
        [
            pytest.param("default", "метод (default) возвращает сообщение для филиала у которого включен chat", "shop_firm_008",
                        marks=[pytest.mark.smoke, pytest.mark.chat]),
            pytest.param("message_statuses", "метод (message_statuses) возвращает статусы для id сообщений", "shop_firm_009",
                        marks=[pytest.mark.smoke, pytest.mark.chat]),
            pytest.param("send_message", "метод (send_message) создает новое сообщение, возвращает статус сообщения", "shop_firm_010",
                        marks=[pytest.mark.smoke, pytest.mark.chat]),
            pytest.param("send_image", "метод (send_image) отправляет новое изображение в чат, возвращает статус сообщения", "shop_firm_011",
                        marks=[pytest.mark.smoke, pytest.mark.chat])
        ]
    )
    @allure.title("управление сообщениями")
    @allure.tag('firm_chat', 'post')
    def test_firm_chat(self, auth_headers, test_id, description, action):
        allure.dynamic.label('Test_ID', test_id)
        allure.dynamic.description(description)
        firm_page = FirmPage(Config.BASE_URL, auth_headers)

        with allure.step(f"Отправка запроса на {firm_page.base_url}{firm_page.post.__name__}"):
            response = firm_page.post_chat(action=action)
            allure.attach(
                response.text,
                name="Ответ сервера firm_chat",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step(f"Проверка статуса и данных метода - {action}"):
            firm_page.assert_status_code(response=response, expected_status=200)

            data = response.json()
            assert data["status"] == "success", (
                f"Ожидался статус - success, а вернулся {data['status']}. "
                f"Код ошибки - {data["error"]["code"]}. "
                f"Описание ошибки - {data["error"]["description"]}"
                )


    @pytest.mark.smoke
    @pytest.mark. parametrize(
        "action, description, test_id",
        [
            pytest.param("info", "для курьера из текущей сессий возвращается информация", "shop_firm_012",
                        marks=[pytest.mark.smoke, pytest.mark.courier]),
            pytest.param("orders", "метод (orders) список заказов текущего курьера", "shop_firm_013",
                        marks=[pytest.mark.smoke, pytest.mark.courier]),
            pytest.param("set_order_status", "метод (set_order_status) меняет статус заказа (по order_id на status)", "shop_firm_014",
                        marks=[pytest.mark.smoke, pytest.mark.courier]),
            pytest.param("take_orders", "метод (take_orders) взять заказ, привязывает текущего курьера", "shop_firm_015",
                        marks=[pytest.mark.smoke, pytest.mark.courier]),
            pytest.param("release_orders", "метод (release_orders) освободить заказ, отвязывает текущего курьера от заказов", "shop_firm_016", 
                        marks=[pytest.mark.smoke, pytest.mark.courier]),
            pytest.param("set_current_location", "метод (set_current_location) установить текущее местоположение", "shop_firm_017",
                        marks=[pytest.mark.smoke, pytest.mark.courier]),
            pytest.param("set_telemetry_history", "метод (set_telemetry_history) запись координат последнего заказа со статусом в историю курьера, добавляет запись в таблицу история движения курьера", "shop_firm_018",
                        marks=[pytest.mark.smoke, pytest.mark.courier]),
            pytest.param("sign_out", "метод (sign_out) выход курьера из системы", "shop_firm_019",
                        marks=[pytest.mark.smoke, pytest.mark.courier])
        ]
    )
    @allure.title("Метод управления курьером")
    @allure.tag('firm_couriers', 'get', 'post')
    def test_firm_couriers(self, courier_session_headers, action, description, test_id, random_values_for_other_task, random_location, random_location_and_order_status):
        allure.dynamic.label('Test_ID', test_id)
        allure.dynamic.description(description)
        firm_page = FirmPage(Config.BASE_URL, courier_session_headers)

        with allure.step(f"Отправка запроса на {firm_page.base_url}{firm_page.post.__name__}"):
            if action == "info":
                response = firm_page.get_couriers(action=action)
            else:
                response = firm_page.post_couriers(
                    action=action, status_order=random_values_for_other_task["set_order_status"], order_id=random_values_for_other_task["random_number_for_test_thousend"], current_location=random_location,
                    telemetry_history=random_location_and_order_status
                    )
            allure.attach(
                response.text,
                name="Ответ сервера firm_couriers",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step(f"Проверка статуса и данных метода - {action}"):
            firm_page.assert_status_code(response=response, expected_status=200)

            data = response.json()
            assert data["status"] == "success", (
                f"Ожидался статус - success, а вернулся {data['status']}. "
                f"Код ошибки - {data["error"]["code"]}. "
                f"Описание ошибки - {data["error"]["description"]}"
                )
            assert "data" in data, f"Ожидалось, что data присутствует в {data}"

        with allure.step(f"Проверка валидации полей метода - {action}"):
            if action == "info":
                firm_page.validation_fields_couriers(data=data)
            elif action == "orders":
                firm_page.validation_fields_couriers_orders(data=data)


    @pytest.mark.parametrize(
            "action, description, test_id",
            [
                pytest.param("complaint", "добавляет запись со статусом problem", "shop_firm_021",
                            marks=[pytest.mark.smoke, pytest.mark.feedback]),
                pytest.param("cache_fields_default", "метод (cache_fields_default) возвращает кэш-поля по умолчанию из переданных параметров", "shop_firm_022",
                            marks=[pytest.mark.smoke, pytest.mark.feedback]),
                pytest.param("default", "метод (default) возвращает список ответов на вопросы обратной связи для текущего филиала", "shop_firm_023",
                            marks=[pytest.mark.smoke, pytest.mark.feedback]),
                pytest.param("orders", "метод (orders) результаты заполнения формы обратной связи", "shop_firm_024",
                            marks=[pytest.mark.smoke, pytest.mark.feedback]),
                pytest.param("new", "метод (new) добавляет запись обратной связи", "shop_firm_025",
                            marks=[pytest.mark.xfail(reason="Код ошибки 124, Описание - Для клиента не найден заказ за последние 3 дня"), pytest.mark.smoke, pytest.mark.feedback])
            ]
    )
    @allure.title("Обратная связь")
    @allure.tag('firm_feedback', 'get', 'post')
    def test_firm_feedback(self, auth_headers, action, description, test_id, random_values_for_other_task):
        allure.dynamic.label('Test_ID', test_id)
        allure.dynamic.description(description)
        firm_page = FirmPage(Config.BASE_URL, auth_headers)

        with allure.step(f"Отправка запроса на {firm_page.base_url}{firm_page.post.__name__}"):
            if action == "complaint":
                response = firm_page.get_feedback(action=action, message=random_values_for_other_task["text_for_key_test"], feedback_id=random_values_for_other_task["random_number_for_test_ten"])
            else:
                response = firm_page.post_feedback(
                    numbrs=random_values_for_other_task["random_number_for_test_ten"], secound_number=random_values_for_other_task["random_number_for_test_secound_field"], 
                    order_id=random_values_for_other_task["random_number_for_test_thousend"], text_new=random_values_for_other_task["text_for_key_test"], 
                    order_status=random_values_for_other_task["set_feedback_status"], action=action
                    )
            allure.attach(
                response.text,
                name="Ответ сервера firm_feedback",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step(f"Проверка статуса и данных для метода - {action}"):
            firm_page.assert_status_code(response=response, expected_status=200)

            data = response.json()
            assert data["status"] == "success", (
                f"Ожидался статус - success, а вернулся {data['status']}. "
                f"Код ошибки - {data["error"]["code"]}. "
                f"Описание ошибки - {data["error"]["description"]}"
                )
            assert "data" in data
        if action == "default":
            with allure.step(f"Проверка и валидация полей ответа метода - {action}"):
                firm_page.validation_fields_feedback_default(data=data)
        elif action == "orders":
            with allure.step(f"Проверка валидации ответа метода - {action}"):
                firm_page.validation_fields_feedback_orders(data=data)


    @pytest.mark.smoke
    @allure.title("Геокодирование")
    @allure.tag('firm_geocoding', 'get')
    @allure.description("возвращает сервисы поиска координат или поиск мест по координатам (обратное геокодирование)")
    def test_firm_geocoding(self, auth_headers):
        allure.dynamic.label('Test_ID', 'shop_firm_026')
        firm_page = FirmPage(Config.BASE_URL, auth_headers)

        with allure.step(f"Отправка запроса на {firm_page.base_url}{firm_page.post.__name__}"):
            response = firm_page.get_geocoding()
            allure.attach(
                response.text,
                name="Ответ сервера firm_geocoding",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step("Проверка статуса и данных"):
            firm_page.assert_status_code(response=response, expected_status=200)

            data = response.json()
            assert data["status"] == "success", (
                f"Ожидался статус - success, а вернулся {data['status']}. "
                f"Код ошибки - {data["error"]["code"]}. "
                f"Описание ошибки - {data["error"]["description"]}"
                )
            assert "data" in data
        with allure.step("Проверка валидации полей"):
            firm_page.validaion_fields_geocoding(data=data)


    @pytest.mark.smoke
    @allure.title("Список стран")
    @allure.tag('firm_locations', 'get')
    @allure.description("список стран с регионами в них")
    def test_firm_locations(self, auth_headers):
        allure.dynamic.label('Test_ID', 'shop_firm_027')
        firm_page = FirmPage(Config.BASE_URL, auth_headers)

        with allure.step(f"Отправка запроса на {firm_page.base_url}.{firm_page.post.__name__}"):
            response = firm_page.get_locations()
            allure.attach(
                response.text,
                name="Ответ сервера firm_locations",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step("Проверка статуса и данных"):
            firm_page.assert_status_code(response=response, expected_status=200)

            data = response.json()
            assert data["status"] == "success", (
                f"Ожидался статус - success, а вернулся {data['status']}. "
                f"Код ошибки - {data["error"]["code"]}. "
                f"Описание ошибки - {data["error"]["description"]}"
                )
            assert "data" in data
        with allure.step("Проверка валидации полей"):
            firm_page.validation_fields_locations(data=data)





