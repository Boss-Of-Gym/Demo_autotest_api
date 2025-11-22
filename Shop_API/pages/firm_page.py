from pages.base_page import BasePage
from utils.endpoints import Firm
from configs.config import Config
from typing import Dict
import requests
import allure
import re
from datetime import datetime

class FirmPage(BasePage):
    """Класс для работы с методами firm"""

    def assert_status_code(self, response, expected_status=200):
        assert response.status_code == expected_status, f"Ожидался код 200, а вернулся {response.status_code}"

    def post_application(self, action):
        """метод (about) - возвращает email филиала, реквизиты"""
        with allure.step("Получение email, филиал, реквизиты"):
            response = self.post(endpoint=f"{Firm.firm_application}?action={action}", timeout=50)
            return response
    
    def validation_fields_application(self, action, data: Dict[str, str]):
        data_block = data["data"]
        
        if action == "about":
            EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            data_list = [
                {'id': 'agreement'},
                {'id': 'license'},
                {'id': 'conditions'},
                {'id': 'privacy_policy'},
                {'id': 'payments'}
            ]

            assert "documents" in data_block
            assert all(isinstance(item, dict) for item in data_list), "Все элементы должны быть словарями"
            assert all(isinstance(item.get("id"), str) for item in data_list), "Все id должны быть строками"
            assert "support_email" in data_block
            assert isinstance(data_block["support_email"], str)
            assert data_block["support_email"].strip() != "", f"Ожидалось, что {data_block['information']} содержится информация, но поле пустое"
            assert re.match(EMAIL_REGEX, data_block["support_email"]), f"Ожидалось корректный email, но вернулся {data_block["support_email"]}"
            assert "requisites" in data_block
            assert isinstance(data_block["requisites"], list)
            requisites = data_block["requisites"]
            assert all(isinstance(item, dict) for item in requisites), "Каждый элемент requisites должен быть словарём"
            for item in requisites:
                assert "key" in item, f"У элемента {item} отсутствует ключ 'key'"
                assert "value" in item, f"У элемента {item} отсутствует ключ 'value'"
                assert isinstance(item["key"], str), "Поле key должно быть строкой"
                assert isinstance(item["value"], str), "Поле value должно быть строкой"
                assert item["key"].strip() != "", "Поле key не должно быть пустым"
                assert item["value"].strip() != "", "Поле value не должно быть пустым"
        elif action == "init":
            assert "init" in data_block
            assert "chain_id" in data_block["init"]
            assert isinstance(data_block["init"]["chain_id"], int), f"Ожидалось, что chain_id - int, но {data_block["init"]["chain_id"]}"
            assert "zone" in data_block["init"]
            assert isinstance(data_block["init"]["zone"], str)
            assert "name" in data_block
            assert isinstance(data_block["name"], str)
            assert "settings" in data_block

            settings = [
                "adult_mode",
                "field_of_activity",
                "geolocation_mode",
                "dialog_delivery_method",
                "client_authorization_required"
            ]

            for setting in settings:
                assert setting in data_block["settings"]
                if setting == "field_of_activity":
                    assert isinstance(data_block["settings"][setting], str)
                else:
                    assert isinstance(data_block["settings"][setting], bool)
            
            assert "themes" in data_block
            assert "desktop" in data_block["themes"]
            
            desktops = [
                "color_scheme",
                "items_image_ratio",
                "loader",
                "infinity_catalog",
                "full_menu",
                "auto_change",
                "name",
                "template",
                "items_max_rows_description"
            ]

            colors = [
                "primary_color",
                "accent_color"
            ]

            for desktop in desktops:
                assert desktop in data_block["themes"]["desktop"]
                if desktop == "color_scheme":
                    for color in colors:
                        assert color in data_block["themes"]["desktop"][desktop]
                        assert isinstance(data_block["themes"]["desktop"][desktop][color], str)
                elif desktop == "infinity_catalog" or desktop == "full_menu" or desktop == "auto_change":
                    assert isinstance(data_block["themes"]["desktop"][desktop], bool)
                else:
                    assert isinstance(data_block["themes"]["desktop"][desktop], str)
            
            # mobiles = [
            #     "name",

            # ]
        
    def get_branch(self) -> requests.Response:
        """
        возвращает информацию об филиале, категория блюд, список блюд, данные из таблиц: firms_branches, 
        firms_chains, map_zones.automations, vacancies, firms_categories, firms_special_offers, ...
        """
        with allure.step("возвращает информацию об филиале"):
            response = self.get(endpoint=Firm.firm_branch, timeout=50)
            return response
        
    def validation_fields_branch(self, data: Dict[str, str] = None) -> None:

        data_block = data["data"]

        # --- settings ---
        settings = data_block.get("settings")
        assert isinstance(settings, dict), "'settings' отсутствует или неверного типа"

        # fields
        fields = settings.get("fields", [])
        assert isinstance(fields, list), "'fields' должен быть списком"
        assert len(fields) > 0, "'fields' пустой — ожидается хотя бы один элемент"

        allowed_groups = {"sender", "recipient", "address", "additional"}

        for idx, field in enumerate(fields):
            assert isinstance(field, dict), f"Элемент fields[{idx}] должен быть словарём"
            # Обязательные ключи, которые всегда есть
            for key in ["name", "required", "type", "group"]:
                assert key in field, f"Поле '{key}' отсутствует в fields[{idx}]"

            # Типы базовых полей
            assert isinstance(field["name"], str), f"fields[{idx}].name должен быть str"
            assert isinstance(field["required"], bool), f"fields[{idx}].required должен быть bool"
            assert isinstance(field["type"], str), f"fields[{idx}].type должен быть str"
            assert isinstance(field["group"], str), f"fields[{idx}].group должен быть str"
            assert field["group"] in allowed_groups, (
                f"fields[{idx}].group имеет недопустимое значение '{field['group']}'. "
                f"Допустимые: {', '.join(allowed_groups)}"
            )

            if field["type"] in ("string", "integer"):
                assert "length" in field, f"Поле 'length' отсутствует в fields[{idx}] при типе {field['type']}"
                assert isinstance(field["length"], int), f"fields[{idx}].length должен быть int"
            else:
                # Для остальных типов 'length' может отсутствовать — это допустимо
                if "length" in field:
                    assert isinstance(field["length"], int), f"fields[{idx}].length должен быть int, если присутствует"

        # info
        info = settings.get("info", {})
        assert isinstance(info, dict), "'info' отсутствует или неверного типа"
        options = info.get("options", {})
        assert isinstance(options, dict), "'info.options' отсутствует или неверного типа"
        for key in ["block_app", "phone_mask", "feedback", "order_countdown", "vacancies", "promo_code"]:
            assert key in options, f"'info.options' не содержит ключ '{key}'"
            assert isinstance(options[key], bool), f"Ожидался тип int для поля {key}, а вернулся тип {type(options[key])}"
        if "special_offers_on_mobile" in options:
            # special_offers_on_mobile вложенные поля
            som = options["special_offers_on_mobile"]
            assert isinstance(som, dict), "'special_offers_on_mobile' неверного типа"
            assert "separate_section" in som and isinstance(som["separate_section"], bool), f"Ожидался тип int для поля separate_section, а вернулся тип {type(som["separate_section"])}"
            assert "title_in_catalog" in som and isinstance(som["title_in_catalog"], bool), f"Ожидался тип int для поля title_in_catalog, а вернулся тип {type(som["title_in_catalog"])}"

        # cart
        cart = info.get("cart", {})
        assert isinstance(cart, dict), "'info.cart' неверного типа"
        assert "lead_time" in cart and isinstance(cart["lead_time"], bool), f"Ожидался тип int для поля lead_time, а вернулся тип {type(cart["lead_time"])}"

        # bonuses
        bonuses = settings.get("bonuses", {})
        assert isinstance(bonuses, dict)
        for key in ["automation", "enable", "common", "referral", "minimum_sum", "free_delivery", "reports", "hide_accrual"]:
            assert key in bonuses and isinstance(bonuses[key], bool), f"Ожидался тип int для поля {key}, а вернулся тип {type(bonuses[key])}"
        rules = bonuses.get("rules", {})
        assert isinstance(rules, dict)
        # проверка вложенных правил accrual
        accrual = rules.get("accrual", {})
        assert isinstance(accrual, dict)
        referral = accrual.get("referral", {})
        for key in ["invited", "inviter", "percent", "pyramid"]:
            assert key in referral
            if key != "pyramid":
                assert isinstance(referral[key], int), f"Ожидался тип int для поля {key}, а вернулся тип {type(referral[key])}"
            else:
                assert isinstance(referral[key], bool), f"Ожидался тип int для поля {key}, а вернулся тип {type(referral[key])}"
        for key in ["withdraw", "decrease", "registration", "items", "feedback", "birthday"]:
            assert key in accrual
            if key == "withdraw" or key == "decrease":
                assert isinstance(accrual[key], bool), f"Ожидался тип int для поля {key}, а вернулся тип {type(accrual[key])}"
            else:
                assert isinstance(accrual[key], int), f"Ожидался тип int для поля {key}, а вернулся тип {type(accrual[key])}"

        withdraw = rules.get("withdraw", {})
        assert isinstance(withdraw, dict)
        assert "items" in withdraw, f"items отсутствует в {withdraw}"
        assert isinstance(withdraw["items"], int), f"Ожидался тип int для поля items, а вернулся тип {type(withdraw["items"])}"

        validity = rules.get("validity", {})
        assert isinstance(validity, dict)
        for key in ["items", "feedback", "birthday", "registration", "referral"]:
            assert key in validity
            assert isinstance(validity[key], int), f"Ожидался тип int для поля {key}, а вернулся тип {type(validity[key])}"

        # preorder
        preorder = settings.get("preorder", {})
        assert isinstance(preorder, dict)
        for key in ["enable", "only_in_work_time", "always"]:
            assert key in preorder and isinstance(preorder[key], bool), f"Ожидался тип int для поля {key}, а вернулся тип {type(preorder[key])}"
        time_limits = preorder.get("time_limits", {})
        assert isinstance(time_limits, dict)
        for method in ["delivery", "pickup"]:
            assert method in time_limits
            assert "minimum_minutes" in time_limits[method] and "maximum_days" in time_limits[method]
            assert isinstance(time_limits[method]["minimum_minutes"], int), f"Ожидался тип int для поля {key}, а вернулся тип {type(time_limits[method]["minimum_minutes"])}"
            assert isinstance(time_limits[method]["maximum_days"], int), f"Ожидался тип int для поля {key}, а вернулся тип {type(time_limits[method]["maximum_days"])}"

        # payments
        payments = settings.get("payments", [])
        assert isinstance(payments, list)
        for idx, payment in enumerate(payments):
            for key in ["id", "system_id", "type", "delivery_method"]:
                assert key in payment
            if "final_urls" in payment:
                urls = payment["final_urls"]
                assert "success" in urls and isinstance(urls["success"], list)
                assert "fail" in urls and isinstance(urls["fail"], list)
            if "info" in payment:
                info_payment = payment["info"]
                assert "method" in info_payment and "gateway" in info_payment

        # --- categories ---
        categories = data_block.get("categories", [])
        assert isinstance(categories, list)
        for idx, cat in enumerate(categories):
            assert "id" in cat and isinstance(cat["id"], str), f"Поле id имеет тип {type(cat["id"])}, а должна int"
            # assert "parent_id" in cat and isinstance(cat["parent_id"], int), f"Поле id имеет тип {type(cat["parent_id"])}, а должна int"
            assert "name" in cat and isinstance(cat["name"], str)
            assert "days_of_week" in cat and isinstance(cat["days_of_week"], list)
            seo = cat.get("seo", {})
            assert "friendly_url" in seo and isinstance(seo["friendly_url"], str)
            assert "published" in cat and isinstance(cat["published"], bool)

        # --- items ---
        items = data_block.get("items", [])
        assert isinstance(items, list)
        for idx, item in enumerate(items):
            for key in ["id", "name", "category_id", "description", "published"]:
                assert key in item
            assert isinstance(item["id"], str), f"Поле id имеет тип {type(item["id"])}, а должна int"
            assert isinstance(item["name"], str)
            assert isinstance(item["category_id"], str), f"Поле id имеет тип {type(item["id"])}, а должна int"
            assert isinstance(item["description"], str)
            assert isinstance(item["published"], bool)
        

            # parameters
            params = item.get("parameters", [])
            for pidx, param in enumerate(params):
                # id
                assert "id" in param, f"Отсутствует поле 'id' в item[{idx}].parameters[{pidx}]"
                assert isinstance(param["id"], (int, str)), f"item[{idx}].parameters[{pidx}].id должен быть int или str"
                if isinstance(param["id"], str):
                    assert param["id"].isdigit(), f"item[{idx}].parameters[{pidx}].id строка должна содержать только цифры"

                # cost и old_cost
                for key in ["cost", "old_cost", "proteins", "fats", "carbohydrates", "calories", "bonuses"]:
                    if key in param:
                        val = param[key]
                        assert isinstance(val, (int, float, str)), f"item[{idx}].parameters[{pidx}].{key} неверного типа: {type(val)}"

                # description
                assert "description" in param and isinstance(param["description"], str)

            # bonuses_settings
            bonuses_settings = item.get("bonuses_settings", {})
            for bkey in ["accrual", "withdraw"]:
                assert bkey in bonuses_settings

            # cart_settings
            cart_settings = item.get("cart_settings", {})
            for ckey in ["minimum_sum", "discount", "free_delivery", "modifiers_multiplier"]:
                assert ckey in cart_settings

            # seo
            seo = item.get("seo", {})
            assert "friendly_url" in seo

        # --- modifiers_groups ---
        modifiers_groups = data_block.get("modifiers_groups", [])
        for mg in modifiers_groups:
            for key in ["id", "name", "type", "minimum", "maximum"]:
                assert key in mg
            modifiers = mg.get("modifiers", [])
            for mod in modifiers:
                for mkey in ["id", "name", "cost", "group_id", "vendor_code"]:
                    assert mkey in mod, f"Ожидалось, что поле {mkey} есть в {mod}.modifiers group"

    def post_chat(self, action):
        """Управление сообщениями"""
        
        endpoint = Firm.firm_chat
        body = {}
        files = None
        use_data = True

        if action == "default":
            body = {
                "limit": 10,
                "after_message_id": 12,
                "before_message_id": 3
            }
        elif action == "message_statuses":
            body = {
            "messages_ids": [
                    123,
                    2454,
                    3452
                ]
            }
        elif action == "send_message":
            body = {
            "message": "test_text"
            }
        elif action == "send_image":
            endpoint = Firm.firm_chat_img
            use_data = False
            body = {
                "name": "test_image"
            }
            with open("tests/files/test_img_offers.png", "rb") as f:
                files = {
                "image": ("test_image.png", f, "image/png")
                }

        if action != "send_image":
            response = self.post(
                endpoint=f"{Firm.firm_chat}?action={action}",
                json=body,
                timeout=50
                )
        else:
            response = self.post(
                endpoint=f"{Firm.firm_chat_img}?action={action}",
                data=body,
                files=files,
                timeout=50
                )
        return self.post(
            endpoint=f"{endpoint}?action={action}",
            json=body if use_data else None,
            data=body if not use_data else None,
            files=files,
            timeout=50
        )

    def get_couriers(self, action):
        """История перемещения текущего курьера"""

        response = self.get(endpoint=f"{Firm.firm_couriers}?action={action}", timeout=50)
        return response

    def validation_fields_couriers(self, data: Dict[str, str] = None) -> None:
        """
        Валидация полей для GET курьерского приложения
        """

        data_block = data["data"]

        #======data======
        for key in ["name", "settings"]:
            assert key in data_block

        #======name======
        assert isinstance(data_block["name"], str), f"Ожидалось, что name содержит тип str, но содержит тип - {type(data_block["name"])}"

        #======settings======
        assert "settings" in data_block
        settings = data_block.get("settings", {})
        for key in ["distribution_method", "independence", "currency", "formats", "bonus"]:
            assert key in settings
            if key == "distribution_method":
                assert isinstance(settings[key], str), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(settings[key])}"
            elif key == "independence":
                assert isinstance(settings[key], bool), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(settings[key])}"

        currency = settings.get("currency", {})
        assert isinstance(currency, dict)
        for key in ["code", "round", "text"]:
            assert key in currency
            if key == "code":
                assert isinstance(currency[key], str), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(currency[key])}"
            elif key == "round":
                assert isinstance(currency[key], int), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(currency[key])}"
            else:
                for key_text in ["symbol", "short", "middle"]:
                    assert key_text in currency[key]
                    assert isinstance(currency[key][key_text], str), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(currency[key][key_text])}"

        formats = settings.get("formats", {})
        assert isinstance(formats, dict)
        for key in ["date", "cost"]:
            assert key in formats
            assert isinstance(formats[key], str), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(settings[key])}"
        assert datetime.strptime(formats["date"], "%H:%M %d/%m/%Y"), f"Не верный формат даты, должен быть '%H:%M %d/%m/%Y', а вернулось {formats["data"]}"

        bonus = settings.get("bonus", {})
        assert isinstance(bonus, dict)
        for key in ["text", "round", "symbol"]:
            assert key in bonus
            if key != "round":
                assert isinstance(bonus[key], str), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(bonus[key])}"
            else:
                assert isinstance(bonus[key], int), f"Ожидалось, что тип поля {key} - str, но вернул тип - {type(bonus[key])}"

    def post_couriers(self, action, status_order, order_id, current_location, telemetry_history):
        """Управление курьера"""

        body = {}
        
        if action == "orders":
            body = {
                "type": "free",
                "districts_ids": [
                    1224,
                    1225
                ]
            }
        elif action == "set_order_status":
            body = {
                "status": status_order,
                "order_id": order_id
            }
        
        elif action == "take_orders":
            body = {
                "orders_ids": [
                    order_id
                ]
            }
        
        elif action == "release_orders":
            body = {
                "orders_ids": [
                    order_id
                ]
            }

        elif action == "set_current_location":
            body = current_location
        
        elif action == "set_telemetry_history":
            body = telemetry_history
        
        response = self.post(endpoint=f"{Firm.firm_couriers}?action={action}", json=body, timeout=50)
        return response
   
    def validation_fields_couriers_orders(self, data: Dict[str, str] = None) -> None:
        """
        Проверка наличия и валидация полей для post couriers orders
        """

        data_block = data["data"]

        status_order = [
            "not_processed",
            "confirmed",
            "canceled",
            "wait_to_kitchen",
            "in_kitchen",
            "cooked",
            "assembly",
            "wait_remade",
            "ready_to_transit",
            "in_transit",
            "done"
        ]

        prepayment = [
            "paid",
            "not_paid",
            "waiting"
        ]

        payment_method = [
            "cash",
            "online",
            "card_upon_receipt"
        ]

        delivery_method = [
            "courier",
            "pickup"
        ]

        #======data======
        for key in [
            "id", "order_number", "total", "sender_name", "sender_phone_number", "street", "house", "latitude", "longitude", "persons", "date", "timestamp_countdown",
            "minutes_to_done", "contactless_service", "cutlery", "not_call_back", "district_name", "city_name", "operator_phone_number", "operator_phone", "sender_phone"
            ]:
            if key in ["latitude", "longitude"]:
                assert isinstance(data_block[key], int), f"Ожидалось, что тип поля {key} - int, но вернулось {type(data_block[key])}"
            elif key in ["cutlery", "not_call_back"]:
                assert isinstance(data_block[key], bool), f"Ожидалось, что тип поля {key} - bool, но вернулось {type(data_block[key])}"
            else:
                assert isinstance(data_block[key], str), f"Ожидалось, что тип поля {key} - str, но вернулось {type(data_block[key])}"
        assert "cart" in data_block
        assert "items" in data_block["cart"]
        assert isinstance(data_block["cart"]["items"], list)
        items = data_block["cart"].get("items", [])
        for idx, item in enumerate(items):
            for key in ["id", "name", "description", "count", "cost", "settings"]:
                assert key in item, f"Ожидалось, что item.{idx} есть поле {key}"
                if key == "count":
                    assert isinstance(item[key], int), f"Ожидалось, что тип поля {key} - int, но вернулось {type(item[key])}"
                else:
                    assert isinstance(item[key], str), f"Ожидалось, что тип поля {key} - str, но вернулось {type(item[key])}"
            settings = item.get("settings", [])
            for sidx, setting in enumerate(settings):
                for key_settings in ["free_delivery", "minimum_sum", "modifiers_multiplier", "stock_balance"]:
                    assert key_settings in setting, f"Отсутвует поле {key_settings} в item.{idx} settings.{sidx}"
                    assert isinstance(setting[key_settings], bool), f"Ожидалось, что тип поля {key_settings} - bool, но вернулось {type(setting[key_settings])} для item.{idx} settings.{sidx}"
        
        assert "status_order" in data_block
        assert isinstance(data_block["status_order"], str)
        assert data_block["status_order"] in status_order

        assert "prepayment" in data_block
        assert isinstance(data_block["prepayment"], str)
        assert data_block["prepayment"] in prepayment

        assert "payment_method" in data_block
        assert isinstance(data_block["payment_method"], str)
        assert data_block["payment_method"] in payment_method

        assert "delivery_method" in data_block
        assert isinstance(data_block["delivery_method"], str)
        assert data_block["delivery_method"] in delivery_method

    def get_feedback(self, message, feedback_id, action):
        """Метод жалобы"""

        response = self.get(endpoint=f"{Firm.firm_feedback}?action={action}&message={message}&feedback_id={feedback_id}", timeout=50)
        return response

    def post_feedback(self, numbrs, secound_number, action, order_id, text_new, order_status):
        """Форма обратной связи"""
        body = {}

        if action == "cache_fields_default":
            body = {
                "type": "client",
                "limit": numbrs,
                "last_receive_id": secound_number
            }

        elif action == "default":
            body = {
                "type": "client"
            }

        elif action == "new":
            body = {
                "order_id": order_id,
                "text": text_new,
                "status": order_status
            }

        response = self.post(endpoint=f"{Firm.firm_feedback}?action={action}", json=body, timeout=50)
        return response

    def validation_fields_feedback_default(self, data: Dict[str, str] = None) -> None:
        """
        Проверка и валидация полей для метода feedback default
        """
        
        status = [
            "positive",
            "negative"
        ]

        data_block = data["data"]
        assert isinstance(data_block, list)

        for idx, data_list in enumerate(data_block):
            for key in ["id", "date", "text", "status", "answer", "published", "name"]:
                assert key in data_list, f"Ожидалось, что в data.{idx} - поле {key} есть в ответе"
                if key == "id":
                    assert isinstance(data_list[key], int), f"Ожидалось, что в data.{idx} поле {key} тип поля - int, но вернулось {type(data_list[key])}"
                elif key == "published":
                    assert isinstance(data_list[key], bool), f"Ожидалось, что в data.{idx} поле {key} тип поля - int, но вернулось {type(data_list[key])}"
                else:
                    assert isinstance(data_list[key], str), f"Ожидалось, что в data.{idx} поле {key} тип поля - int, но вернулось {type(data_list[key])}"
            assert data_list["status"] in status, f'{data_list["status"]} отсутствует в списке ожидаемых статусов'
            assert isinstance(datetime.strptime(data_list["date"], "%Y-%m-%d %H:%M:%S"), datetime), f"Дата '{data_list["date"]}' не соответствует формату '%Y-%m-%d %H:%M:%S'"

    def validation_fields_feedback_orders(self, data: Dict[str, str] = None) -> None:
        """
        Проверка валидации полей feedback orders
        """

        data_block = data["data"]
        assert isinstance(data_block, list)

        for idx, data_list in enumerate(data_block):
            for key in ["id", "number", "date"]:
                if key != "date":
                    assert isinstance(data_list[key], int), f"Ожидалось что в data.{idx} поле {key} имеет тип int, но вернулось - {type(data_list[key])}"
                else:
                    assert isinstance(data_list[key], str), f"Ожидалось что в data.{idx} поле {key} имеет тип int, но вернулось - {type(data_list[key])}"

    def get_geocoding(self):
        """
        возвращает сервисы поиска координат или поиск мест по координатам (обратное геокодирование)
        """
        with allure.step("возвращает сервисы поиска координат или поиск мест по координатам"):
            response = self.get(endpoint=f"{Firm.firm_geocoding}?action=protocol", timeout=50)
            return response

    def validaion_fields_geocoding(self, data:Dict[str, str] = None) -> None:
        """Проверка наличия и валидации полей геокодирования"""

        data_block = data["data"]

        #======data======
        assert isinstance(data_block, dict)
        for key in ["protected", "search", "reverse"]:
            assert key in data_block, f"Поле {key} отсутствует в блоке ответа"
        #======protected======
        assert isinstance(data_block["protected"], bool), f'Ожидалось, что поле protected имеет тип bool, но вернулось {type(data_block["protected"])}'
        #======search======
        search = data_block.get("search", {})
        assert isinstance(search, dict)
        for key_search in ["url", "method", "type"]:
            assert key_search in search, f"Поле {key_search} отсутствует в блоке ответа search"
            assert isinstance(search[key_search], str), f'Ожидалось, что поле {key_search} имеет тип str, но вернулось {type(search[key_search])}'
        #==========fields==========
        fields = search.get("fields", {})
        assert isinstance(fields, dict)
        for key_fields in ["mutables", "constants"]:
            assert key_fields in fields, f"Поле {key_fields} отсутствует в блоке ответа fields"
        #===============mutables===============
        mutables = fields.get("mutables", {})
        assert isinstance(mutables, dict)
        for key_mutables in ["search"]:
            assert key_mutables in mutables, f"Поле {key_mutables} отсутствует в блоке ответа mutables"
            assert isinstance(mutables[key_mutables], str), f'Ожидалось, что поле {key_mutables} имеет тип str, но вернулось {type(mutables[key_mutables])}'
        assert "viewbox" in mutables
        assert isinstance(mutables["viewbox"]["field"], str), f'Ожидалось, что поле field имеет тип str, но вернулось {type(mutables["viewbox"]["field"])}'
        assert isinstance(mutables["viewbox"]["format"], str), f'Ожидалось, что поле format имеет тип str, но вернулось {type(mutables["viewbox"]["format"])}'
        #===============constants===============
        constants = fields.get("constants", {})
        assert isinstance(constants, dict)
        for key_constants in ["apikey", "format", "results", "rspn", "lang"]:
            assert key_constants in constants, f"Поле {key_constants} отсутствует в блоке ответа constants"
            assert isinstance(constants[key_constants], str), f'Ожидалось, что поле {key_constants} имеет тип str, но вернулось {type(constants[key_constants])}'
        #==========response==========
        response = search.get("response", {})
        assert isinstance(response, dict)
        for key_response in ["find", "fields"]:
            assert key_response in response, f"Поле {key_response} отсутствует в блоке ответа response"
        #===============find===============
        assert isinstance(response["find"]["type"], str), f'Ожидалось, что поле type имеет тип str, но вернулось {type(response["find"]["type"])}'
        assert isinstance(response["find"]["path"], str), f'Ожидалось, что поле path имеет тип str, но вернулось {type(response["find"]["path"])}'
        #===============fields===============
        fields_response = response.get("fields", {})
        assert isinstance(fields_response, dict)
        for key_fields_response in ["title", "description", "country", "city", "street", "house", "zip_code", "latitude", "longitude", "address_line_1"]:
            assert key_fields_response in fields_response, f"Поле {key_fields_response} отсутствует в блоке ответа response"
            if not key_fields_response in ["latitude", "longitude"]:
                assert isinstance(fields_response[key_fields_response], str), f'Ожидалось, что поле {key_fields_response} имеет тип str, но вернулось {type(fields_response[key_fields_response])}'
            else:
                for key_coordinates in ["action", "path", "position", "type"]:
                    assert key_coordinates in fields_response[key_fields_response], f"Поле {key_coordinates} отсутствует в блоке ответа response.fields.{key_fields_response}"
                    if key_coordinates == "position":
                        assert isinstance(fields_response[key_fields_response][key_coordinates], int), f'Ожидалось, что поле {key_coordinates} имеет тип int, но вернулось {type(fields_response[key_fields_response][key_coordinates])}'
                    else:
                        assert isinstance(fields_response[key_fields_response][key_coordinates], str), f'Ожидалось, что поле {key_coordinates} имеет тип str, но вернулось {type(fields_response[key_fields_response][key_coordinates])}'
        assert "check_coordinates" in response
        assert isinstance(response["check_coordinates"], dict), f'Ожидалось, что поле check_coordinates имеет тип str, но вернулось {type(response["check_coordinates"])}'
        #======reverse======
        reverse = data_block.get("reverse", {})
        assert isinstance(reverse, dict)
        for key_reverse in ["url", "method", "type"]:
            assert key_reverse in reverse, f"Поле {key_reverse} отсутствует в блоке ответа reverse"
            assert isinstance(reverse[key_reverse], str), f'Ожидалось, что поле {key_reverse} имеет тип str, но вернулось {type(reverse[key_reverse])}'
        #==========fields==========
        fields_reverse = reverse.get("fields", {})
        assert isinstance(fields_reverse, dict)
        for key_fields_reverse in ["mutables", "constants"]:
            assert key_fields_reverse in fields_reverse, f"Поле {key_fields_reverse} отсутствует в блоке ответа reverse.fields"
            #===============mutables===============
            if key_fields_reverse == "mutables":
                mutables_reverse = fields_reverse.get("mutables", {})
                assert isinstance(mutables_reverse, dict)
                for key_mutables_reverse in ["coordinates"]:
                    assert key_mutables_reverse in mutables_reverse, f"Поле {key_mutables_reverse} отсутствует в блоке ответа reverse.mutables"
                    for key_coordinates_mutables_reverse in ["field", "format"]:
                        assert key_coordinates_mutables_reverse in mutables_reverse[key_mutables_reverse]
                        assert isinstance(mutables_reverse[key_mutables_reverse][key_coordinates_mutables_reverse], str), (
                            f'Ожидалось, что поле {key_coordinates_mutables_reverse} имеет тип str, но вернулось {type(mutables_reverse[key_mutables_reverse][key_coordinates_mutables_reverse])}'
                            )
            #===============constants===============
            else:
                constants_reverse = fields_reverse.get("constants", {})
                assert isinstance(constants_reverse, dict)
                for key_constants_reverse in ["apikey", "kind", "format", "results", "lang"]:
                    assert key_constants_reverse in constants_reverse, f"Поле {key_constants_reverse} отсутствует в блоке ответа reverse.constants"
                    assert isinstance(constants_reverse[key_constants_reverse], str), f'Ожидалось, что поле {key_constants_reverse} имеет тип str, но вернулось {type(constants_reverse[key_constants_reverse])}'
        #==========response==========
        response_reverse = reverse.get("response", {})
        assert isinstance(response_reverse, dict)
        for key_response_reverse in ["find", "fields"]:
            assert key_response_reverse in response_reverse, f"Поле {key_response_reverse} отсутствует в блоке ответа reverse.response"
            #===============find===============
            if key_response_reverse == "find":
                assert "type" in response_reverse[key_response_reverse]
                assert isinstance(response_reverse[key_response_reverse]["type"], str), f'Ожидалось, что поле {key_response_reverse} имеет тип str, но вернулось {type(response_reverse[key_response_reverse]["type"])}'
                assert isinstance(response_reverse[key_response_reverse]["path"], str), f'Ожидалось, что поле {key_response_reverse} имеет тип str, но вернулось {type(response_reverse[key_response_reverse]["path"])}'
            #===============fields===============
            else:
                fields_response_reverse = response_reverse.get("fields", {})
                assert isinstance(fields_response_reverse, dict)
                for key_fields_response_reverse in ["title", "description", "country", "city", "street", "house", "zip_code", "latitude", "longitude", "address_line_1"]:
                    assert key_fields_response_reverse in fields_response_reverse, f"Поле {key_fields_response_reverse} отсутствует в блоке ответа reverse.response.fields"
                    if not key_fields_response_reverse in ["latitude", "longitude"]:
                        assert isinstance(fields_response_reverse[key_fields_response_reverse], str), f'Ожидалось, что поле {key_fields_response_reverse} имеет тип str, но вернулось {type(fields_response_reverse[key_fields_response_reverse])}'
                    else:
                        for key_coordinates_reverse in ["action", "path", "position", "type"]:
                            assert key_coordinates_reverse in fields_response_reverse[key_fields_response_reverse], f"Поле {key_coordinates_reverse} отсутствует в блоке ответа response.fields.{key_fields_response_reverse}"
                            if key_coordinates_reverse == "position":
                                assert isinstance(fields_response_reverse[key_fields_response_reverse][key_coordinates_reverse], int), f'Ожидалось, что поле {key_coordinates_reverse} имеет тип int, но вернулось {type(fields_response_reverse[key_fields_response_reverse][key_coordinates_reverse])}'
                            else:
                                assert isinstance(fields_response_reverse[key_fields_response_reverse][key_coordinates_reverse], str), f'Ожидалось, что поле {key_coordinates_reverse} имеет тип str, но вернулось {type(fields_response_reverse[key_fields_response_reverse][key_coordinates_reverse])}'
        assert "check_coordinates" in response_reverse
        assert isinstance(response_reverse["check_coordinates"], dict), f'Ожидалось, что поле check_coordinates имеет тип str, но вернулось {type(response_reverse["check_coordinates"])}'

    def get_locations(self):
        """
        список стран с регионами в них
        """
        with allure.step("список стран с регионами в них"):
            response = self.get(endpoint=f"{Firm.firm_locations}", timeout=50)
            return response
        
    def validation_fields_locations(self, data: Dict[str, str] = None) -> None:

        data_block = data["data"]

        #======data======
        assert isinstance(data_block, dict)
        for key in ["countries", "phone_formats"]:
            assert key in data_block, f"Поле {key} отсутствует в {data_block}"

        #==========countries==========
        countries = data_block.get("countries", [])
        assert isinstance(countries, list)
        for idx, country in enumerate(countries):
            for key_country in ["id", "name", "flag", "zone", "language", "phone_format_id"]:
                assert key_country in country, f"Country.{idx} поле {key_country} отсутствует в country"
                if key_country in ["id", "phone_format_id"]:
                    assert isinstance(country[key_country], int), f"Ожидалось, что поле {key_country} имеет тип - int, но вернулся {type(country[key_country])}"
                else:
                    assert isinstance(country[key_country], str), f"Ожидалось, что поле {key_country} имеет тип - str, но вернулся {type(country[key_country])}"
            #===============currency===============
            assert "currency" in country
            currency = country.get("currency", {})
            assert isinstance(currency, dict)
            for key_currency in ["code", "text"]:
                assert key_currency in currency, f"Country.{idx} поле {key_currency} отсутствует в {currency}"
                if key_currency == "code":
                    assert isinstance(currency[key_currency], str), f"Ожидалось, что поле {key_currency} имеет тип - str, но вернулся {type(currency[key_currency])}"
                else:
                    for key_text in ["symbol", "short", "middle"]:
                        assert key_text in currency[key_currency], f"Country.{idx} поле {key_text} отсутствует в {currency[key_currency]}"
                        assert isinstance(currency[key_currency][key_text], str), f"Ожидалось, что поле {key_text} имеет тип - str, но вернулся {type(currency[key_currency])}"
            #===============bonus===============
            assert "bonus" in country
            bonus = country.get("bonus", {})
            assert isinstance(bonus, dict)
            for key_bonus in ["text", "round", "symbol"]:
                assert key_bonus in bonus, f"Country.{idx} поле {key_bonus} отсутствует в {bonus}"
                assert isinstance(bonus[key_bonus], str), f"Ожидалось, что поле {key_bonus} имеет тип - str, но вернулся {type(bonus[key_bonus])}"
            #===============formats===============
            assert "formats" in country
            formats = country.get("formats", {})
            assert isinstance(formats, dict)
            for key_formats in ["date", "cost"]:
                assert key_formats in formats, f"Country.{idx} поле {key_formats} отсутствует в {formats}"
                assert isinstance(formats[key_formats], str), f"Ожидалось, что поле {key_formats} имеет тип - int, но вернулся {type(formats[key_formats])}"
            #===============cities===============
            assert "cities" in country
            cities = country.get("cities", [])
            assert isinstance(cities, list)
            for cidx, city in enumerate(cities):
                for key_city in ["id", "name", "timezone"]:
                    assert key_city in city, f"Country.{idx}/city.{cidx} поле {key_city} отсутствует в {city}"
                    assert isinstance(city[key_city], str), f"Ожидалось, что поле {key_city} имеет тип - str, но вернулся {type(city[key_city])}"
                #===============districts===============
                assert "districts" in city
                districts = city.get("districts", [])
                assert isinstance(districts, list)
                for didx, district in enumerate(districts):
                    for key_district in ["id", "name", "branch_id", "chain_id", "account_id", "redirect_district_id"]:
                        assert key_district in district, f"Country.{idx}/city.{cidx}/district.{didx} поле {key_district} отсутствует в district"
                        if key_district in ["id", "name", "branch_id", "account_id"]:
                            assert isinstance(district[key_district], str), f"Ожидалось, что поле {key_district} имеет тип - str, но вернулся {type(district[key_district])}"
                        else:
                            assert isinstance(district[key_district], int), f"Ожидалось, что поле {key_district} имеет тип - int, но вернулся {type(district[key_district])}"
                    #===============currency===============
                    assert "currency" in district, f"Country.{idx}/city.{cidx}/district.{didx} поле currency отсутствует в {district}"
                    assert "round" in district["currency"], f"Country.{idx}/city.{cidx}/district.{didx} поле round отсутствует в currency"
                    for key_round in ["precision", "mode"]:
                        assert key_round in district["currency"]["round"], f"Country.{idx}/city.{cidx}/district.{didx} поле {key_round} отсутствует в round"
                        assert isinstance(district["currency"]["round"][key_round], str), f"Ожидалось, что поле {key_round} имеет тип - str, но вернулся {type(district["currency"]["round"][key_round])}"
                    #===============work_time===============
                    assert "work_time" in district, f"Country.{idx}/city.{cidx}/district.{didx} поле work_time отсутствует в {district}"
                    work_time = district.get("work_time", {})
                    for key_work_time in ["splitted", "glued"]:
                        assert key_work_time in work_time, f"Country.{idx}/city.{cidx}/district.{didx} поле {key_work_time} отсутствует в {work_time}"
                        if key_work_time == "splitted":
                            for key_splitted in ["1", "2", "3", "4", "5", "6", "7"]:
                                assert key_splitted in work_time[key_work_time], f"Country.{idx}/city.{cidx}/district.{didx} поле {key_splitted} отсутствует в {work_time[key_work_time]}"
                                for key_numbers in ["parameter", "times"]:
                                    assert key_numbers in work_time[key_work_time][key_splitted], f"Country.{idx}/city.{cidx}/district.{didx} поле {key_numbers} отсутствует в {work_time[key_work_time][key_splitted]}"
                                    if key_numbers == "parameter":
                                        assert isinstance(work_time[key_work_time][key_splitted][key_numbers], int), f"Ожидалось, что поле parameter имеет тип - int, но вернулся {type(work_time[key_work_time][key_splitted][key_numbers])}"
                                    else:
                                        assert isinstance(work_time[key_work_time][key_splitted][key_numbers], list), f"Ожидалось, что поле times имеет тип - list, но вернулся {type(work_time[key_work_time][key_splitted][key_numbers])}"
                                        for tidx, time in enumerate(work_time[key_work_time][key_splitted][key_numbers]):
                                            assert isinstance(time, str), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx}/times.{tidx} поле times имеет тип - str, но вернулся {type(time)}"
                        else:
                            for key_glued in ["1", "2", "3", "4", "5", "6", "7"]:
                                assert key_glued in work_time[key_work_time], f"Country.{idx}/city.{cidx}/district.{didx} поле {key_glued} отсутствует в {work_time[key_work_time]}"
                                assert isinstance(work_time[key_work_time][key_glued], str), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx} поле {key_glued} имеет тип - str, но вернулся {type(work_time[key_work_time][key_glued])}"
                    #===============settings===============
                    assert "settings" in district, f"Country.{idx}/city.{cidx}/district.{didx} поле settings отсутствует в {district}"
                    settings = district.get("settings", {})
                    for key_settings in ["delivery_time", "other_delivery_time", "other_delivery_time_enabled", "cost_of_delivery", "free_delivery_from", "paid_delivery_enabled", "minimum_order_amount", "other_minimum_order_amount", "other_minimum_order_amount_enabled"]:
                        assert key_settings in settings, f"Country.{idx}/city.{cidx}/district.{didx} поле {key_settings} отсутствует в {settings}"
                        if key_settings in ["other_delivery_time_enabled", "paid_delivery_enabled", "other_minimum_order_amount_enabled"]:
                            assert isinstance(settings[key_settings], bool), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx}/times.{tidx} поле {key_settings} имеет тип - bool, но вернулся {type(settings[key_settings])}"
                        else:
                            assert isinstance(settings[key_settings], str), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx}/times.{tidx} поле {key_settings} имеет тип - str, но вернулся {type(settings[key_settings])}"
                    
                    assert "other_delivery_time_periods" in settings, f"Country.{idx}/city.{cidx}/district.{didx} поле other_delivery_time_periods отсутствует в {settings}"
                    assert isinstance(settings["other_delivery_time_periods"], list), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx}/times.{tidx} поле other_delivery_time_periods имеет тип - list, но вернулся {type(settings["other_delivery_time_periods"])}"
                    for sidx, time_period in enumerate(settings["other_delivery_time_periods"]):
                        assert isinstance(time_period, str), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx}/times.{tidx}/other_delivery.{sidx} поле {time_period} имеет тип - str, но вернулся {type(time_period)}"

                    assert "other_minimum_order_amount_periods" in settings, f"Country.{idx}/city.{cidx}/district.{didx} поле other_minimum_order_amount_periods отсутствует в {settings}"
                    assert isinstance(settings["other_minimum_order_amount_periods"], list), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx}/times.{tidx} поле other_minimum_order_amount_periods имеет тип - list, но вернулся {type(settings["other_minimum_order_amount_periods"])}"
                    for pidx, other_minimum in enumerate(settings["other_minimum_order_amount_periods"]):
                        assert isinstance(other_minimum, str), f"Ожидалось, что Country.{idx}/city.{cidx}/district.{didx}/times.{tidx}/other_order.{pidx} поле {other_minimum} имеет тип - str, но вернулся {type(other_minimum)}"
                #===============coordinates===============
                assert "coordinates" in city, f"Country.{idx}/city.{cidx} поле coordinates отсутствует в {city}"
                assert isinstance(city["coordinates"], dict), f"Ожидалось, что Country.{idx}/city.{cidx} поле coordinates имеет тип - dict, но вернулся {type(city["coordinates"])}"
                coordinates = city.get("coordinates", {})
                for key_coordinates in ["latitude", "longitude"]:
                    assert key_coordinates in coordinates, f"Country.{idx}/city.{cidx} поле {key_coordinates} отсутствует в {coordinates}"
                    assert isinstance(coordinates[key_coordinates], str), f"Ожидалось, что Country.{idx}/city.{cidx} поле {key_coordinates} имеет тип - str, но вернулся {type(coordinates[key_coordinates])}"
        #===============phone_formats===============
        assert "phone_formats" in data_block, f"Поле phone_formats отсутствует в {data_block}"
        phone_formats = data_block.get("phone_formats", [])
        assert isinstance(phone_formats, list), f"Ожидалось, что поле {phone_formats} имеет тип - list, но вернулся {type(phone_formats)}"
        for pfidx, phone_format in enumerate(phone_formats):
            for key_phone_format in ["id", "mask", "regex"]:
                assert key_phone_format in phone_format, f"Phone_format.{pfidx} поле {key_phone_format} отсутствует в {phone_format}"
                if key_phone_format == "id":
                    assert isinstance(phone_format[key_phone_format], int), f"Ожидалось, что Phone_format.{pfidx} поле {key_phone_format} имеет тип - int, но вернулся {type(phone_format[key_phone_format])}"
                else:
                    assert isinstance(phone_format[key_phone_format], str), f"Ожидалось, что Phone_format.{pfidx} поле {key_phone_format} имеет тип - str, но вернулся {type(phone_format[key_phone_format])}"
            assert "country" in phone_format, f"Phone_format.{pfidx} поле country отсутствует в {phone_format}"
            country_pf = phone_format.get("country", {})
            for key_country_pf in ["name", "flag", "code"]:
                assert key_country_pf in country_pf, f"Phone_format.{pfidx} поле {key_country_pf} отсутствует в {country_pf}"
                assert isinstance(country_pf[key_country_pf], str), f"Ожидалось, что поле {key_country_pf} имеет тип - str, но вернулся {type(country_pf[key_country_pf])}"

