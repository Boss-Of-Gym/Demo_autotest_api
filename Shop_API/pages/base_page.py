import requests
import allure

class BasePage:
    """
    Базовый класс для всех вызовов API страниц
    Здесь будут храниться основные методы которые используются во всех страницах вызова
    """

    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers

    def post(
            self, endpoint: str, json: dict | None = None, data: dict | None = None, files: dict | None = None, timeout: int = 30
            ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        try:
            with allure.step(f"Выполнение POST запроса на {endpoint}"):
                response = requests.post(url=url, headers=self.headers, json=json, data=data, files=files, timeout=timeout)
                response.raise_for_status()
                return response
        except requests.RequestException as e:
            allure.attach(str(e), name="HTTP error", attachment_type=allure.attachment_type.TEXT)
            raise
    
    def get(self, endpoint: str, params: dict | None = None, timeout: int = 30) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        try:
            with allure.step(f"Выполнение GET запроса на {endpoint}"):
                response = requests.get(url=url, headers=self.headers, params=params, timeout=timeout)
                response.raise_for_status()
                return response
        except requests.RequestException as e:
            allure.attach(str(e), name="HTTP error", attachment_type=allure.attachment_type.TEXT)