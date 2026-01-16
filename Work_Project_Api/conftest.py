"""
Конфигурация Pytest для API автотестов.
Обеспечивает фикстуры для сессии requests и отчетов Allure.
"""
import sys
import os
from pathlib import Path
import pytest
import requests
import allure
from dotenv import load_dotenv
import uuid
import shutil
import json
import time
from utils.endpoints import Firm, Client
from scheme.client_scheme import SignInByPhoneSuccessData
from typing import Any, List, Dict, Callable
from typing_extensions import TypedDict
from core.BaseAPI import HTTPClient
from configs.config import Config
from core.assertions import assert_status_code
import logging

# -----------------------------
# Добавляем корень проекта в sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Загружаем .env (например .env.love)
dotenv_path = PROJECT_ROOT / ".env.love"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
# -----------------------------

from utils.api_auth import APIAuth
from utils.request_logger import live_format_request_response

# -----------------------------
# Фикстура для корня проекта
@pytest.fixture(scope="session")
def root_dir():
    return PROJECT_ROOT

# -----------------------------
@pytest.fixture(autouse=True)
def patch_requests(monkeypatch):
    original_request = requests.request
    original_session_request = requests.Session.request

    def traced_request(method, url, **kwargs):
        resp = original_request(method, url, **kwargs)
        mask_token = "/application?action=authorization" in url
        live_format_request_response(resp, mask_access_token=mask_token)
        return resp

    def traced_session_request(self, method, url, **kwargs):
        resp = original_session_request(self, method, url, **kwargs)
        mask_token = "/application?action=authorization" in url
        live_format_request_response(resp, mask_access_token=mask_token)
        return resp

    monkeypatch.setattr(requests, "request", traced_request)
    monkeypatch.setattr(requests.Session, "request", traced_session_request)

# Сессия для авторизации (можно использовать для всех запросов)
@pytest.fixture(scope="function")
def auth_headers(make_uuid):
    """
    Фикстура для авторизации с динамической сигнатурой.
    Возвращает headers с токеном для всех последующих запросов.
    """

    # logging.info(make_uuid)
    
    api_auth = APIAuth(make_uuid=make_uuid)

    with allure.step("Авторизация - получаем токен доступа для взаимодействия с api сервиса"):
        token = api_auth.get_access_token(make_uuid=make_uuid)

    api_auth.refresh_signature(uuid=make_uuid, token_access=token)

    headers = api_auth.headers.copy()
    headers["token-access"] = token

    return headers

@pytest.fixture(scope="function")
def courier_session_id(api_client: HTTPClient) -> str:
    """
    Выполняет авторизацию курьера и возращает session_id
    Применим только для методов курьера
    """

    with allure.step("метод (sign_in) авторизация курьера"):
        response = api_client.request(
            method="post",
            endpoint=Firm.FIRM_COURIERS.value,
            params={"action": "sign_in"},
            json={
                "login": f"{Config.LOGIN_COURIER}",
                "password": f"{Config.PASSWORD_COURIER}",
                "captcha": "***DEMO***"
                }
            )
        assert_status_code(response=response, expected_status=200)
    return response.json()["data"]["session_id"]

@pytest.fixture(scope="function")
def courier_session_headers(
    auth_headers: Dict[str, Any],
    courier_session_id: str
    ) -> Dict[str, Any]:
    """Добавляем заголовок session_id к имеющимся заголовкам, только для методов /firm/couriers?action=***
    
    :param auth_headers: Заголовки запроса
    :type auth_headers: Dict[str, Any]
    :param courier_session_id: Передаем session_id после авторизации курьера
    :type courier_session_id: str
    :return: Dict[str, Any]
    """

    headers = auth_headers.copy()
    headers["session"] = courier_session_id

    return headers

@pytest.fixture(scope="function")
def order_session_headers(
    auth_headers: Dict[str, Any]
    ) -> Dict[str, Any]:
    """Добавляем заголовок pickup к имеющимся заголовкам, только для метода /firm/order

    :param auth_headers: Заголовки запроса
    :type auth_headers: Dict[str, Any]
    :return: Dict[str, Any]"""
    headers = auth_headers.copy()
    headers["pickup"] = "***DEMO***"

    return headers

