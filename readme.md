# Automation QA Portfolio – Python, Pytest, Requests

* **Автор:** Дмитрий

* **Роль:** Automation QA Engineer

* **Контакты:** <naydanov.dmitriy@gmail.com> • <@DatorDeus>

---

## Краткое описание

Этот репозиторий демонстрирует практический подход к автоматизации тестирования API с использованием **Python**, **Requests** и **Pytest**. Цель — показать структуру тестов, применяемые паттерны (Page Object, API-клиенты), удобную генерацию отчётов с помощью **Allure CLI** и готовность репозитория к интеграции в CI.

---

## Технологический стек

* Язык: **Python 3.13.5**
* Тестовый раннер: **Pytest**
* API: **requests** (легковесные клиентские обёртки)
* Отчёты: **Allure CLI**
* Форматирование и статический анализ: **flake8**

---

## Структура проекта

```
Shop_API/
|__configs/
| |__config.py
|
|__fixtures/
| |__api.py
|
|__pages/
| |__base_page.py
| |__firm_page.py
|
|__tests/
| |__api/
| | |__test_firm.py
| |__files/
| | |__example_image.img
|
|__utils/
| |__api_auth.py
| |__endpoints.py
| |__request_logger.py
| |__signature.py
| |__token_access.txt
|
|__.env.v29
|__.gitlab-ci
|__conftest.py
|__pytest.ini
|__requirement.txt
.gitignore
readme.md
```

Ключевые элементы:

* **tests/** — реальные тесты использующиеся в тестировании (api).
* **pages/** — реализация Page Object Model.
* **utils/** — авторизация, логирование, эндпоинты, генерация подписи для заголовков запросов.
* **conftest.py** — фикстуры Pytest (Allure CLI, авторизация, добавление заголовков, метрики).
* **configs/** — конфиги для секретов и заголовков.

---

## Быстрый старт (локально)

> Предполагается, что Python и Requests уже установлены.

1. **Создать виртуальное окружение и установить зависимости**

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
requests install
```

2. **Запуск тестов**

```bash
# Запуск всех тестов
pytest -vv

# Запуск тестов (пример)
pytest tests/api
```

3. **Генерация отчёта Allure**

```bash
pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

---

## Рекомендации по написанию тестов

* Единый уровень абстракции: тесты читаемы и кратки, логика — в Page Object.
* Избегать жёсткой привязки к данным — использовать фикстуры и тест-даты.
* Использовать параметризацию Pytest для покрытий сценариев.
* Включать assertions с понятными сообщениями.
* Покрывать happy path и минимум негативных сценариев. 

---

## Пример фикстуры (conftest.py)

```python
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
```

---

## CI / дальнейшие шаги

На этапе разработки: планируется добавить GitLab CI для:

* запуска тестов при PR;
* публикации Allure-отчётов;
* проверки статики/линтинга.

Также рассматривается контейнеризация окружения (Docker) для стабилизации сред запуска.

---

## Best practices и примечания

* Храните секреты и конфигурации вне репозитория (env-файлы, секрет-менеджеры).
* Логи и артефакты тестов следует хранить в `reports/` и при необходимости выгружать в CI.
* Поддерживайте чистую и понятную документацию: README должен покрывать сценарии запуска и требования.

---