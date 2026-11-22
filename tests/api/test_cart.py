"""API: cart add → get → clear, plus validation negative."""

import allure
import pytest
from jsonschema import validate

from fixtures.api_helpers import first_available_product
from utils.schemas import CART_SCHEMA


@allure.feature("API")
@allure.story("Cart")
@allure.title("Cart lifecycle: add → get → clear")
@pytest.mark.api
@pytest.mark.smoke
def test_cart_add_get_clear(api_client, test_user_id, clear_cart):
    product = first_available_product(api_client)

    add_response = api_client.post(
        "/api/cart",
        json={
            "telegramUserId": test_user_id,
            "productId": product["id"],
            "quantity": 1,
        },
    )
    assert add_response.status_code == 200
    assert add_response.json().get("success") is True

    get_response = api_client.get(f"/api/cart/{test_user_id}")
    assert get_response.status_code == 200
    cart_body = get_response.json()
    validate(instance=cart_body, schema=CART_SCHEMA)
    assert cart_body["count"] >= 1
    assert any(item["product_id"] == product["id"] for item in cart_body["cart"])

    clear_response = api_client.delete(f"/api/cart/clear/{test_user_id}")
    assert clear_response.status_code == 200

    empty = api_client.get(f"/api/cart/{test_user_id}").json()
    assert empty["count"] == 0
    assert empty["cart"] == []


@pytest.mark.api
@pytest.mark.negative
def test_cart_add_without_product_id(api_client, test_user_id, clear_cart):
    response = api_client.post(
        "/api/cart",
        json={"telegramUserId": test_user_id, "quantity": 1},
    )

    assert response.status_code == 400
    body = response.json()
    assert body.get("success") is False
    assert "error" in body
