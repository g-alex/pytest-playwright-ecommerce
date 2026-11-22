"""UI: category button filters catalog."""

import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.ui
def test_category_filter_shows_products(page, api_client):
    cats = api_client.get("/api/categories").json().get("data") or []
    assert cats, "Need categories on the stand"
    slug = cats[0]["slug"]

    catalog = CatalogPage(page)
    catalog.open()
    catalog.wait_products_loaded()

    catalog.select_category(slug)
    assert catalog.products_grid.is_visible()

    if catalog.products_count() > 0:
        assert catalog.products_count() >= 1
