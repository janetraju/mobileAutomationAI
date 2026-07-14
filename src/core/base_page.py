"""Base page object — locators and element queries only."""

from __future__ import annotations

from typing import TYPE_CHECKING

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.core.settings import get_settings

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


class BasePage:
    """Base class for all page objects. Element lookup lives here only."""

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        settings = get_settings()
        self._platform = settings.platform
        self._wait_timeout = settings.explicit_wait_timeout
        self._poll = settings.poll_frequency

    @property
    def driver(self) -> WebDriver:
        return self._driver

    def _wait(self, timeout: float | None = None) -> WebDriverWait:
        return WebDriverWait(
            self._driver,
            timeout or self._wait_timeout,
            poll_frequency=self._poll,
        )

    def find_by_accessibility_id(self, accessibility_id: str) -> WebElement:
        """Find element by accessibility id (priority 1)."""
        return self._driver.find_element(AppiumBy.ACCESSIBILITY_ID, accessibility_id)

    def find_by_resource_id(self, resource_id: str) -> WebElement:
        """Find element by Android resource-id."""
        return self._driver.find_element(AppiumBy.ID, resource_id)

    def find_by_text(self, text: str, exact: bool = True) -> WebElement:
        """Find element by visible text."""
        if self._platform == "android":
            condition = f'new UiSelector().text{"Equals" if exact else ""}("{text}")'
            return self._driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, condition)
        predicate = f'label == "{text}"' if exact else f'label CONTAINS "{text}"'
        return self._driver.find_element(AppiumBy.IOS_PREDICATE, predicate)

    def find_by_uiautomator(self, selector: str) -> WebElement:
        """Find element by UiAutomator selector (Android)."""
        return self._driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)

    def find_by_ios_predicate(self, predicate: str) -> WebElement:
        """Find element by iOS predicate string."""
        return self._driver.find_element(AppiumBy.IOS_PREDICATE, predicate)

    def find_by_ios_class_chain(self, chain: str) -> WebElement:
        """Find element by iOS class chain."""
        return self._driver.find_element(AppiumBy.IOS_CLASS_CHAIN, chain)

    def find_by_xpath(self, xpath: str) -> WebElement:
        """Find element by XPath (last resort)."""
        return self._driver.find_element(AppiumBy.XPATH, xpath)

    def wait_for_visible(
        self, locator: tuple[str, str], timeout: float | None = None
    ) -> WebElement:
        """Wait until element matching locator tuple is visible."""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def is_displayed(self, locator: tuple[str, str]) -> bool:
        """Return True if element is displayed without raising."""
        try:
            return self._driver.find_element(*locator).is_displayed()
        except Exception:
            return False
