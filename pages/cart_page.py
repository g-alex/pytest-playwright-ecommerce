"""Page Object: cart screen and empty-cart popup."""

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_btn = page.locator("#cartBtn")
        self.empty_popup = page.locator(".empty-cart-content")
        self.empty_title = page.locator(".empty-cart-title")
        self.empty_ok_btn = page.locator(".empty-cart-btn")
        self.checkout_btn = page.locator("#checkoutBtn")
        self.cart_items = page.locator(".cart-item")

    def open_from_header(self) -> None:
        self.cart_btn.click()

    def expect_empty_popup(self) -> None:
        expect(self.empty_popup).to_be_visible(timeout=10_000)
        expect(self.empty_title).to_be_visible()

    def close_empty_popup(self) -> None:
        self.empty_ok_btn.click()
        expect(self.empty_popup).to_be_hidden(timeout=5_000)

    def expect_cart_open(self) -> None:
        expect(self.checkout_btn).to_be_visible(timeout=10_000)
        expect(self.cart_items.first).to_be_visible()

    def checkout(self) -> None:
        self.checkout_btn.click()
