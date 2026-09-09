"""Layer 2 base class: `page_actions` may call `page_objects` + `core`, but
must never call `driver.find_element` directly — elements always come from a
page object's `find_*()` accessor. This base only holds gesture/interaction
helpers that operate on elements already found, plus wait re-checks after
navigation (no stale `WebElement` caching across screens).
"""

from __future__ import annotations

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from src.core.base_page import BasePage


class PageActions(BasePage):
    """Shared interaction helpers. Concrete `*_actions.py` files subclass
    this, hold a matching page object instance, and orchestrate calls to its
    `find_*()` accessors — never their own `driver.find_element`."""

    # --- Basic interactions on an already-found element ---

    def tap(self, element) -> None:
        element.click()

    def type_text(self, element, text: str, clear_first: bool = True) -> None:
        # Flutter's semantics-based text fields don't reliably accept
        # send_keys() until explicitly focused with a tap first (confirmed
        # live: send_keys() alone silently no-ops on this app).
        element.click()
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, element) -> str:
        return element.text

    def hide_keyboard(self) -> None:
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def wait_until_gone(self, by: str, value: str, timeout: int | None = None) -> bool:
        try:
            self._wait(timeout).until_not(lambda d: d.find_element(by, value).is_displayed())
            return True
        except (TimeoutException, StaleElementReferenceException):
            return True

    # --- Gestures (driver-level, not element lookups — allowed here) ---

    def swipe(
        self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 400
    ) -> None:
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=finger)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.release()
        actions.perform()

    def swipe_up(self, fraction: float = 0.6) -> None:
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        self.swipe(w // 2, int(h * fraction), w // 2, int(h * (1 - fraction)))

    def swipe_down(self, fraction: float = 0.6) -> None:
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        self.swipe(w // 2, int(h * (1 - fraction)), w // 2, int(h * fraction))

    def scroll_until_visible(
        self, by: str, value: str, max_swipes: int = 6, timeout_per_check: int = 2
    ):
        for _ in range(max_swipes):
            if self.is_displayed(by, value, timeout=timeout_per_check):
                return self.driver.find_element(by, value)
            self.swipe_up()
        raise TimeoutException(f"Element not found after {max_swipes} swipes: {by}={value}")
