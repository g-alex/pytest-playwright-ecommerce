"""Thin API helpers used by tests (readable steps for reports)."""

from __future__ import annotations

import allure
import httpx


@allure.step("GET {path}")
def get_json(client: httpx.Client, path: str, **params) -> httpx.Response:
    return client.get(path, params=params or None)


@allure.step("POST {path}")
def post_json(client: httpx.Client, path: str, payload: dict) -> httpx.Response:
    return client.post(path, json=payload)


@allure.step("DELETE {path}")
def delete(client: httpx.Client, path: str) -> httpx.Response:
    return client.delete(path)


def _free_qty(product: dict) -> int:
    """Free stock for orders = stock - reserved (API field available_stock)."""
    if product.get("available_stock") is not None:
        return int(product["available_stock"])
    stock = int(product.get("stock") or 0)
    reserved = int(product.get("reserved_quantity") or 0)
    return max(0, stock - reserved)


def first_available_product(client: httpx.Client, min_qty: int = 1) -> dict:
    response = get_json(client, "/api/products", available="true", limit=100)
    response.raise_for_status()
    body = response.json()
    assert body.get("success") is True
    products = body.get("data") or []
    assert products, "Need at least one available product on the test stand"

    in_stock = [p for p in products if _free_qty(p) >= min_qty]
    assert in_stock, (
        "Need a product with available_stock >= "
        f"{min_qty} (stock minus reserved). "
        "Cancel old confirmed test orders or refresh local DB."
    )
    return in_stock[0]


def cancel_order(client: httpx.Client, order_id: int) -> None:
    """Release reservation / clean up after status tests."""
    client.put(f"/api/orders/{order_id}/status", json={"status": "cancelled"})
