"""Layer 1 base class: `core` → no imports of page_objects/page_actions/steps
or any app-specific code (one-way dependency rule).

Page objects extend `BasePage` and expose only locators + `find_*()` /
`loc_*()` accessors — no business logic, gestures, or assertions here either
(those live in `page_actions` / `tests`).
"""

from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from src.core.settings import Settings, get_settings


class BasePage:
    """Shared wait/locator plumbing. Concrete `*_po.py` files subclass this
    and add locators only, under a `# --- Locators ---` marker."""

    def __init__(self, driver, settings: Settings | None = None):
        self.driver = driver
        self.settings = settings or get_settings()
        self._platform = "android" if self.settings.is_android else "ios"
        self.timeout = self.settings.explicit_wait_timeout

    # --- Waits ---

    def _wait(self, timeout: int | None = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    def wait_present(self, by: str, value: str, timeout: int | None = None):
        return self._wait(timeout).until(lambda d: d.find_element(by, value))

    def wait_visible(self, by: str, value: str, timeout: int | None = None):
        return self._wait(timeout).until(
            lambda d: (el := d.find_element(by, value)) and el.is_displayed() and el
        )

    def wait_clickable(self, by: str, value: str, timeout: int | None = None):
        def _clickable(d):
            el = d.find_element(by, value)
            return el if el.is_displayed() and el.is_enabled() else False

        return self._wait(timeout).until(_clickable)

    # --- Finders (used by page-object find_*() accessors) ---

    def find(self, by: str, value: str, timeout: int | None = None):
        return self.wait_visible(by, value, timeout)

    def find_all(self, by: str, value: str, timeout: int | None = None):
        self._wait(timeout).until(lambda d: d.find_elements(by, value))
        return self.driver.find_elements(by, value)

    def is_displayed(self, by: str, value: str, timeout: int = 3) -> bool:
        try:
            self.wait_visible(by, value, timeout)
            return True
        except TimeoutException:
            return False

    def resolve_locator(self, *candidates: tuple[str, str]) -> tuple[str, str]:
        """Given candidate `(by, value)` tuples in the repo's locator-priority
        order (accessibility id → resource-id/predicate → text → xpath), return
        the first one actually present on screen. Lets a page object offer
        several strategies for one element without `core` knowing anything
        app-specific about which one wins."""
        last_exc: Exception | None = None
        for by, value in candidates:
            try:
                self.wait_present(by, value, timeout=2)
                return by, value
            except TimeoutException as exc:
                last_exc = exc
        raise NoSuchElementException(
            f"None of the candidate locators matched on screen: {list(candidates)}"
        ) from last_exc