@pytest.fixture(scope="function")
def login_with_phone(api_client: HTTPClient) -> Dict[str, Any]:
    """Выполняет авторизацию клиента по номеру телефона и возвращает session"""

    with allure.step(f"Отправляем запрос на метод {Client.CLIENT.value}?action=sign_in_by_phone"):
        # logging.info(api_client.session.headers)
        response = api_client.request(
            method="post",
            endpoint=Client.CLIENT.value,
            params={"action": "sign_in_by_phone"},
            json={
                    "security_code": "***DEMO***",
                    "phone": {
                        "format_id": 1,
                        "number": "+79***DEMO***"
                    }
                }
            )

    with allure.step("Проверяем валидацию ответа"):
        assert_status_code(response=response, expected_status=200)
        SignInByPhoneSuccessData.model_validate(response.json())
    session_id = response.json()["data"]["session_id"]
    headers = api_client.session.headers.copy()
    headers["session"] = session_id

    yield headers # передаем заголовки тесту

    time.sleep(3) #Необходимо делать неявные паузы, так как иначе сервер вернет ошибку частых запросов

    with allure.step("Выходим из аккаунта после завершения теста"):
        try:
            logout_response = api_client.request(
                method='post',
                endpoint=Client.CLIENT.value,
                params={"action": "sign_out"}
            )
            assert_status_code(response=logout_response, expected_status=200)
        except Exception as e:
            logging.warning(f"Не удалось выйти из аккаунта:\n{e}")

class AddressStoreFixture(TypedDict):
    add: Callable[[str, Any], None]
    get: Callable[[str], List[Any]]
    pop_one: Callable[[str, int], Any]
    store: Dict[str, List[Any]]

STORE_FILE = "address_store.json"

@pytest.fixture(scope="session")
def address_store() -> AddressStoreFixture:
    """
    Хранилище данных между тестами
    Формат файла:
    {
        "<key>": [value1, value2, ...]
    }
    """
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r", encoding='utf-8') as f:
            store = json.load(f)
    else:
        store = {}
    
    def add(key: str, value: Any) -> None:
        """
        Добавляет значение в список по ключу
        
        :param key: Ключ в хранилище
        :type key: str
        :param value: Любое JSON-сериализуемое значение
        :type value: Any
        :return: None
        """
        store.setdefault(key, [])
        store[key].append(value)
        save()

    def get(key: str, index: int = -1) -> List:
        """
        Возвращает список значений по ключу
        
        :param key: Ключ в хранилище
        :type key: str
        :param index: Индекс элемента (по умолчанию последний)
        :type index: int
        :return: List[Any]
        """
        value = store.get(key, [])
        if not value:
            raise AssertionError(f'В store нет значений для ключа "{key}"')
        return value[index]

    def pop_one(key: str, index: int = -1) -> Any:
        """
        Берет одно значение из списка и удаляет его
        По умолчанию это поледний элемент

        :param key: Ключ в хранилище
        :type: key: str
        :param index: Индекс элемента (по умолчанию последний)
        :type index: int
        :return: Any (любое значение из списка)
        """
        values = store.get(key, [])
        if not values:
            raise AssertionError(f'Нечего удалить: список "{key}" пуст')
        value = values.pop(index)
        save()
        return value
    
    def save() -> None:
        """
        Сохраняет текущее состояние store в файл

        :return: None
        """
        with open(STORE_FILE, "w", encoding='utf-8') as f:
            json.dump(store, f, indent=4, ensure_ascii=False)

    return {
        "add": add,
        "get": get,
        "pop_one": pop_one,
        "store": store
    }

@pytest.fixture
def api_client(auth_headers: Dict[str, Any]) -> HTTPClient:
    return HTTPClient(base_url=Config.BASE_URL, headers=auth_headers)

@pytest.fixture
def make_uuid() -> str:
    """Генерация уникального uuid для Header"""
    return str(uuid.uuid4())

ALLURE_RESULTS = Path("reports/allure-results")
ALLURE_REPORT = Path("reports/allure-report")
EXECUTOR = ALLURE_RESULTS / "executor.json"
HISTORY_SRC = ALLURE_REPORT / "history"
HISTORY_DST = ALLURE_RESULTS / "history"

