import random
import pytest
from configs.config import Config
from mimesis import Person, Text
from scheme.firm_scheme import (
    SuccessResponse,
    ErrorData,
    FirmApplicationAboutResponse,
    FirmApplicationInitResponse,
    FirmApplicationSettingsResponse,
    FirmBranchResponse,
    FirmChatMesasageStatusesResponse,
    FirmFeedbackCFDResponse,
    FirmFeedbackDefaultResponse,
    FirmFeedbackOrdersResponse,
    FirmGeocodingResponseResponse,
    FirmNotificationsResponse,
    FirmOrderResponse,
    FirmSpecialOffersResponse,
    FirmSpecialOffersGetPromoCodeResponse,
    FirmVacanciesGetResponse,
    SuccessResponseSecound,
    FirmDocumentResponse
)
from utils.endpoints import Firm

test_data_firm_about = [
                #==========firm/application?action=about==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "about"},
                        {},
                        "Авторизированный пользователь. Метод (about) - возвращает email филиала, реквизиты",
                        "shop_firm_006",
                        "Успешно возвращает email филиала и реквизиты",
                        "success",
                        200,
                        FirmApplicationAboutResponse,
                        "application/json",
                        True,
                        marks=pytest.mark.smoke
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "about"},
                        {},
                        "Неавторизованный пользователь. Метод (about) - возвращает email филиала, реквизиты",
                        "shop_firm_007",
                        "Успешно возвращает email филиала и реквизиты",
                        "success",
                        200,
                        FirmApplicationAboutResponse,
                        "application/json",
                        False,
                        marks=pytest.mark.smoke
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "about"},
                        {"extra": "&lt;script&gt;alert('wow')&lt;/script&gt;"},
                        "Лишние поля в теле",
                        "shop_firm_008",
                        "Успешно возвращает email филиала и реквизиты",
                        "success",
                        200,
                        FirmApplicationAboutResponse,
                        "application/json",
                        True,
                        marks=pytest.mark.regression
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "aboutt"},
                        {},
                        "Несуществующий метод",
                        "shop_firm_009",
                        "Возвращается ошибка с кодом 6 - Данного метода не существует",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=pytest.mark.regression
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": ""},
                        {},
                        "Несуществующий метод",
                        "shop_firm_010",
                        "Возвращается ошибка с кодом 6 - Данного метода не существует",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=pytest.mark.regression
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "about; DROP TABLE"},
                        {},
                        "Несуществующий метод",
                        "shop_firm_011",
                        "Возвращается ошибка с кодом 6 - Данного метода не существует",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=pytest.mark.regression)
                ),
                #==========firm/application?action=init==========
                # Изменить ожидаемый результат при смене заголовка platform
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "init"},
                        {"social_id": 5678, "type": "universal"},
                        "Метод (init) - возвращает настройки темы, ссылки на приложения. Social_id и type для platform == android/ios",
                        "shop_firm_012",
                        "Возвращается ошибка с кодом 16 - Неправильный домен",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.smoke,
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "init"},
                        {},
                        "Метод (init) - возвращает настройки темы, ссылки на приложения. Пустое тело для platform == site",
                        "shop_firm_012_1",
                        "Успешно возвращает настройки темы, ссылки на приложения",
                        "success",
                        200,
                        FirmApplicationInitResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.smoke,
                            pytest.mark.regression
                            ]
                        )
                ),
                #==========firm/application?action=settings==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION,
                        {"action": "settings"},
                        {},
                        "Mетод (settings) - настроки темы для сайта",
                        "shop_firm_013",
                        "Успешно возвращает настройки темы для сайта",
                        "success",
                        200,
                        FirmApplicationSettingsResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Код ошибки 103, Описание - Не удается добавить адрес"),
                            pytest.mark.smoke
                            ]
                        )
                ),
                #==========firm/application/uuid?action=registration==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION_UUID,
                        {"action": "registration"},
                        {},
                        "Авторизованный пользователь. Добавляем новый токен (таблица clients_tokens) или обновляем старую запись профиля (таблица clients_sessions)",
                        "shop_firm_014",
                        "Успешно добавляется новый токен или обновляется старая запись профиля",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        True,
                        marks=pytest.mark.smoke
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION_UUID,
                        {"action": "registration"},
                        {},
                        "Неавторизованный пользователь. Добавляем новый токен (таблица clients_tokens) или обновляем старую запись профиля (таблица clients_sessions)",
                        "shop_firm_015",
                        "Успешно добавляется новый токен или обновляется старая запись профиля",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        False,
                        marks=pytest.mark.smoke
                        )
                ),
                #==========firm/application/uuid?action=unregistration==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION_UUID,
                        {"action": "unregistration"},
                        {},
                        "Блокирует токен в таблице clients_tokens меняет на b_blocked = true",
                        "shop_firm_016",
                        "Успешно блокируется токен",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        True,
                        marks=pytest.mark.smoke
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION_UUID,
                        {"action": ""},
                        {},
                        "Несуществующий метод",
                        "shop_firm_017",
                        "Возвращается ошибка с кодом 6 - Данного метода не существует",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=pytest.mark.regression
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION_UUID,
                        {"action": "remove"},
                        {},
                        "Несуществующий метод для этого метода",
                        "shop_firm_018",
                        "Возвращается ошибка с кодом 6 - Данного метода не существует",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=pytest.mark.regression
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION_UUID,
                        {"action": "remove; DROP TABLE tokens; --"},
                        {},
                        "Не существующий метод, с SQL-инъекцией",
                        "shop_firm_019",
                        "Возвращается ошибка с кодом 6 - Данного метода не существует, SQL-инъекция не работает",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=pytest.mark.regression
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_APPLICATION_UUID,
                        {"action": "registration"*10000},
                        {},
                        "Длинный параметр запроса",
                        "shop_firm_020", 
                        "Возвращается ошибка с кодом ответа 414 - Request-URI Too Large",
                        "error",
                        414,
                        ErrorData,
                        "text/html",
                        True,
                        marks=pytest.mark.regression
                        )
                ),
                #==========firm/branch==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {},
                        {},
                        "Авторизация пользователя. Возвращает информацию об филиале, категория блюд, список блюд, данные из таблиц",
                        "shop_firm_021",
                        "Успешно возвращает информацию о филиале",
                        "success",
                        200,
                        FirmBranchResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.smoke
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {},
                        {},
                        "Без авторизации. Возвращает информацию об филиале, категория блюд, список блюд, данные из таблиц",
                        "shop_firm_022",
                        "Успешно возвращает информацию о филиале",
                        "success",
                        200,
                        FirmBranchResponse,
                        "application/json",
                        False,
                        marks=[
                            pytest.mark.smoke,
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {"category": "all"},
                        {},
                        "Проверка фильтрации в параметрах запроса",
                        "shop_firm_023",
                        "Успешное возвращение всей информации о филиале",
                        "success",
                        200,
                        FirmBranchResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {"category": 3389142},
                        {},
                        "Фильтрация в параметрах запроса со значением INT",
                        "shop_firm_024",
                        "Успешное возвращение всей информации о филиале",
                        "success",
                        200,
                        FirmBranchResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {"search": "x"*10000},
                        {},
                        "Тест на устойчивость к длинным строкам в параметре запроса",
                        "shop_firm_025",
                        "Возвращается код сервера - 414 с текстом - Request-URI Too Large",
                        "error",
                        414,
                        ErrorData,
                        "text/html",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {"category": "<script>alert(1)</script>"},
                        {},
                        "Проверка безопасности. Передача в параметре запроса XSS-код уязвимости",
                        "shop_firm_026",
                        "Проверка на безопасность проходит успешно, символы '<''>' игнорируются, информация о филиале успешно возвращается",
                        "success",
                        200,
                        FirmBranchResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {},
                        {"Item": "1'; DROP TABLE users;--'"},
                        "Проверяем передачу в get запрос - тело. SQL-инъекция",
                        "shop_firm_027",
                        "Успешно возвращает информацию о филиале",
                        "success",
                        200,
                        FirmBranchResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                *[
                    pytest.param(
                        "post",
                        Firm.FIRM_BRANCH,
                        {},
                        {},
                        f"Идемпотентность и стабильность #{i}",
                        f"shop_firm_028_{str(i).zfill(2)}",
                        "Успешно отрабатывают все 100 запросов подряд, 100 раз возвращается информация о филиале",
                        "success",
                        200,
                        FirmBranchResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.load
                            ]
                        )
                        for i in range(1, 100)
                ],
                #==========firm/chat?action=default==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT,
                        {"action": "default"},
                        {
                            "limit": 10,
                            "after_message_id": 12,
                            "before_message_id": 3
                        },
                        "Авторизованный пользователь. Аметод (default) возвращает сообщение для филиала у которого включен chat",
                        "shop_firm_029",
                        "Успешно возвращает сообщение для филиала",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT,
                        {"action": "default"},
                        {
                            "limit": 10,
                            "after_message_id": 12,
                            "before_message_id": 3
                        },
                        "Неавторизованный пользователь. Аметод (default) возвращает сообщение для филиала у которого включен chat",
                        "shop_firm_030",
                        "Успешно возвращает сообщение для филиала",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        False,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                #==========firm/chat?action=message_statuses==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT,
                        {"action": "message_statuses"},
                        {
                            "messages_ids": [
                                                123,
                                                2454,
                                                3452
                                            ]
                        },
                        "Авторизованный пользователь. метод (message_statuses) возвращает статусы для id сообщений",
                        "shop_firm_031",
                        "Успешно возвращает статусы для id сообщений",
                        "success",
                        200,
                        FirmChatMesasageStatusesResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT,
                        {"action": "message_statuses"},
                        {
                            "messages_ids": [
                                                123,
                                                2454,
                                                3452
                                            ]
                        },
                        "Не авторизованный пользователь. метод (message_statuses) возвращает статусы для id сообщений",
                        "shop_firm_032",
                        "Успешно возвращает статусы для id сообщений",
                        "success",
                        200,
                        FirmChatMesasageStatusesResponse,
                        "application/json",
                        False,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                #==========firm/chat?action=send_message (возможно ожидаемый результат не верный, нужно проверить!)==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT,
                        {"action": "send_message"},
                        {"message": "test_text"},
                        "Авторизованный пользователь. метод (send_message) создает новое сообщение, возвращает статус сообщения",
                        "shop_firm_033",
                        "Успешно создает новое сообщение и возвращает статус сообщения (но это не точно)",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT,
                        {"action": "send_message"},
                        {"message": "test_text"},
                        "Не авторизованный пользователь. метод (send_message) создает новое сообщение, возвращает статус сообщения",
                        "shop_firm_034",
                        "Успешно создает новое сообщение и возвращает статус сообщения (но это не точно)",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        False,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                #==========firm/chat?action=send_image==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT_IMG,
                        {"action": "send_image"},
                        {"name": "test_image"},
                        "Авторизованный пользователь. метод (send_image) отправляет новое изображение в чат, возвращает статус сообщения",
                        "shop_firm_035",
                        "Успешно отправляет изображение в чат, возвращая успешный статус ",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_CHAT_IMG,
                        {"action": "send_image"},
                        {"name": "test_image"},
                        "Авторизованный пользователь. метод (send_image) отправляет новое изображение в чат, возвращает статус сообщения",
                        "shop_firm_036",
                        "Успешно отправляет изображение в чат, возвращая успешный статус ",
                        "success",
                        200,
                        SuccessResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Возвращается код 117 - Нет подключенных чатов"),
                            pytest.mark.smoke,
                            pytest.mark.chat
                            ]
                        )
                ),
                #==========firm/document==========
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments")), 
                            "company_id": Config.BRANCH
                        },
                        "Авторизованный пользователь. Возвращает документ по id для company_id",
                        "shop_firm_037",
                        "Успешно возвращаются документы по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.smoke
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments")), 
                            "company_id": Config.BRANCH
                        },
                        "Неавторизованный пользователь. Возвращает документ по id для company_id",
                        "shop_firm_038",
                        "Успешно возвращаются документы по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        False,
                        marks=[
                            pytest.mark.smoke
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": 0, 
                            "company_id": Config.BRANCH
                        },
                        "Передача в теле запроса нулевой id",
                        "shop_firm_039",
                        "Возвращается ошибка с кодом 30 - Пустое значение для ключа, поле id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": -1, 
                            "company_id": Config.BRANCH
                        },
                        "Передача в теле запроса отрицательный id",
                        "shop_firm_040",
                        "Успешно возвращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        ) # Необходимо уточнить, может ли быть такое
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments")), 
                            "company_id": 0
                        },
                        "Передача в теле запроса нулевой ID компании",
                        "shop_firm_041",
                        "Возвращается ошибка с кодом 30 - Пустое значение для ключа для поля company_id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                # Необходимо уточнить, может ли быть такое
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments")), 
                            "company_id": -50
                        },
                        "Передача в тело запроса отрицательный id компании",
                        "shop_firm_042",
                        "Успешно возращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                # Необходимо уточнить, может ли быть такое
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": 1, 
                            "company_id": Config.BRANCH
                        },
                        "Передача в тело запроса неправильный тип данных - str",
                        "shop_firm_043",
                        "Успешно возвращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[pytest.mark.regression]
                        )
                ),
                # Необходимо уточнить, может ли быть такое
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": 1.1, 
                            "company_id": Config.BRANCH
                        },
                        "Передача в тело запроса неправильный тип данных - float",
                        "shop_firm_043",
                        "Успешно возвращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[pytest.mark.regression]
                        )
                ),
                # Необходимо уточнить, может ли быть такое
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": True, 
                            "company_id": Config.BRANCH
                        },
                        "Передача в тело запроса неправильный тип данных - bool",
                        "shop_firm_044",
                        "Успешно возвращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[pytest.mark.regression]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": [random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments"))], 
                            "company_id": Config.BRANCH
                        },
                        "Передача в тело запроса неправильный тип данных - list",
                        "shop_firm_045",
                        "Успешно возвращается документ по id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Fatal error"),
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": {"x": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments"))}, 
                            "company_id": Config.BRANCH
                        },
                        "Передача в тело запроса неправлиьный тип данных - dict",
                        "shop_firm_046",
                        "Успешно возвращается документ по id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Fatal error"),
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {"company_id": Config.BRANCH},
                        "Передача в тело запроса, с отсутствующим полем - id",
                        "shop_firm_047",
                        "Возвращает ошибку с кодом 27 - Не найден ключ для поля id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {"id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments"))},
                        "Передача в тело запроса, с отсутствующим полем - company_id",
                        "shop_firm_048",
                        "Возвращает ошибку с кодом 27 - Не найден ключ для поля company_id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {},
                        "Передача пустого тела в запрос",
                        "shop_firm_049",
                        "Возвращает ошибку с кодом 27 - Не найден ключ для поля id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                # Необходимо уточнить, может ли быть такое
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": "١٢٣", 
                            "company_id": Config.BRANCH
                        },
                        "Передача в тело запроса Unicode цифры",
                        "shop_firm_050",
                        "Успешно возвращает документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                # Необходимо уточнить, может ли быть такое
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": "1" * 10000, 
                            "company_id": Config.BRANCH
                        },
                        "Передача в теле запроса слишком длинную строку с 10000 символами",
                        "shop_firm_051",
                        "Успешно возвращает документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": "", 
                            "company_id": Config.BRANCH
                        },
                        "Передача в теле запроса пустую строку ключа",
                        "shop_firm_052",
                        "Возвращает ошибку с кодом 30 - Пустое значение для ключа id",
                        "error",
                        200,
                        ErrorData,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.regression
                            ]
                        )
                ),
                # Необходимо уточнить, может ли быть такое
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": "<script>alert(1)</script>", 
                            "company_id": Config.BRANCH
                        },
                        "Передача в теле запроса XSS-код",
                        "shop_firm_053",
                        "Успешно возвращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[pytest.mark.regression]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments")),  
                            "company_id": "1; DROP TABLE users"
                        },
                        "Проверка метода на SQL уязвимость",
                        "shop_firm_054",
                        "Успешно возвращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.xfail(reason="Fatal error"),
                            pytest.mark.regression
                            ]
                        )
                ),
                (
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments")), 
                            "company_id": Config.BRANCH, 
                            "extra": "test"
                        },
                        "Передача в теле запроса дополнительное поле",
                        "shop_firm_055",
                        "Успешно возвращается документ по id",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[pytest.mark.regression]
                        )
                ),
                *[
                    pytest.param(
                        "post",
                        Firm.FIRM_DOCUMENT,
                        {},
                        {
                            "id": random.choice(seq=("agreement", "license", "conditions", "privacy_policy", "payments")), 
                            "company_id": Config.BRANCH
                        },
                        "Проверка на нагрузку метода с 100 последовательными запросами",
                        f"shop_firm_56_{str(i).zfill(2)}",
                        f"Идемпотентность и стабильность #{i}",
                        "success",
                        200,
                        FirmDocumentResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.load
                            ]
                        )
                        for i in range(1, 100)
                ],
                #==========firm/feedback?action=complaint==========
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint", 
                        "message": Text().title(), 
                        "feedback_id": random.randint(100000, 999999)
                    },
                    {},
                    "Авторизованный пользователь. добавляет запись со статусом problem",
                    "shop_firm_057",
                    "Успешно добавляется запись со статусом problem (Жалоба)",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke, 
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint", 
                        "message": Text().title(), 
                        "feedback_id": random.randint(100000, 999999)
                    },
                    {},
                    "Неавторизованный пользователь. добавляет запись со статусом problem",
                    "shop_firm_058",
                    "Успешно добавляется запись со статусом problem (Жалоба)",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "message": "",
                        "feedback_id": random.randint(100000, 999999)
                    },
                    {},
                    "Передача в параметрах запроса пустое поле message",
                    "shop_firm_059",
                    "Возвращает ошибку с кодом 30 - Пустое значение для ключа поля message",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "message": "1"*10000,
                        "feedback_id": random.randint(100000, 999999)
                    },
                    {},
                    "Передача в параметрах запроса слишком длинное поле message",
                    "shop_firm_060",
                    "Возвращает код ответа 414 - Request-URI Too Large",
                    "error",
                    414,
                    ErrorData,
                    "text/html",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "message": "🔥💬😎",
                        "feedback_id": random.randint(100000, 999999)
                    },
                    {},
                    "Передача в параметрах запроса emoji в сообщении",
                    "shop_firm_061",
                    "Успешно отправляется запись",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                #Почему так?
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "message": Text().title(),
                        "feedback_id": "123456"
                    },
                    {},
                    "Передача в параметрах запроса неверный тип данных - feedback: str",
                    "shop_firm_062",
                    "Успешно отправляется запись в таблицу",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "message": Text().title(),
                        "feedback_id": 0
                    },
                    {},
                    "Передача в параметрах запроса нулевое значение feedback_id",
                    "shop_firm_063",
                    "Успешно оправляется запись в таблицу",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "message": Text().title(),
                        "feedback_id": -5
                    },
                    {},
                    "Передача в параметрах запроса отрицательное значение в feedback_id",
                    "shop_firm_064",
                    "Успешно отправляется запись в таблицу",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "feedback_id": random.randint(100000, 999999)
                    },
                    {},
                    "Отсутствие поля message в параметрах запроса",
                    "shop_firm_065",
                    "Возвращается ошибка с кодом 27 - Не найден ключ для поля message",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                #Нужно уточнить работу этого метода, если query action не правильный, должен ли сервер возвращать ошибку 
                # возвращается ответ метода default
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "actionn": "complaint",
                        "message": Text().title(),
                        "feedback_id": random.randint(100000, 999999)
                    },
                    {},
                    "Неверный метод в параметрах запроса",
                    "shop_firm_066",
                    "Возвращается ответ метода ?action=default",
                    "success",
                    200,
                    FirmFeedbackDefaultResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {
                        "action": "complaint",
                        "message": Text().title(),
                        "feedback_id": random.randint(100000, 999999),
                        "sequrity": "<script>alert('XSS')</script>"
                    },
                    {},
                    "Проверка метода на xss безопасность, дополнительным полем в параметрах запроса",
                    "shop_firm_067",
                    "Успешно добавляется запись в таблицу",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                #==========firm/feedback?action=cache_fields_default==========
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "cache_fields_default"},
                    {
                        "type": "client", 
                        "limit": 10, 
                        "last_receive_id": 3
                    },
                    "Авторизованный пользователь. метод (cache_fields_default) возвращает кэш-поля по умолчанию из переданных параметров",
                    "shop_firm_068",
                    "Успешно возвращается кэш поля по умолчанию",
                    "success",
                    200,
                    FirmFeedbackCFDResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "cache_fields_default"},
                    {
                        "type": "client",
                        "limit": 10,
                        "last_receive_id": 3
                    },
                    "Неавторизованный пользователь. метод (cache_fields_default) возвращает кэш-поля по умолчанию из переданных параметров",
                    "shop_firm_069",
                    "Успешно возвращается кэш поля по умолчанию",
                    "success",
                    200,
                    FirmFeedbackCFDResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "cache_fields_default"},
                    {
                        "type": "client",
                        "last_receive_id": 3
                    },
                    "Отсутствует поле limit при передаче в теле запроса",
                    "shop_firm_070",
                    "Успешно возвращается кэш-поля по умолчанию",
                    "success",
                    200,
                    FirmFeedbackCFDResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "cache_fields_default"},
                    {
                        "type": "client",
                        "limit": 10,
                        "last_receive_id": "wasd"
                    },
                    "Неверный тип для поля last_receive_id",
                    "shop_firm_071",
                    "Успешно возвращается кэш-поля по умолчанию",
                    "success",
                    200,
                    FirmFeedbackCFDResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "cache_fields_default"},
                    {
                        "type": "client",
                        "limit": 10,
                        "last_receive_id": 10,
                        "extra": "wtf_dude"
                    },
                    "Передача в теле запроса лишнего поля",
                    "shop_firm_072",
                    "Успешно возвращается кэш-поля по умолчанию",
                    "success",
                    200,
                    FirmFeedbackCFDResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "cache_fields_default"},
                    {
                        "type": "admin",
                        "limit": 10, 
                        "last_receive_id": 10
                    },
                    "Поле type принимает значение admin",
                    "shop_firm_073",
                    "Успешно возвращается кэш поля по умолчанию",
                    "success",
                    200,
                    FirmFeedbackCFDResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                #==========firm/feedback?action=default==========
                #Почему возвращается пустая data, в то время как в 66 тесте возвращается ожидаемый ответ
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "default"},
                    {"type": "client"},
                    "Авторизированный пользователь. метод (default) возвращает список ответов на вопросы обратной связи для текущего филиала",
                    "shop_firm_074",
                    "Успешно возвращает список ответов на вопросы обратной связи",
                    "success",
                    200,
                    SuccessResponseSecound,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "default"},
                    {"type": "client"},
                    "Неавторизированный пользователь. метод (default) возвращает список ответов на вопросы обратной связи для текущего филиала",
                    "shop_firm_075",
                    "Успешно возвращает список ответов на вопросы обратной связи",
                    "success",
                    200,
                    SuccessResponseSecound,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "default"},
                    {},
                    "Передача пустого тела в запросе",
                    "shop_firm_076",
                    "Успешно возвращается список ответов на вопросы обратной связи",
                    "success",
                    200,
                    FirmFeedbackDefaultResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                #==========firm/feedback?action=orders==========
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "orders"},
                    {},
                    "Авторизованный пользователь. метод (orders) результаты заполнения формы обратной связи",
                    "shop_firm_077",
                    "Успешно возвращаются результаты заполнения формы обратной связи",
                    "success",
                    200,
                    FirmFeedbackOrdersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "orders"},
                    {},
                    "Неавторизованный пользователь. метод (orders) результаты заполнения формы обратной связи",
                    "shop_firm_078",
                    "Успешно возвращаются результаты заполнения формы обратной связи",
                    "success",
                    200,
                    FirmFeedbackOrdersResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "orders", "wtf": "new"},
                    {},
                    "Передача дополнительного параметра",
                    "shop_firm_079",
                    "Успешно возвращаются результаты заполнения формы обратной связи",
                    "success",
                    200,
                    FirmFeedbackOrdersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                #==========firm/feedback?action=new==========
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "new"},
                    {
                        "order_id": 12864630, 
                        "text": Text().text(), 
                        "status": random.choice(seq=["negative", "positive"])
                    },
                    "Авторизированный пользователь. метод (new) добавляет запись обратной связи",
                    "shop_firm_080",
                    "Успешно создает новую запись обратной связи",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "new"},
                    {
                        "order_id": 12864630,
                        "text": "",
                        "status": random.choice(seq=["negative", "positive"])
                    },
                    "Передача в теле запроса пустое поле",
                    "shop_firm_081",
                    "Возвращается ошибка с кодом 30 - Пустое значение для ключа для поля text",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "new"},
                    {
                        "order_id": random.choice(seq=[12864630, 12864650, 12864651, 12864652, 12864653, 12864654, 12864655, 12864656, 12864657, 12864658, 12864659, 12864661]),
                        "text": Text().text(),
                        "status": "invalid"
                    },
                    "Неправильный статус в теле запроса",
                    "shop_firm_082",
                    "Возвращается ошибка с кодом 123 - Неправильный статус для отзыва",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_FEEDBACK,
                    {"action": "new"},
                    {
                        "order_id": random.choice(seq=[12864630, 12864650, 12864651, 12864652, 12864653, 12864654, 12864655, 12864656, 12864657, 12864658, 12864659, 12864661]),
                        "text": "test; DROP TABLE users; --",
                        "status": random.choice(seq=["negative", "positive"])
                    },
                    "Передача в теле запроса - SQL инъекцию",
                    "shop_firm_083",
                    "Возвращает ошибку с кодом 124 - Для клиента не найден заказ за последние 3 дня",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.feedback
                        ]
                    ),
                #==========firm/geocoding?action=protocol==========
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": "protocol"},
                    {},
                    "Авторизованный пользователь. Возвращает сервисы поиска координат",
                    "shop_firm_084",
                    "Возвращает сервисы поиска координат или поиск мест по координатам",
                    "success",
                    200,
                    FirmGeocodingResponseResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": "protocol"},
                    {},
                    "Неавторизованный пользователь. Возвращает сервисы поиска координат",
                    "shop_firm_085",
                    "Возвращает сервисы поиска координат или поиск мест по координатам",
                    "success",
                    200,
                    FirmGeocodingResponseResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {},
                    {},
                    "Обязательный параметр отсутствует",
                    "shop_firm_086",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": "invalid"},
                    {},
                    "Несуществующий метод при передаче в параметрах запроса",
                    "shop_firm_087",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": ""},
                    {},
                    "Пустое значение метода при передаче параметров запроса",
                    "shop_firm_088",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": 123},
                    {},
                    "Несуществующее значение в параметрах запроса",
                    "shop_firm_089",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": True},
                    {},
                    "Значение в параметре запроса - тип данных - bool",
                    "shop_firm_090",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": None},
                    {},
                    "Нулевое значение в значении параметраз запроса",
                    "shop_firm_091",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                #вернул 502, возможно что то с гитом, но это не точно
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": "PROTOCOL"},
                    {},
                    "Чувствительность к регистру при передаче в параметрах запроса",
                    "shop_firm_092",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                #вернул 502, возможно что то с гитом, но это не точно
                pytest.param(
                    "post",
                    Firm.FIRM_GEOCODING,
                    {"action": "<script>alert(1)</script>"},
                    {},
                    "XSS уязвимость в параметрах запроса",
                    "shop_firm_093",
                    "Возвращает ошибку с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                    ),
                *[
                    pytest.param(
                        "post",
                        Firm.FIRM_GEOCODING,
                        {"action": "protocol"},
                        {},
                        f"Идемпотентность и стабильность #{i}",
                        f"shop_firm_094_{str(i).zfill(2)}",
                        "Успешно возвращаются сервисы поиска координат",
                        "success",
                        200,
                        FirmGeocodingResponseResponse,
                        "application/json",
                        True,
                        marks=[
                            pytest.mark.load
                            ]
                        )
                        for i in range(1, 100)
                ],
                #==========firm/notification_cart?action=reminder_init==========
                pytest.param(
                    "post",
                    Firm.FIRM_NOTIFICATION_CART,
                    {"action": "reminder_init"},
                    {},
                    "Авторизованный пользователь. метод (reminder_init) добавляет запись в таблицу - одиночные push-уведомления фирмам",
                    "shop_firm_097",
                    "Успешно добавляет запись в таблицу",
                    "success",
                    200,
                    FirmNotificationsResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_NOTIFICATION_CART,
                    {"action": "reminder_init"},
                    {},
                    "Неавторизованный пользователь. метод (reminder_init) добавляет запись в таблицу - одиночные push-уведомления фирмам",
                    "shop_firm_098",
                    "Успешно добавляет запись в таблицу",
                    "success",
                    200,
                    FirmNotificationsResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.regression
                        ]
                    ),
                #==========firm/notification_cart?action=reminder_delete==========
                pytest.param(
                    "post",
                    Firm.FIRM_NOTIFICATION_CART,
                    {"action": "reminder_delete"},
                    {},
                    "Авторизованный пользователь. метод (reminder_delete) удаляет уведомление из таблицы",
                    "shop_firm_099",
                    "Успешно удаляет уведомление из таблицы",
                    "success",
                    200,
                    FirmNotificationsResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_NOTIFICATION_CART,
                    {"action": "reminder_delete"},
                    {},
                    "Неавторизованный пользователь. метод (reminder_delete) удаляет уведомление из таблицы",
                    "shop_firm_100",
                    "Успешно удаляет уведомление из таблицы",
                    "success",
                    200,
                    FirmNotificationsResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                    ),
                #==========firm/notifications==========
                pytest.param(
                    "post",
                    Firm.FIRM_NOTIFICATION_CART,
                    {},
                    {},
                    "Авторизованный пользователь. возвращает массовые push-уведомления фирм",
                    "shop_firm_101",
                    "Возвращается ошибка с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                    ),
                pytest.param(
                    "post",
                    Firm.FIRM_NOTIFICATION_CART,
                    {},
                    {},
                    "Неавторизованный пользователь. возвращает массовые push-уведомления фирм",
                    "shop_firm_102",
                    "Возвращается ошибка с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                    ),
                #==========firm/order?action=new==========
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                            }
                        ]
                    },
                    "Авторизованный пользователь. Создание новго заказа на самовывоз",
                    "shop_firm_103",
                    "Успешное создание ноого заказа",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                            }
                        ]
                    },
                    "Неавторизованный пользователь. Создание новго заказа на самовывоз",
                    "shop_firm_103",
                    "Успешное создание нового заказа",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                            }
                        ]
                    },
                    "Авторизованный пользователь. Создание новго заказа на доставку",
                    "shop_firm_103_1",
                    "Успешное создание нового заказа",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                            }
                        ]
                    },
                    "Неавторизованный пользователь. Создание новго заказа на доставку",
                    "shop_firm_103_2",
                    "Успешное создание нового заказа",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke,
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                },
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание двух товаров в заказе на самовывоз",
                    "shop_firm_104",
                    "Успешное создание нового заказа",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #Возвращается 200, но без тела, скорее всего тут должна возвращаться какая то ошибка
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": "2"*10000,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с количеством товара больше 9999",
                    "shop_firm_105",
                    "Успешное создание нового заказа",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.xfail(reason="Возвращается 200, но без тела, скорее всего тут должна возвращаться какая то ошибка"),
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": ""},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа без параметра action",
                    "shop_firm_106",
                    "Возвращается ошибка с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "neww"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с неверным параметром action",
                    "shop_firm_107",
                    "Возвращается ошибка с кодом 6 - Данного метода не существует",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа без заголовка pickup",
                    "shop_firm_108",
                    "Возвращает ошибку с кодом 104 - Филиал в данное время не работает",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с неверным заголовком pickup",
                    "shop_firm_109",
                    "Возвращается ошибка с кодом 33 - Значение по ключу должно быть цифрой для заголовка pickup",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {},
                    "Создание заказа с пустым телом запроса",
                    "shop_firm_110",
                    "Возвращает ошибку с кодом 27 - Не найден ключ для поля info",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": []
                    },
                    "Создание заказа с пустым списком товаров",
                    "shop_firm_111",
                    "Возвращает ошибку с кодом 30 - Пустое значение для ключа поля cart",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 0,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с нулевым количеством товаров",
                    "shop_firm_112",
                    "Успешное создание нового заказа",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": 99999999999999999999999999999999
                                }
                            ]
                    },
                    "Создание заказа с несуществующим товаром",
                    "shop_firm_113",
                    "Возвращает ошибку с кодом 108 - Товара не найден",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                # Валидация типов полей отсутствует для id?
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": "94091133"
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле id",
                    "shop_firm_114",
                    "Успешно создает новый заказ",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 0,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле count",
                    "shop_firm_115",
                    "Успешно создает новый заказ",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #Возвращает успешно созданный заказ
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": "invalid", # Так вроде тоже не должно быть
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле payment_status",
                    "shop_firm_116",
                    "Успешно создается новый заказ",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #Доступ запрещен на ограниченный промежуток времени
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": "invalid" # Так вроде тоже не должно быть
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле payment_method",
                    "shop_firm_117",
                    "Успешно создает новый заказ",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.xfail(reason="Fatal error"),
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": "invalid"
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле id",
                    "shop_firm_118",
                    "Возвращается ошибка с кодом 33 - Значение по ключу должно быть цифрой для поля id",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "abc", "format_id": 1}} # Это реально?
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле number",
                    "shop_firm_119",
                    "Успешно создает новый заказ",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 9999999}}
                            },
                        "cart": [
                            {
                                "count": 3,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле format_id",
                    "shop_firm_120",
                    "Успешно создает новый заказ",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {"info": "value"},
                    "Создание заказа с неверным боди",
                    "shop_firm_121",
                    "Возвращается ошибка с кодом 27 - Не найден ключ для поля fields",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": 940911.32
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле id",
                    "shop_firm_122",
                    "Возвращается ошибка с кодом 108 - Товара не найден",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": "2",
                                "id": 94091133
                                },
                            {
                                "count": 2, 
                                "id": 94091132
                                }
                            ]
                    },
                    "Создание заказа с неверным типом данных в поле count",
                    "shop_firm_123",
                    "Успешно создается новый заказ",
                    "success",
                    200,
                    FirmOrderResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #количество запросов превышено
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999"*100, "format_id": 1}}
                            },
                        "cart": [
                            {
                                "count": 2,
                                "id": 94089172
                                },
                            {
                                "count": 2,
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Создание заказа с экстримально длинным номером телефона",
                    "shop_firm_124",
                    "Возвращается ошибка - ",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.xfail(reason="Fatal error"),
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {
                        "info": {
                            "payment_status": random.choice(seq=["paid", "not_paid", "waiting"]),
                            "payment_method": random.choice(seq=["cash", "online", "card_upon_receipt"])
                            },
                        "fields": {
                            "sender": {"phone": {"number": "9999999999", "format_id": 1}}
                            },
                        "cart": [{
                                "count": 2, 
                                "id": random.choice(seq=[94091133, 94091132])
                                }
                            ]
                    },
                    "Заголовок pickup c 0 значением",
                    "shop_firm_125",
                    "Возвращается ошибка с кодом 104 - Филиал в данное время не работает",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_ORDER,
                    {"action": "new"},
                    {"info": None},
                    "None в теле запроса",
                    "shop_firm_126",
                    "Возвращается ошибка с кодом 27 - Не найден ключ для поля info",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #==========firm/special_offers?action=check_first_purchase==========
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_first_purchase"},
                    {
                        "offers_ids": [
                            random.choice(seq=[152717, 152715, 152712, 152605, 152604])
                            ]
                    },
                    "Авторизованный пользователь. Проверка первой покупки",
                    "shop_firm_127",
                    "Успешно возвращается информация о первой покупке",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_first_purchase"},
                    {
                        "offers_ids": [
                            random.choice(seq=[152717, 152715, 152712, 152605, 152604,])
                            ]
                    },
                    "Неавторизованный пользователь. Проверка первой покупки",
                    "shop_firm_128",
                    "Успешно возвращается информация о первой покупке",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_first_purchase"},
                    {"offers_ids": [152717, "1"*10000000]},
                    "длинная строка в массиве",
                    "shop_firm_129",
                    "Успешно возвращается информация о первой покупке",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.xfail(reason="fatal error"),
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_first_purchase"},
                    {"offers_ids": ["abc", 152717]},
                    "Некорректный массив",
                    "shop_firm_130",
                    "Успешно возвращается информация о первой покупке",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_first_purchase"},
                    {},
                    "Некорректный массив",
                    "shop_firm_131",
                    "Возвращается ошибка с кодом 27 - Не найден ключ для поля offers_ids",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #==========firm/special_offers?action=check_reuse==========
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_reuse"},
                    {"offers_ids": [random.choice(seq=[152717, 152715, 152712, 152605, 152604])]},
                    "Авторизованный пользователь. проверить повторное использование",
                    "shop_firm_132",
                    "Успешно проверяем повтороное использование",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_reuse"},
                    {"offers_ids": [random.choice(seq=[152717, 152715, 152712, 152605, 152604])]},
                    "Неавторизованный пользователь. проверить повторное использование",
                    "shop_firm_132",
                    "Успешно проверяем повтороное использование",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_reuse"},
                    {"offers_ids": [152717, 152717]},
                    "Дублирование ID",
                    "shop_firm_133",
                    "Успешно проверяем повторное использование",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_reuse", "once": "again"},
                    {"offers_ids": [random.choice(seq=[152717, 152715, 152712, 152605, 152604])]},
                    "Дублирование ID",
                    "shop_firm_134",
                    "Успешно проверяем повторное использование",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #==========firm/special_offers?action=check_birthday==========
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_birthday"},
                    {"offers_ids": [random.choice(seq=[152717, 152715, 152712, 152605, 152604])]},
                    "проверка дня рождения",
                    "shop_firm_135",
                    "Авторизованный пользователь. Успешно проверяем день рождение",
                    "success",
                    200,
                    FirmSpecialOffersResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_birthday"},
                    {"offers_ids": [random.choice(seq=[152717, 152715, 152712, 152605, 152604])]},
                    "проверка дня рождения",
                    "shop_firm_135_1",
                    "Неавторизованный пользователь. Возвращается ошибка с кодом 106 - Сессия не найдена",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.regression,
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "check_birthday"},
                    {"offers_ids": []},
                    "проверка дня рождения",
                    "shop_firm_136",
                    "Возвращается ошибка с кодом 30 - Пустое значение для ключа поля offers_ids",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #==========firm/special_offers?action=get_promo_code==========
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "get_promo_code"},
                    {"promo_code": "1111"},
                    "Авторизованный пользоатель. получает промокод",
                    "shop_firm_137",
                    "Успешно возвращается информация о промокоде",
                    "success",
                    200,
                    FirmSpecialOffersGetPromoCodeResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "get_promo_code"},
                    {"promo_code": "1111"},
                    "Неавторизованный пользователь. получает промокод",
                    "shop_firm_138",
                    "Успешно возвращается информация о промокоде",
                    "success",
                    200,
                    FirmSpecialOffersGetPromoCodeResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "get_promo_code"},
                    {"promo_code": ""},
                    "Пустой промокод",
                    "shop_firm_139",
                    "Возвращает ошибку с кодом 30 - Пустое значение для ключа promo_code",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_SPECIAL_OFFERS,
                    {"action": "get_promo_code"},
                    {},
                    "Пустое тело запроса",
                    "shop_firm_140",
                    "Возвращает ошибку 27 - Не найден ключ promo_code",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #==========firm/vacancies==========
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {},
                    {},
                    "Авторизованный пользователь. возвращает список вакансии для филиала",
                    "shop_firm_141",
                    "Успешно возвращает список вакансии для филиала",
                    "success",
                    200,
                    FirmVacanciesGetResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {},
                    {},
                    "Неавторизованный пользователь. возвращает список вакансии для филиала",
                    "shop_firm_142",
                    "Успешно возвращает список вакансии для филиала",
                    "success",
                    200,
                    FirmVacanciesGetResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"extra_params": 2255},
                    {},
                    "Игнорирование параметров",
                    "shop_firm_143",
                    "Успешно возвращает список вакансии для филиала",
                    "success",
                    200,
                    FirmVacanciesGetResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                #==========firm/vacancies?action=new_candidate==========
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": Person().first_name(), 
                        "date_of_birth": "1900-02-22", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "higher",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Авторизованный пользователь. добавляет запись (отклик на вакансию) в таблицу candidates, отправляет почтовое сообщение",
                    "shop_firm_144",
                    "Успешно добавляется запись в таблицу",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": Person().first_name(), 
                        "date_of_birth": "1900-02-22", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "higher",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Неавторизованный пользователь. добавляет запись (отклик на вакансию) в таблицу candidates, отправляет почтовое сообщение",
                    "shop_firm_144",
                    "Успешно добавляется запись в таблицу",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    False,
                    marks=[
                        pytest.mark.smoke
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {},
                    "Отправка пустого тела",
                    "shop_firm_145",
                    "Возвращает ошибку с кодом 27 - Не найден ключ vacancy_id",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": "", 
                        "date_of_birth": "1900-02-22", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "higher",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Проверка обязательного поля name",
                    "shop_firm_146",
                    "Возвращается ошибка с кодом 30 - Пустое значение для ключа name",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": Person().first_name(), 
                        "date_of_birth": "01-02-1825", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "higher",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Проверка обязательного поля date_of_birthday",
                    "shop_firm_147",
                    "Возвращается ошибка с кодом 500",
                    "success",
                    500,
                    SuccessResponse,
                    "text/html",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": Person().first_name(), 
                        "date_of_birth": "3000-01-02", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "higher",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Проверка обязательного поля date_of_birth",
                    "shop_firm_148",
                    "Успешно добавляется новый кандидат в таблицу",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": Person().first_name(), 
                        "date_of_birth": "1900-02-22", 
                        "gender": "other",
                        "education": "higher",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Проверка обязательного поля name",
                    "shop_firm_149",
                    "Возвращается ошибка с кодом 19 - Неправильный формат данных для поля gender",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": Person().first_name(), 
                        "date_of_birth": "1900-02-22", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "another",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Проверка обязательного поля name",
                    "shop_firm_150",
                    "Возвращается ошибка с кодом 19 - Неправильный формат данных для поля education",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": Person().first_name(), 
                        "date_of_birth": "1900-02-22", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "higher",
                        "phone": {"format_id": 1, "number": "aaaaass"}
                    },
                    "Проверка обязательного поля name",
                    "shop_firm_151",
                    "Возвращается ошибка с кодом 132 - Телефон имеет не корректный формат",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {},
                    "Проверка обязательного поля name",
                    "shop_firm_152",
                    "Возвращается ошибка с кодом 27 - Не найден ключ для поля vacancy_id",
                    "error",
                    200,
                    ErrorData,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                ),
                pytest.param(
                    "post",
                    Firm.FIRM_VACANCIES,
                    {"action": "new_candidate"},
                    {
                        "vacancy_id": random.choice(seq=["564", "526", "562", "556"]), 
                        "name": "test; DROP TABLE users; --", 
                        "date_of_birth": "1900-02-22", 
                        "gender": random.choice(seq=["man", "woman"]),
                        "education": "higher",
                        "phone": {"format_id": 1, "number": Person().phone_number(mask="9#########")}
                    },
                    "Проверка обязательного поля name",
                    "shop_firm_153",
                    "Успешно добавляется запись нового кандидата",
                    "success",
                    200,
                    SuccessResponse,
                    "application/json",
                    True,
                    marks=[
                        pytest.mark.regression
                        ]
                )
            ]
