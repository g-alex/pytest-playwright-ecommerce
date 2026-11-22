"""API: product search and category filter."""

import pytest

from utils.search_token import search_token


@pytest.mark.api
def test_products_search_returns_matches(api_client):
    seed = api_client.get("/api/products", params={"limit": 5, "lang": "ru"})
    assert seed.status_code == 200
    products = seed.json().get("data") or []
    assert products, "Need products on the stand"

    token = search_token(products[0])
    response = api_client.get(
        "/api/products",
        params={"search": token, "lang": "ru", "limit": 20},
    )

    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    assert body.get("count", 0) >= 1
    assert any(
        token.lower() in (p.get("title_ru") or p.get("title") or "").lower()
        for p in body["data"]
    )


@pytest.mark.api
def test_products_filter_by_category_slug(api_client):
    cats = api_client.get("/api/categories")
    assert cats.status_code == 200
    categories = cats.json().get("data") or []
    assert categories, "Need categories on the stand"

    slug = categories[0]["slug"]
    response = api_client.get("/api/products", params={"category": slug, "limit": 20})

    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    for product in body.get("data") or []:
        assert product.get("category_slug") == slug
