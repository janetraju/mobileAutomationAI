"""Home screen locators for CoFee."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class HomePo(BasePage):
    """Locators for the logged-in home dashboard."""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        # --- Locators ---
        self._tab_home_acc = (AppiumBy.ACCESSIBILITY_ID, "Home")
        self._lnk_add_new_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Add New")',
        )
        self._section_groups_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Groups")',
        )
        self._tab_payments_acc = (AppiumBy.ACCESSIBILITY_ID, "Payments")
        self._tab_groups_acc = (AppiumBy.ACCESSIBILITY_ID, "Groups")
        # Live-confirmed: Dues section header merges title + CTA into one Semantics
        # node ("Dues\nView All"); Groups keeps a separate "View All" sibling.
        self._btn_dues_view_all_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Dues").descriptionContains("View All")',
        )

    def find_tab_home(self):
        """Bottom navigation Home tab."""
        return self._driver.find_element(*self._tab_home_acc)

    def find_add_new(self):
        """Add New group tile in the Groups carousel."""
        return self._driver.find_element(*self._lnk_add_new_uia)

    def loc_tab_home(self) -> tuple[str, str]:
        """Locator tuple for home tab wait."""
        return self._tab_home_acc

    def loc_add_new(self) -> tuple[str, str]:
        """Locator tuple for Add New tile."""
        return self._lnk_add_new_uia

    def loc_section_groups(self) -> tuple[str, str]:
        """Locator tuple for Groups section header."""
        return self._section_groups_uia

    def loc_tab_payments(self) -> tuple[str, str]:
        """Bottom navigation Payments tab."""
        return self._tab_payments_acc

    def loc_tab_groups(self) -> tuple[str, str]:
        """Bottom navigation Groups tab."""
        return self._tab_groups_acc

    def loc_btn_dues_view_all(self) -> tuple[str, str]:
        """Dues section header / View All CTA on the home dashboard."""
        return self._btn_dues_view_all_uia
