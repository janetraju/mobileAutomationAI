"""Home screen interactions for CoFee."""

from __future__ import annotations

from contextlib import suppress

from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.page_actions import PageActions
from src.page_objects.cofee.home_po import HomePo


class HomeActions(PageActions):
    """Business logic for the logged-in home dashboard."""

    def __init__(self, driver: WebDriver) -> None:
        self._home_po = HomePo(driver)
        super().__init__(driver, self._home_po)

    def is_home_screen_visible(self, timeout: float | None = None) -> bool:
        """Return True when home tab is visible."""
        try:
            self.wait_for_element_visible(self._home_po.loc_tab_home(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def ensure_home_tab_selected(self) -> None:
        """Tap Home tab to ensure dashboard is active."""
        home_tab = self.wait_for_element_visible(self._home_po.loc_tab_home(), timeout=10)
        self.tap(home_tab)

    def return_to_home_dashboard(self, max_back_presses: int = 4) -> bool:
        """Navigate to home when already logged in but on a nested screen."""
        if self.is_home_screen_visible(timeout=2):
            with suppress(Exception):
                self.ensure_home_tab_selected()
            return True
        for _ in range(max_back_presses):
            with suppress(Exception):
                self._driver.press_keycode(4)
            if self.is_home_screen_visible(timeout=2):
                with suppress(Exception):
                    self.ensure_home_tab_selected()
                return True
        with suppress(Exception):
            self.ensure_home_tab_selected()
        return self.is_home_screen_visible(timeout=3)

    def scroll_to_groups_section(self) -> None:
        """Scroll home until Add New is visible."""
        if self._page.is_displayed(self._home_po.loc_add_new()):
            return
        for _ in range(3):
            self.swipe_up(percent=0.55)
            if self._page.is_displayed(self._home_po.loc_add_new()):
                return
        # Final attempt via explicit wait (raises if still missing)
        self.wait_for_element_visible(self._home_po.loc_add_new(), timeout=5)

    def tap_add_new_group(self) -> None:
        """Open select-members sheet from home Groups carousel."""
        self.ensure_home_tab_selected()
        self.scroll_to_groups_section()
        add_new = self.wait_for_element_visible(self._home_po.loc_add_new(), timeout=10)
        self.tap(add_new)

    def tap_payments_tab(self) -> None:
        """Open the global 'All payments' screen via the bottom nav tab."""
        tab = self.wait_for_element_visible(self._home_po.loc_tab_payments(), timeout=10)
        self.tap(tab)

    def tap_groups_tab(self) -> None:
        """Open the Groups list via the bottom nav tab."""
        tab = self.wait_for_element_visible(self._home_po.loc_tab_groups(), timeout=10)
        self.tap(tab)

    def scroll_to_dues_section(self) -> None:
        """Scroll home until the Dues 'View All' header is visible."""
        if self._page.is_displayed(self._home_po.loc_btn_dues_view_all()):
            return
        for _ in range(3):
            self.swipe_up(percent=0.55)
            if self._page.is_displayed(self._home_po.loc_btn_dues_view_all()):
                return
        self.wait_for_element_visible(self._home_po.loc_btn_dues_view_all(), timeout=5)

    def tap_dues_view_all(self) -> None:
        """Open All payments (Pending) from the home Dues section View All CTA."""
        self.ensure_home_tab_selected()
        self.scroll_to_dues_section()
        view_all = self.wait_for_element_visible(self._home_po.loc_btn_dues_view_all(), timeout=10)
        self.tap(view_all)
