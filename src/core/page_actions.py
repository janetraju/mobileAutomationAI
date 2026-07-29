"""Base page actions — interactions and mobile gestures."""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.core.base_page import BasePage
from src.core.settings import get_settings

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


class PageActions:
    """Base class for page actions. Business logic and gestures live here."""

    def __init__(self, driver: WebDriver, page: BasePage | None = None) -> None:
        self._driver = driver
        self._page = page or BasePage(driver)
        settings = get_settings()
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

    def tap(self, element: WebElement) -> None:
        """Tap an element."""
        element.click()

    def type_text(self, element: WebElement, text: str) -> None:
        """Type text into an element."""
        element.send_keys(text)

    def clear_and_type(self, element: WebElement, text: str) -> None:
        """Clear field then type text."""
        element.clear()
        element.send_keys(text)

    def long_press(self, element: WebElement, duration_ms: int = 1000) -> None:
        """Long-press an element."""
        self._driver.execute_script(
            "mobile: longClickGesture",
            {"elementId": element.id, "duration": duration_ms},
        )

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration_ms: int = 500,
    ) -> None:
        """Swipe between coordinates."""
        self._driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": start_x,
                "top": start_y,
                "width": 0,
                "height": 0,
                "direction": "up" if end_y < start_y else "down",
                "percent": 0.75,
            },
        )

    def swipe_up(self, percent: float = 0.75) -> None:
        """Swipe up on the screen."""
        size = self._driver.get_window_size()
        self._driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": size["width"] // 2,
                "top": size["height"] // 2,
                "width": 1,
                "height": 1,
                "direction": "up",
                "percent": percent,
            },
        )

    def scroll_to_element(self, element: WebElement) -> None:
        """Scroll until element is visible."""
        self._driver.execute_script("mobile: scroll", {"elementId": element.id})

    def scroll_to_text(self, text: str) -> None:
        """Scroll to text on screen (platform-specific)."""
        settings = get_settings()
        if settings.is_android:
            selector = "new UiScrollable(new UiSelector().scrollable(true))"
            selector += f'.scrollIntoView(new UiSelector().text("{text}"))'
            self._driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
        else:
            predicate = f'label CONTAINS "{text}"'
            self._driver.find_element(AppiumBy.IOS_PREDICATE, predicate)

    def wait_for_element_visible(
        self,
        locator: tuple[str, str],
        timeout: float | None = None,
    ) -> WebElement:
        """Wait until element is visible."""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_element_gone(
        self,
        locator: tuple[str, str],
        timeout: float | None = None,
    ) -> bool:
        """Wait until element is not present or invisible."""
        try:
            return self._wait(timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False

    def wait_for_loading_spinner_to_disappear(
        self,
        spinner_locator: tuple[str, str],
        timeout: float | None = None,
    ) -> None:
        """Wait for loading spinner to disappear."""
        self.wait_for_element_gone(spinner_locator, timeout=timeout or self._wait_timeout * 2)

    def hide_keyboard(self) -> None:
        """Dismiss the on-screen keyboard if visible.

        Guarded on `is_keyboard_shown()` — calling the driver's hideKeyboard
        command when no keyboard is actually up makes UiAutomator2 fall back
        to a BACK press, which can exit the app entirely on a screen with no
        back stack (e.g. the login phone-entry screen).
        """
        with suppress(Exception):
            if self._driver.is_keyboard_shown():
                self._driver.hide_keyboard()

    def get_text(self, element: WebElement) -> str:
        """Get element text."""
        return element.text or ""

    def get_attribute(self, element: WebElement, name: str) -> str:
        """Get element attribute value."""
        value = element.get_attribute(name)
        return value or ""

    def dismiss_system_alert(self, button_label: str = "Allow") -> None:
        """Dismiss a native system alert by button label."""
        settings = get_settings()
        if settings.is_ios:
            self._driver.execute_script(
                "mobile: alert",
                {"action": "accept", "buttonLabel": button_label},
            )
        else:
            with suppress(Exception):
                self._driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{button_label}")'
                ).click()

    def switch_to_webview(self, context_name: str | None = None) -> None:
        """Switch to WebView context."""
        contexts = self._driver.contexts
        webviews = [c for c in contexts if "WEBVIEW" in c.upper()]
        if not webviews:
            raise RuntimeError("No WebView context available")
        target = context_name if context_name in webviews else webviews[-1]
        self._driver.switch_to.context(target)

    def switch_to_native(self) -> None:
        """Switch to native app context."""
        contexts = self._driver.contexts
        native = [c for c in contexts if "NATIVE" in c.upper()]
        if native:
            self._driver.switch_to.context(native[0])
