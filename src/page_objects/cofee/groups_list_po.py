"""Groups tab ("My active groups" list). Locators confirmed live on
`builds/cofee-dev.apk` (versionCode 116).
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class GroupsListPage(BasePage):
    # --- Locators ---
    _tab_groups_acc = (AppiumBy.ACCESSIBILITY_ID, "Groups")
    _txt_my_active_groups_acc = (AppiumBy.ACCESSIBILITY_ID, "My active groups")

    # --- Public API ---
    def find_tab_groups(self):
        return self.find(*self._tab_groups_acc)

    def is_loaded(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._txt_my_active_groups_acc, timeout=timeout or self.timeout)

    def loc_card_group(self, group_name: str) -> tuple[str, str]:
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{group_name}")',
        )

    def is_group_card_visible(self, group_name: str, timeout: int | None = None) -> bool:
        return self.is_displayed(*self.loc_card_group(group_name), timeout=timeout or self.timeout)
