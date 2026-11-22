"""Shared pytest fixtures: settings, API client, Playwright page."""

from __future__ import annotations

import allure
import httpx
import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

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
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Browser:
    launcher = getattr(playwright_instance, settings.browser)
    browser = launcher.launch(headless=settings.headless)
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser, settings: Settings, test_user_id: str) -> Page:
    """Fresh browser context; seed the same user id as API tests.

    Mini App browser mode reads localStorage.browserTempUserId.
    Seeding it keeps UI cart and API clear_cart on one user.
    """
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        locale="ru-RU",
        base_url=settings.base_url,
    )
    context.add_init_script(
        f"localStorage.setItem('browserTempUserId', {test_user_id!r});"
    )
    page = context.new_page()
    yield page
    context.close()
