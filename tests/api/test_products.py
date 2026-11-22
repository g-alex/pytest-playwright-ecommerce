"""API: products list, one product, not-found."""

import allure
import pytest
from jsonschema import validate

from utils.schemas import PRODUCT_LIST_SCHEMA


@allure.feature("API")
@allure.story("Products")
@allure.title("GET /api/products returns list with contract")
@pytest.mark.api
@pytest.mark.smoke
def test_products_list_ok(api_client):
    response = api_client.get("/api/products", params={"limit": 10})

    assert response.status_code == 200

    body = response.json()
    assert body.get("success") is True
    assert isinstance(body.get("data"), list)
    assert body.get("count") == len(body["data"])
    validate(instance=body, schema=PRODUCT_LIST_SCHEMA)


@pytest.mark.api
def test_product_by_id_ok(api_client):
    list_response = api_client.get("/api/products", params={"limit": 1})
    assert list_response.status_code == 200
    products = list_response.json().get("data") or []
    assert products, "Need at least one product on the test stand"

    product_id = products[0]["id"]
    response = api_client.get(f"/api/products/{product_id}")

    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    assert body["data"]["id"] == product_id
    assert "title" in body["data"]
    assert "price" in body["data"]


@pytest.mark.api
@pytest.mark.negative
def test_product_not_found(api_client):
    response = api_client.get("/api/products/999999")

    assert response.status_code == 404
    body = response.json()
    assert body.get("success") is False
    assert "error" in body
