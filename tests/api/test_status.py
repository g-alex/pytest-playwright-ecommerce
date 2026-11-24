"""Smoke: API is alive."""

import allure
import pytest


@allure.feature("API")
@allure.story("Health")
@allure.title("GET /api/status returns ok")
@pytest.mark.api
@pytest.mark.smoke
def test_api_status_ok(api_client):
    with allure.step("Request status endpoint"):
        response = api_client.get("/api/status")

    with allure.step("Assert healthy payload"):
        assert response.status_code == 200
        body = response.json()
        assert body.get("status") == "ok"
        assert "timestamp" in body

    assert False  # temporary: verify CI still runs UI after API fail
