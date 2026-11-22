"""Page Object: product detail modal."""

from playwright.sync_api import Page, expect


class ProductModal:
    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator("#productModal")
        self.title = page.locator("#modalTitle")
        self.add_to_cart_btn = page.locator("#orderBtn")
        self.close_btn = page.locator("#closeModal")

    def wait_open(self) -> None:
        expect(self.root).to_be_visible(timeout=10_000)
        expect(self.title).not_to_be_empty()

    def add_to_cart(self) -> None:
        self.add_to_cart_btn.click()
