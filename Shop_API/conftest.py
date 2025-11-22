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
import shutil
import json
import time
from pathlib import Path
from configs.config import Config
from utils.endpoints import Firm

# -----------------------------
# Добавляем корень проекта в sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Загружаем .env (например .env.v30)
dotenv_path = PROJECT_ROOT / ".env.v30"
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
def auth_headers():
    """
    Фикстура для авторизации с динамической сигнатурой.
    Возвращает headers с токеном для всех последующих запросов.
    """
    api_auth = APIAuth()

    with allure.step("Авторизация - получаем токен доступа для взаимодействия с api сервиса"):
        token = api_auth.get_access_token()

    api_auth.refresh_signature(token_access=token)

    headers = api_auth.headers.copy()
    headers["token-access"] = token
    
    # print(headers)

    return headers

@pytest.fixture(scope="function")
def courier_session_id(auth_headers):
    """
    Выполняет авторизацию курьера и возращает session_id
    Применим только для методов курьера
    """

    body = {
        "login": f"{Config.LOGIN_COURIER}",
        "password": f"{Config.PASSWORD_COURIER}",
        "captcha": "example_captcha"
        }
        
    url = f"{Config.BASE_URL}{Firm.firm_couriers}?action=sign_in"

    with allure.step("метод (sign_in) авторизация курьера"):
        response = requests.post(url=url, headers=auth_headers, json=body, timeout=50)
        assert response.status_code == 200, f"Ожидался код 200, но вернулся {response.status_code}"
        data = response.json()
        assert "data" in data, 'Ожидалось, что data есть в структуре ответа'
        assert "session_id" in data["data"], "Ожидалось, что session_id есть в структуре ответа в data"
        session_id = data["data"]["session_id"]
        assert isinstance(session_id, str), f"Ожидалось, что session_id имеет тип {type(session_id)}"

    return session_id

@pytest.fixture(scope="function")
def courier_session_headers(auth_headers, courier_session_id):
    """Добавляем заголовок session_id к имеющимся заголовкам, только для методов /firm/couriers?action=***"""

    headers = auth_headers.copy()
    headers["session"] = courier_session_id

    return headers

@pytest.fixture(scope="function")
def order_session_headers(auth_headers):
    """Добавляем заголовок pickup к имеющимся заголовкам, только для метода /firm/order"""
    headers = auth_headers.copy()
    headers["pickup"] = "4961"

    return headers

@pytest.fixture(scope="function")
def order_session_courier_headers(auth_headers):
    """Добавляем заголовок pickup к имеющимся заголовкам, только для метода /firm/order"""
    headers = auth_headers.copy()
    headers["pickup"] = None

    return headers

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

