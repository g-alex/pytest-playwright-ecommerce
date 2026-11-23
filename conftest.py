"""Shared pytest fixtures: settings, API client, Playwright context seed."""

from __future__ import annotations

import json

import allure
import httpx
import pytest
from playwright.sync_api import BrowserContext

from utils.config import Settings, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings: Settings):
    client = httpx.Client(
        base_url=settings.base_url,
        timeout=settings.request_timeout,
        headers={"Accept": "application/json"},
    )
    yield client
    client.close()


@pytest.fixture
def test_user_id(settings: Settings) -> str:
    return settings.test_user_id


@pytest.fixture
def clear_cart(api_client: httpx.Client, test_user_id: str):
    """Ensure cart is empty before and after the test."""

    def _clear() -> None:
        with allure.step(f"Clear cart for {test_user_id}"):
            api_client.delete(f"/api/cart/clear/{test_user_id}")

    _clear()
    yield
    _clear()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, settings: Settings) -> dict:
    """Mini App viewport + stand base_url, so goto('/') works."""
    return {
        **browser_context_args,
        "base_url": settings.base_url,
        "viewport": {"width": 390, "height": 844},
        "locale": "ru-RU",
    }


@pytest.fixture
def context(context: BrowserContext, test_user_id: str) -> BrowserContext:
    """Plugin context + same user id as API clear_cart.

    Not autouse: API tests must not start a browser.
    """
    context.add_init_script(
        f"localStorage.setItem('browserTempUserId', {json.dumps(test_user_id)});"
    )
    return context
