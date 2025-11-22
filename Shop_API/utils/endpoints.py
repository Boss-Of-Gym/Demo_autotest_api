"""
Класс для хранения эндпоинтов API.
Содержит пути к эндпоинтам, чтобы использовать их в тестах.
"""

class Authorization:
    application = "/application" # авторизация

class Client:
    client = "/client" # yправление аккаунтом
    client_address = "/client/address" # адрес доставки управление
    client_addresses = "/client/addresses" # список адресов, временная метка
    client_favorite_items = "/client/favorite_items" # список избранных элементов текущего пользователя
    client_history_order = "/client/history/order" # заказ, местоположение
    client_history_orders = "/client/history_orders" # список заказов текущего пользователя

class Firm:
    firm_about = "/firm/about" # описание филиала фирмы
    firm_application = "/firm/application" # данные филиала
    firm_application_uuid = "/firm/application/uuid" # управление токеном профиля
    firm_branch = "/firm/branch" # возвращает информацию об филиале, категория блюд, список блюд
    firm_chat = "/firm/chat" # управление сообщениями
    firm_chat_img = "/firm/chat/" # отправить изображение
    firm_couriers = "/firm/couriers" # история перемещения текущего курьера
    firm_document = "/firm/document" # возвращает документ по id
    firm_feedback = "/firm/feedback" # жалоба
    firm_geocoding = "/firm/geocoding" # геокодирование
    firm_locations = "/firm/locations" # список стран
    firm_notification_cart = "/firm/notification_cart" # запись, удаление уведомления
    firm_notifications = "/firm/notifications" # уведомления
    firm_order = "/firm/order" # новый заказ
    firm_special_offers = "/firm/special_offers" # специальные предложения
    firm_vacancies = "/firm/vacancies" # список вакансии

class Payment:
    payment = "/payment" # транзакция оплаты
    payments_check = "/payments/check" # запрос на предварительную проверку
    payments_fail = "/payments/fail" # закрывает диалоговое окно
    payments_redirect = "/payments/redirect" # переадресация на платежный адаптор
    payments_success = "/payments/success" # закрывает окно платежного адаптера

class Default:
    locations = "/locations" # список стран