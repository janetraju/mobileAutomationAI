"""Home screen. Locators confirmed live on `builds/cofee-dev.apk` (versionCode 116)."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class HomePage(BasePage):
    # --- Locators ---
    # "Overview" merges with an adjacent promo-banner Semantics node on some
    # Home states ("Overview\nInstant payment links\n...") -- "Add New" is
    # the stable, always-standalone content-desc confirmed live instead.
    _btn_add_new_acc = (AppiumBy.ACCESSIBILITY_ID, "Add New")

    # --- Public API ---
    def is_loaded(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._btn_add_new_acc, timeout=timeout or self.timeout)

    def find_btn_add_new(self):
        return self.find(*self._btn_add_new_acc)
