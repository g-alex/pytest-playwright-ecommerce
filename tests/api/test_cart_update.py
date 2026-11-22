"""API: update quantity and remove cart item."""

import pytest

from fixtures.api_helpers import first_available_product


@pytest.mark.api
def test_cart_update_quantity(api_client, test_user_id, clear_cart):
    product = first_available_product(api_client, min_qty=2)

    add = api_client.post(
        "/api/cart",
        json={
            "telegramUserId": test_user_id,
            "productId": product["id"],
            "quantity": 1,
        },
    )
    assert add.status_code == 200

    cart = api_client.get(f"/api/cart/{test_user_id}").json()["cart"]
    item_id = cart[0]["id"]

    upd = api_client.put(f"/api/cart/{item_id}", json={"quantity": 2})
    assert upd.status_code == 200
    assert upd.json().get("success") is True

    after = api_client.get(f"/api/cart/{test_user_id}").json()["cart"]
    assert after[0]["quantity"] == 2


@pytest.mark.api
def test_cart_remove_item(api_client, test_user_id, clear_cart):
    product = first_available_product(api_client)

    api_client.post(
        "/api/cart",
        json={
            "telegramUserId": test_user_id,
            "productId": product["id"],
            "quantity": 1,
        },
    )
    cart = api_client.get(f"/api/cart/{test_user_id}").json()["cart"]
    item_id = cart[0]["id"]

    removed = api_client.delete(f"/api/cart/{item_id}")
    assert removed.status_code == 200
    assert removed.json().get("success") is True

    empty = api_client.get(f"/api/cart/{test_user_id}").json()
    assert empty["count"] == 0
