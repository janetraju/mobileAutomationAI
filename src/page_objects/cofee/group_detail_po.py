"""Group detail screen, reached after saving a new/edited group. Locators
confirmed live on `builds/cofee-dev.apk` (versionCode 116).

The post-save "Get paid faster with CoFee!" share interstitial only appeared
on some runs (backend-latency dependent, not deterministic) — treated as
optional/best-effort here, not a required step.
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class GroupDetailPage(BasePage):
    # --- Locators ---
    _txt_overview_acc = (AppiumBy.ACCESSIBILITY_ID, "Overview")
    _btn_share_later_acc = (AppiumBy.ACCESSIBILITY_ID, "I'll share later")

    # --- Public API ---
    def loc_group_title(self, group_name: str) -> tuple[str, str]:
        return (AppiumBy.ACCESSIBILITY_ID, group_name)

    def is_loaded(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._txt_overview_acc, timeout=timeout or self.timeout)

    def is_share_later_visible(self, timeout: int = 3) -> bool:
        return self.is_displayed(*self._btn_share_later_acc, timeout=timeout)

    def find_btn_share_later(self):
        return self.find(*self._btn_share_later_acc)
