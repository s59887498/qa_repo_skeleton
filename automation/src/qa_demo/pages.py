"""Page object owns locators and explicit waits; tests own behavior assertions."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CatalogPage:
    NAME = (By.CSS_SELECTOR, '[data-testid="item-name"]')
    CREATE = (By.CSS_SELECTOR, '[data-testid="create-item"]')
    RESULT = (By.CSS_SELECTOR, '[data-testid="result"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def open(self, base_url):
        self.driver.get(base_url + "/ui")

    def create(self, name):
        self.wait.until(EC.visibility_of_element_located(self.NAME)).send_keys(name)
        self.wait.until(EC.element_to_be_clickable(self.CREATE)).click()
        self.wait.until(EC.text_to_be_present_in_element(self.RESULT, "已建立"))
        return self.driver.find_element(*self.RESULT)
