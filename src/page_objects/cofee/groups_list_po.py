"""Groups list (My active groups) locators for CoFee."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class GroupsListPo(BasePage):
    """Locators for the My active groups list screen."""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        # --- Locators ---
        # Live-confirmed via Home → Groups "View All" (and bottom nav Groups tab).
        self._txt_my_active_groups_acc = (AppiumBy.ACCESSIBILITY_ID, "My active groups")

    def loc_txt_my_active_groups(self) -> tuple[str, str]:
        """Screen title for the active groups list."""
        return self._txt_my_active_groups_acc
