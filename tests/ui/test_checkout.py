"""UI: add to cart → checkout → order success (browser mode)."""

import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_form import CheckoutForm
from pages.product_modal import ProductModal
from utils.test_user import telegram_username_for


@allure.feature("UI")
@allure.story("Checkout")
@allure.title("Browser checkout creates an order")
@pytest.mark.ui
@pytest.mark.smoke
def test_checkout_creates_order(page, test_user_id, clear_cart):
    catalog = CatalogPage(page)
    modal = ProductModal(page)
    cart = CartPage(page)
    form = CheckoutForm(page)
    telegram = telegram_username_for(test_user_id)

    catalog.open()
    catalog.wait_products_loaded()
    catalog.open_first_in_stock_product()
    modal.wait_open()
    modal.add_to_cart()
    expect(catalog.cart_badge).not_to_have_text("0", timeout=10_000)

    catalog.cart_btn.click()
    cart.expect_cart_open()
    cart.checkout()

    form.wait_open()
    # Same username → form builds the same web_tg_* id as seeded localStorage
    form.fill_and_submit(name="AQA Tester", telegram=telegram)
    form.expect_order_created()
