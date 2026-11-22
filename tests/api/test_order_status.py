"""API: change order status after create."""

import pytest

from fixtures.api_helpers import cancel_order, first_available_product


def _create_order(api_client, test_user_id: str) -> int:
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

    order = api_client.post(
        "/api/orders/cart",
        json={
            "telegramUserId": test_user_id,
            "first_name": "AQA",
            "last_name": "Status",
            "language_code": "ru",
        },
    )
    assert order.status_code == 201, order.text
    return order.json()["orderNumber"]


@pytest.mark.api
def test_order_status_pending_to_confirmed(api_client, test_user_id, clear_cart):
    order_id = _create_order(api_client, test_user_id)

    response = api_client.put(
        f"/api/orders/{order_id}/status",
        json={"status": "confirmed"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body.get("success") is True
    assert body["data"]["status"] == "confirmed"

    # Release reserved stock so later runs stay green
    cancel_order(api_client, order_id)


@pytest.mark.api
@pytest.mark.negative
def test_order_status_invalid_value(api_client, test_user_id, clear_cart):
    order_id = _create_order(api_client, test_user_id)

    response = api_client.put(
        f"/api/orders/{order_id}/status",
        json={"status": "shipped"},
    )
    assert response.status_code == 400
    assert response.json().get("success") is False

    cancel_order(api_client, order_id)
