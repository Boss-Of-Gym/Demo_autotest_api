"""
Сохранение полученных order_id и address_id в файл и извлечение их при необходимости
"""

import pytest
import requests
from typing import Dict, Any

@pytest.fixture
def add_delete_after_cancel(address_store):
    """
    Удаление, добавление идентификаторов которые возвращаются сервером
    
    _cleanup_cancel - удаляет id при использовании order_id при отмене заказа
    _clenup_delete - удаляет id при использовании его в методе удаления
    _cleanup_add - добавляет id при получении его от сервера
    """
    def _cleanup_cancel(
            endpoint: str,
            params: Dict[str, Any],
            ):
        if endpoint.value == '/client/history/order' and params.get("action") == "cancel":
            address_store["pop_one"]("order_id")
    def _cleanup_delete(
            params: Dict[str, Any],
            expected_status_body: str
            ):
        if params.get("action") == "delete" and expected_status_body == "success":
            address_store["pop_one"]("address_id")
    def _cleanup_add(
            params: Dict[str, Any],
            response: requests.Response,
            expected_status_body: str
            ):
        if params.get("action") == "add" and expected_status_body == "success":
            address_store["add"]("address_id", response.json()["data"]["address_id"])
    def _cleanup_add_order(
            expected_status_body: str,
            endpoint: str,
            response: requests.Response
            ):
        if expected_status_body == "success" and endpoint.value == '/firm/order':
                    address_store["add"]("order_id", response.json()["data"]["id"])

    return {
        "cancel": _cleanup_cancel,
        "delete": _cleanup_delete,
        "add": _cleanup_add,
        "add_order": _cleanup_add_order
    }

@pytest.fixture
def prepare_body(address_store):
    def _prepare(
            endpoint: str,
            test_id: str,
            body: Dict[str, Any],
            params: Dict[str, Any],
            with_address: bool | None = None
            ) -> Dict[str, Any]:

        json = body.copy()
        
        if (
            endpoint.value == '/client/history/order'
            and test_id in (
                "shop_client_119",
                "shop_client_120",
                "shop_client_121",
                "shop_client_123",
                "shop_client_124",
                "shop_client_125",
                "shop_client_134",
                "shop_client_135"
                )
            ):
            json["order_id"] = address_store["get"]("order_id")
        
        if params.get("action") in ("update", "delete") and with_address:
            json["address_id"] = address_store["get"]("address_id")
        
        elif endpoint.value == "/firm/feedback" and params.get("action") == 'new':
            json["order_id"] = address_store["get"]("order_id")

        return json
    return _prepare