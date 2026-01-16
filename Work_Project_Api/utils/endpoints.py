"""
Файл в котором хранятся эндпоинты API.
Содержит пути к эндпоинтам для использования их в тестах.
"""

from enum import Enum

class Authorization(str, Enum):
    """
    Возвращает токен доступа к приложению пользователю
    """
    APPLICATION = "/application" # авторизация

class Bag(str, Enum):
    """
    Универсальный метод для работы проекта
    """
    BAG = '/bag'
    BAG_DOCUMENT = BAG + '/document'
    BAG_INFO = BAG + '/info'
    BAG_LOCATIONS = BAG + '/locations'
    BASE = '/base'
    MAIL = '/mail'

class Chain(str, Enum):
    CHAIN = '/chain/about'
    
class Client(str, Enum):
    """
    Метод управления аккаунтом, доставками, адресами, избранными товарами и историей заказов
    """
    CLIENT = "/client"
    CLIENT_ADDRESS = CLIENT + "/address"
    CLIENT_ADDRESSES = CLIENT + "/addresses"
    CLIENT_FAVORITE_ITEMS = CLIENT + "/favorite_items"
    CLIENT_HISTORY_ORDER = CLIENT + "/history/order"
    CLIENT_HISTORY_ORDERS = CLIENT + "/history_orders"

class Firm(str, Enum):
    """
    Метод работы с основным контентом.
    Описание филиала, возвращения товаров, параметров, и так далее.
    Возможность задать вопрос в чат, прислать изображение, вызвать поддержку.
    Метод для работы курьера.
    Возможность создать отзыв о магазине или товарах.
    Возвращение геолокации, геокодинг, уведомления в приложении.
    Метод создания нового заказа и использование спец. предложений.
    Отображение вакансий и отправка анкеты кандидата.
    """
    FIRM = '/firm'
    FIRM_ABOUT = FIRM + "/about"
    FIRM_APPLICATION = FIRM + "/application"
    FIRM_APPLICATION_UUID = FIRM + "/application/uuid"
    FIRM_BRANCH = FIRM + "/branch"
    FIRM_CHAT = FIRM + "/chat"
    FIRM_CHAT_IMG = FIRM + "/chat/"
    FIRM_COURIERS = FIRM + "/couriers"
    FIRM_DOCUMENT = FIRM + "/document"
    FIRM_FEEDBACK = FIRM + "/feedback"
    FIRM_GEOCODING = FIRM + "/geocoding"
    FIRM_LOCATIONS = FIRM + "/locations"
    FIRM_NOTIFICATION_CART = FIRM + "/notification_cart"
    FIRM_NOTIFICATIONS = FIRM + "/notifications"
    FIRM_ORDER = FIRM + "/order"
    FIRM_SPECIAL_OFFERS = FIRM + "/special_offers"
    FIRM_VACANCIES = FIRM + "/vacancies"

class Payment(str, Enum):
    """
    Методы оплаты заказа, создание нового заказа со статусом Ожидания.
    Методы с отслеживанием транзакций, вызов и закрытие окон проверки транзакций.
    """
    PAYMENT = "/payment"
    PAYMENTS = "/payments"
    PAYMENTS_CHECK = PAYMENTS + "/check"
    PAYMENTS_FAIL = PAYMENTS + "/fail"
    PAYMENTS_REDIRECT = PAYMENTS + "/redirect"
    PAYMENTS_SUCCESS = PAYMENTS + "/success"

class Default(str, Enum):
    """
    Возвращает список стран
    """
    LOCATIONS = "/locations"

