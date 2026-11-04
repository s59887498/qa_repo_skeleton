"""Playwright page object owns locators/actions; tests own observable assertions."""

from playwright.sync_api import Locator, Page


class CatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.name = page.get_by_label("項目名稱", exact=True)
        self.create_button = page.get_by_role("button", name="建立項目", exact=True)
        self.result = page.get_by_role("status")

    def open(self, base_url):
        self.page.goto(base_url + "/ui")

    def create(self, name: str) -> Locator:
        self.name.fill(name)
        self.create_button.click()
        return self.result
