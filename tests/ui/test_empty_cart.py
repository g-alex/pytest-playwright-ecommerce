"""UI negative: empty cart shows popup."""

import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage


@pytest.mark.ui
@pytest.mark.negative
def test_empty_cart_shows_popup(page, clear_cart):
    catalog = CatalogPage(page)
    cart = CartPage(page)

    catalog.open()
    catalog.wait_products_loaded()

    # Same TEST_USER_ID as API clear_cart + seeded localStorage
    cart.open_from_header()
    cart.expect_empty_popup()
    cart.close_empty_popup()
