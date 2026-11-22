"""API: order from cart — negative empty, happy-path on local/staging only."""

import allure
import pytest

from fixtures.api_helpers import first_available_product


@pytest.mark.api
@pytest.mark.negative
def test_order_from_empty_cart(api_client, test_user_id, clear_cart):
    response = api_client.post(
        "/api/orders/cart",
        json={
            "telegramUserId": test_user_id,
            "first_name": "AQA",
            "last_name": "Test",
            "language_code": "ru",
        },
    )

    assert response.status_code == 400
    body = response.json()
    assert body.get("success") is False
    assert "error" in body


@allure.feature("API")
@allure.story("Orders")
@allure.title("Create order from cart and read it back")
@pytest.mark.api
@pytest.mark.smoke
def test_order_from_cart_happy_path(api_client, test_user_id, clear_cart):
    product = first_available_product(api_client)

    add = api_client.post(
        "/api/cart",
        json={
            "telegramUserId": test_user_id,
            "productId": product["id"],
            "quantity": 1,
        },
    )
    assert add.status_code == 200, add.text
    assert add.json().get("success") is True

    order = api_client.post(
        "/api/orders/cart",
        json={
            "telegramUserId": test_user_id,
            "telegram_username": "aqa_portfolio",
            "first_name": "AQA",
            "last_name": "Test",
            "language_code": "ru",
        },
    )
    assert order.status_code == 201, order.text
    order_body = order.json()
    assert order_body.get("success") is True
    assert "orderNumber" in order_body
    assert order_body.get("totalAmount", 0) > 0

    order_id = order_body["orderNumber"]
    get_order = api_client.get(f"/api/orders/{order_id}")
    assert get_order.status_code == 200
    saved = get_order.json()
    assert saved.get("success") is True
    assert saved["data"]["id"] == order_id
    assert saved["data"]["telegram_user_id"] == test_user_id
    assert len(saved["data"].get("items") or []) >= 1

    empty_cart = api_client.get(f"/api/cart/{test_user_id}").json()
    assert empty_cart["count"] == 0
