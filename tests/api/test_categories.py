"""API: categories list and not-found."""

import allure
import pytest
from jsonschema import validate

from utils.schemas import CATEGORY_LIST_SCHEMA


@allure.feature("API")
@allure.story("Categories")
@allure.title("GET /api/categories returns list with contract")
@pytest.mark.api
@pytest.mark.smoke
def test_categories_list_ok(api_client):
    response = api_client.get("/api/categories")

    assert response.status_code == 200

    body = response.json()
    assert body.get("success") is True
    assert isinstance(body.get("data"), list)
    validate(instance=body, schema=CATEGORY_LIST_SCHEMA)


@pytest.mark.api
@pytest.mark.negative
def test_category_not_found(api_client):
    response = api_client.get("/api/categories/999999")

    assert response.status_code == 404

    body = response.json()
    assert body.get("success") is False
    assert "error" in body
