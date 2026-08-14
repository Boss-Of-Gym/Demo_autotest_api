# Automation QA Portfolio – Python, Pytest, Requests

* **Автор:** Дмитрий

* **Роль:** Automation QA Engineer

* **Контакты:** <naydanov.dmitriy@gmail.com> • <@DatorDeus>

---

## Краткое описание

Этот репозиторий демонстрирует практический подход к автоматизации тестирования API с использованием **Python**, **HTTPX** и **Pytest**. Цель — показать структуру тестов, применяемые паттерны (Page Object, API-клиенты), удобную генерацию отчётов с помощью **Allure CLI** и готовность репозитория к интеграции в CI.

---

## Технологический стек

* Язык: **Python 3.13.5**
* Тестовый раннер: **Pytest**
* API: **httpx**
* Отчёты: **Allure CLI**

---

## Содержание

1. [Структура проекта](#1-структура-проекта)
2. [Команда запуска](#2-команда-запуска)
3. [Полная схема вызовов](#11-полная-схема-вызовов)

---

## 1. Структура проекта - демонстрационная

```
CRM_API_REFACTORING/
│
├── .env.dev                          ← конфигурация окружения (credentials, URL)
├── pytest.ini                        ← настройки pytest
├── conftest.py                       ← точка входа, загрузка .env, регистрация плагинов
│
├── config/
│   └── settings.py                   ← Pydantic Settings: читает .env.dev → типизированный объект
│
├── core/
│   ├── client.py                     ← BaseHTTPClient: обёртка над httpx
│   └── exceptions.py                 ← иерархия исключений фреймворка
│
├── enums/
│   └── endpoints.py                  ← URL-адреса эндпоинтов (ApplicationEndpoints)
│
├── schemas/
│   ├── authorization/
│   │   ├── request.py                ← Pydantic-модель тела POST-запроса авторизации
│   │   └── response.py               ← Pydantic-модели ответов (AuthorizationResponse, ErrorResponse...)
│   └── user_info/
│       └── response.py               ← Pydantic-модель ответа GET /application.user_info
│
├── services/
│   ├── base.py                       ← BaseService: хранит ссылку на клиент
│   ├── authorization.py              ← AuthorizationService: authorize(), sign_out()
│   └── user_info.py                  ← UserInfoService: get_user_info()
│
├── validators/
│   ├── http.py                       ← проверки на уровне HTTP (статус, заголовки, время)
│   └── response.py                   ← проверки тела ответа (Pydantic-модель, JSON Schema, статус)
│
├── log/
│   └── logger.py                     ← HTTPLogger: форматирование, маскировка, запись в файл и Allure
│
├── fixtures/
│   ├── allure_setup.py               ← pytest-хуки жизненного цикла сессии и отчёта
│   ├── client.py                     ← фикстура api_client (session scope)
│   └── auth.py                       ← фикстуры session_id, authorization_service, user_info_service
│
├── tests/
│   ├── data/
│   │   ├── shared/
│   │   │   ├── types.py              ← датаклассы GetCase и ExpectedResult
│   │   │   └── error_results.py      ← EXPECTED_ERROR: общий ожидаемый результат для ошибок
│   │   ├── authorization/
│   │   │   ├── expected.py           ← EXPECTED_VALID_AUTH
│   │   │   ├── request_body.py       ← ADMIN_AUTH_REQUEST, INVALID_CREDENTIALS_REQUEST
│   │   │   └── test_data.py          ← AUTHORIZATION_TEST_DATA: список pytest.param
│   │   └── user_info/
│   │       ├── expected.py           ← EXPECTED_VALID_USER_INFO
│   │       └── test_data.py          ← USER_INFO_TEST_DATA: список pytest.param
│   ├── test_authorization.py         ← класс TestAuthorization (2 кейса)
│   └── test_user_info.py             ← класс TestUserInfo (1 кейс)
│
└── utils/
    └── pytest_helpers.py             ← generate_test_ids: читаемые ID для Allure
```

---

## 2. Команда запуска

Пример стандартного запуска:

```bash
pytest -m smoke
```

Что означают параметры:
- `pytest` — запускает фреймворк
- `-m smoke` — запускает только тесты с маркером `smoke`

Другие варианты:

```bash
pytest                          # все тесты
pytest -m regression            # только regression
pytest -m "smoke and positive"  # smoke + positive одновременно
pytest -v --tb=short            # подробный вывод, короткий трейсбек
pytest tests/test_authorization.py  # только один файл
```

После запуска pytest читает **`pytest.ini`** и берёт из него настройки:

```ini
[pytest]
testpaths = tests         ← искать тесты в папке tests/
pythonpath = .            ← добавить корень проекта в sys.path (импорты работают как from config.settings ...)
python_files = test_*.py  ← файлы с тестами начинаются на test_
python_classes = Test*    ← классы начинаются на Test
python_functions = test_* ← функции начинаются на test_
addopts =
    --alluredir=reports/allure-results  ← куда сохранять JSON-результаты Allure
    -v                                  ← verbose: показывать каждый тест отдельно
log_cli = true            ← выводить логи в консоль в реальном времени
log_cli_level = INFO      ← минимальный уровень логов в консоли
```

---

## 3. Полная схема вызовов

```
$ pytest -m smoke
│
├── pytest читает pytest.ini
│   └── pythonpath = . → добавляет корень в sys.path
│
├── загружает conftest.py
│   ├── load_dotenv(.env.dev) → заполняет os.environ
│   └── pytest_plugins = ['fixtures.allure_setup', 'fixtures.client', 'fixtures.auth']
│
├── загружает fixtures.allure_setup
│   ├── устанавливает абсолютные пути для reports/
│   └── регистрирует pytest_configure, pytest_sessionstart, pytest_runtest_logreport, pytest_sessionfinish
│
├── загружает fixtures.client
│   └── регистрирует фикстуру api_client (session scope)
│
├── загружает fixtures.auth
│   ├── импортирует ADMIN_AUTH_REQUEST из tests.data.authorization.request_body
│   │   └── вызывает get_settings() → создаёт _Settings() → читает .env.dev
│   └── регистрирует фикстуры session_id, authorization_service, user_info_service
│
├── pytest_configure() вызывается
│   ├── mkdir reports/allure-results/
│   ├── _cleanup_results() → удаляет старые артефакты
│   ├── _restore_history() → копирует history из прошлого отчёта
│   ├── _init_history_trend() → создаёт history-trend.json
│   └── _write_executor() → пишет executor.json с buildOrder
│
├── COLLECTION: pytest обходит tests/
│   ├── импортирует test_authorization.py
│   │   └── generate_test_ids() → создаёт читаемые ID
│   └── импортирует test_user_info.py
│       └── generate_test_ids() → создаёт читаемые ID
│   Итог: 3 тест-кейса
│
├── pytest_sessionstart() → _SESSION_START = time.time()
│
├── api_client fixture создаётся (session scope)
│   ├── get_settings() → из кеша (уже создан)
│   └── BaseHTTPClient(base_url, timeout, headers)
│       └── httpx.Client(...)
│           └── get_logger('core.client') → HTTPLogger → StreamHandler + FileHandler
│
├── ── ТЕСТ 1: crm_refactored_001 ──────────────────────────────
│   ├── authorization_service fixture → AuthorizationService(api_client)
│   ├── allure.dynamic.id / title / description
│   ├── allure.step 'POST /application.authorization'
│   │   └── authorization_service.authorize(ADMIN_AUTH_REQUEST)
│   │       ├── request.model_dump(exclude_none=True) → dict
│   │       ├── BaseHTTPClient.request('post', '/application.authorization', json=...)
│   │       │   ├── httpx.Client.request(...) → HTTP 200
│   │       │   └── HTTPLogger.log_http(response)
│   │       │       ├── _build_trace() → маскировка + форматирование
│   │       │       ├── logging.info(trace) → консоль + файл
│   │       │       └── allure.attach(trace, 'HTTP Trace')
│   │       └── return response
│   ├── validate_status_code(response, 200) → ✅
│   ├── validate_content_type(response, 'application/json') → ✅
│   ├── validate_response_time(response) → ✅
│   ├── validate_headers(response) → ✅
│   ├── validate_body_status(response, 'success') → ✅
│   ├── validate_model(response, AuthorizationResponse) → ✅
│   └── validate_schema(response, AuthorizationResponse.model_json_schema()) → ✅
│   pytest_runtest_logreport → _METRICS = {total:1, passed:1, ...}
│
├── ── ТЕСТ 2: crm_refactored_002 ──────────────────────────────
│   ├── authorization_service fixture → AuthorizationService(api_client)
│   ├── authorize(INVALID_CREDENTIALS_REQUEST) → HTTP 200, status='error'
│   ├── validate_status_code(response, 200) → ✅
│   ├── validate_body_status(response, 'error') → ✅
│   ├── validate_model(response, ErrorResponse) → ✅
│   └── validate_schema(response, ErrorResponse.model_json_schema()) → ✅
│   pytest_runtest_logreport → _METRICS = {total:2, passed:2, ...}
│
├── session_id fixture создаётся (session scope) — нужен для теста 3
│   ├── AuthorizationService(api_client)
│   ├── service.authorize(ADMIN_AUTH_REQUEST) → HTTP 200
│   └── yield response.json()['data']['session_id']
│
├── ── ТЕСТ 3: crm_refactored_003 ──────────────────────────────
│   ├── user_info_service fixture → UserInfoService(api_client)
│   ├── user_info_service.get_user_info(session_id)
│   │   └── BaseHTTPClient.request('get', '/application.user_info', headers={'authorization': sid})
│   │       ├── httpx.Client.request(...) → HTTP 200
│   │       └── HTTPLogger.log_http(response) → лог + Allure
│   ├── validate_status_code(response, 200) → ✅
│   ├── validate_body_status(response, 'success') → ✅
│   ├── validate_model(response, UserInfoResponse) → ✅
│   └── validate_schema(response, UserInfoResponse.model_json_schema()) → ✅
│   pytest_runtest_logreport → _METRICS = {total:3, passed:3, ...}
│
├── TEARDOWN session_id
│   └── service.sign_out(sid) → POST /application.sign_out
│
├── TEARDOWN api_client
│   └── client.close() → закрывает httpx.Client
│
└── pytest_sessionfinish()
    ├── _update_history_trend() → добавляет {total:3, passed:3, duration:...} в JSON
    ├── allure generate reports/allure-results -o reports/allure-report --clean
    ├── _copy_history_back() → копирует history для следующего запуска
    └── allure open reports/allure-report → открывает в браузере
```

---