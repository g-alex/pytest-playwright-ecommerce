"""UI: catalog opens and shows product cards."""

import allure
import pytest

from pages.catalog_page import CatalogPage


@allure.feature("UI")
@allure.story("Catalog")
@allure.title("Catalog page shows at least one product card")
@pytest.mark.ui
@pytest.mark.smoke
def test_catalog_shows_products(page):
    catalog = CatalogPage(page)

    with allure.step("Open catalog"):
        catalog.open()
        catalog.wait_products_loaded()

    with allure.step("Assert products are visible"):
        assert catalog.products_count() >= 1

    assert False  # temporary: verify ui-failure-screenshots artifact
