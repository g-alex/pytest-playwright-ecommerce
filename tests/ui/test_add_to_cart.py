"""UI: open product → add to cart → badge updates."""

import allure
import pytest
from playwright.sync_api import expect

from pages.catalog_page import CatalogPage
from pages.product_modal import ProductModal


@allure.feature("UI")
@allure.story("Cart")
@allure.title("Add to cart updates header badge")
@pytest.mark.ui
@pytest.mark.smoke
def test_add_product_to_cart_updates_badge(page, test_user_id, clear_cart):
    # page fixture seeds localStorage.browserTempUserId = TEST_USER_ID
    # clear_cart clears the same user on API side
    catalog = CatalogPage(page)
    modal = ProductModal(page)

    catalog.open()
    catalog.wait_products_loaded()

    badge_before = catalog.cart_badge.inner_text().strip()
    before = int(badge_before) if badge_before.isdigit() else 0

    catalog.open_first_in_stock_product()
    modal.wait_open()
    modal.add_to_cart()

    expect(catalog.cart_badge).not_to_have_text(str(before), timeout=10_000)
    badge_after = int(catalog.cart_badge.inner_text().strip())
    assert badge_after >= before + 1
