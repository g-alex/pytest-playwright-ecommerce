"""UI: catalog search filters product cards."""

import pytest

from pages.catalog_page import CatalogPage
from utils.search_token import search_token


@pytest.mark.ui
def test_search_filters_products(page, api_client):
    seed = api_client.get("/api/products", params={"limit": 5, "lang": "ru"}).json().get("data") or []
    assert seed, "Need products on the stand"
    token = search_token(seed[0])

    api_check = api_client.get(
        "/api/products",
        params={"search": token, "lang": "ru", "limit": 20},
    )
    assert api_check.json().get("count", 0) >= 1, f"API search found nothing for {token!r}"

    catalog = CatalogPage(page)
    catalog.open()
    catalog.wait_products_loaded()
    before = catalog.products_count()

    catalog.search(token)

    assert catalog.products_count() >= 1
    assert catalog.products_count() <= before or before == 1
    assert token.lower() in catalog.first_product_title().lower()
