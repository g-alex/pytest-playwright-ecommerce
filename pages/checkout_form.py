"""Page Object: browser contact form shown on checkout outside Telegram."""

from playwright.sync_api import Page, expect


class CheckoutForm:
    def __init__(self, page: Page):
        self.page = page
        self.popup = page.locator(".browser-user-data-popup")
        self.name = page.locator("#userName")
        self.whatsapp = page.locator("#userWhatsapp")
        self.telegram = page.locator("#userTelegram")
        self.continue_btn = page.locator(".browser-user-data-btn-primary")
        self.success_popup = page.locator(".popup-order-number")

    def wait_open(self) -> None:
        expect(self.popup).to_be_visible(timeout=10_000)

    def fill_and_submit(self, name: str, telegram: str) -> None:
        self.name.fill(name)
        self.telegram.fill(telegram)
        self.continue_btn.click()

    def expect_order_created(self) -> None:
        expect(self.success_popup).to_be_visible(timeout=15_000)
