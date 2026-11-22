"""Page Object: shop catalog (Mini App main screen)."""

from playwright.sync_api import Page, expect


class CatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.products_grid = page.locator("#productsGrid")
        self.product_cards = page.locator(".product-card")
        self.cart_btn = page.locator("#cartBtn")
        self.cart_badge = page.locator("#cartBadge")
        self.search_input = page.locator("#searchInput")
        self.empty_state = page.locator(".empty-state")

    def open(self) -> None:
        self.page.goto("/")
        self.products_grid.wait_for(state="visible")

    def wait_products_loaded(self) -> None:
        expect(self.product_cards.first).to_be_visible(timeout=15_000)

    def wait_grid_settled(self) -> None:
        """Cards or empty-state after filter/search (anti-flaky)."""
        expect(self.product_cards.first.or_(self.empty_state)).to_be_visible(timeout=15_000)

    def products_count(self) -> int:
        return self.product_cards.count()

    def open_first_product(self) -> None:
        self.product_cards.first.click()

    def open_first_in_stock_product(self) -> None:
        """Skip cards marked out-of-stock (available_stock may be 0)."""
        card = self.product_cards.filter(
            has_not=self.page.locator(".out-of-stock")
        ).first
        expect(card).to_be_visible(timeout=15_000)
        card.click()

    def search(self, query: str) -> None:
        with self.page.expect_response(
            lambda r: "/api/products" in r.url and "search=" in r.url and r.ok,
            timeout=15_000,
        ):
            self.search_input.fill(query)
        self.wait_grid_settled()

    def select_category(self, slug: str) -> None:
        btn = self.page.locator(f'.category-btn[data-category="{slug}"]')
        with self.page.expect_response(
            lambda r: "/api/products" in r.url and "category=" in r.url and r.ok,
            timeout=15_000,
        ):
            btn.click()
        self.wait_grid_settled()

    def first_product_title(self) -> str:
        return self.product_cards.first.locator(".product-title").inner_text().strip()