def pytest_configure():
    """
    Перед запуском тестов:
    - очищаем старые результаты (кроме history, executor, environment)
    - восстанавливаем history из последнего отчета
    - создаем executor.json
    """
    # 1. Очистка результатов (кроме history, executor.json, environment.properties)
    if ALLURE_RESULTS.exists():
        for item in ALLURE_RESULTS.iterdir():
            if item.name not in {"history", "executor.json", "environment.properties"}:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

    # 2. Восстановление history из последнего отчета
    if HISTORY_SRC.exists():
        shutil.copytree(HISTORY_SRC, HISTORY_DST, dirs_exist_ok=True)
        print("[Allure] History restored before run")

    # 3. Инициализация history-trend.json, если нет
    HISTORY_DST.mkdir(parents=True, exist_ok=True)
    history_trend_file = HISTORY_DST / "history-trend.json"
    if not history_trend_file.exists():
        history_trend_file.write_text("[]")
        print("[Allure] Initialized empty history-trend.json")

    # 4. Создание executor.json
    generate_executor_json()


def pytest_sessionfinish(session, exitstatus):
    """
    После завершения всех тестов:
    - обновляем history-trend.json
    - генерируем отчет
    - копируем историю обратно в отчет
    - открываем отчет на локальном сервере
    """
    update_history_trend()

    # Генерация отчета
    os.system(f'allure generate "{ALLURE_RESULTS}" -o "{ALLURE_REPORT}" --clean')

    # Копирование истории обратно в отчет
    if HISTORY_DST.exists():
        shutil.copytree(HISTORY_DST, ALLURE_REPORT / "history", dirs_exist_ok=True)
        print("[Allure] History updated for next run")

    # Автооткрытие отчета
    if "CI" not in os.environ:
        os.system(f'allure open "{ALLURE_REPORT}"')
# -----------------------------
# Вспомогательные функции
# -----------------------------
def get_next_build_order() -> int:
    """Берет последний buildOrder из history-trend.json и увеличивает на 1"""
    history_trend_file = HISTORY_DST / "history-trend.json"
    max_order = 0
    if history_trend_file.exists():
        try:
            data = json.loads(history_trend_file.read_text())
            if data:
                max_order = max(item.get("buildOrder", 0) for item in data if isinstance(item.get("buildOrder"), int))
                print(f"[Allure] Max buildOrder from history: {max_order}")
        except Exception as e:
            print(f"[Allure] Ошибка чтения history-trend.json: {e}")
    return max_order + 1


def generate_executor_json():
    """Создает executor.json с информацией о текущем билде"""
    build_order = get_next_build_order()
    date_str = time.strftime("%Y-%m-%d %H:%M")
    executor = {
        "buildOrder": build_order,
        "buildName": f"Run #{build_order} - {date_str}",
        "reportUrl": f"file://{ALLURE_REPORT.resolve()}",
        "name": "Local Pytest",
        "type": "local"
    }
    ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)
    EXECUTOR.write_text(json.dumps(executor, indent=2, ensure_ascii=False))
    print(f"[Allure] Executor created: buildOrder={build_order}")


def update_history_trend():
    """Обновляет history-trend.json после завершения тестов"""
    HISTORY_DST.mkdir(parents=True, exist_ok=True)
    history_trend_file = HISTORY_DST / "history-trend.json"

    # Загружаем старые данные
    if history_trend_file.exists():
        try:
            data = json.loads(history_trend_file.read_text())
        except Exception:
            data = []
    else:
        data = []

    # Собираем статистику по текущему билду
    executor_file = ALLURE_RESULTS / "executor.json"
    executor = json.loads(executor_file.read_text())

    current_build = {
        "buildOrder": executor["buildOrder"],
        "buildName": executor["buildName"],
        "reportUrl": executor["reportUrl"],
        "total": 0,
        "passed": 0,
        "failed": 0,
        "broken": 0,
        "skipped": 0,
        "duration": 0
    }

    # Добавляем новый билд в историю
    data.append(current_build)
    history_trend_file.write_text(json.dumps(data, indent=2))
    print(f"[Allure] history-trend.json updated: buildOrder={executor['buildOrder']}")

