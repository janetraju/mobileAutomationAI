"""Create Group (Fixed fee) form + "Schedule payment collection" modal.
Locators confirmed live on `builds/cofee-dev.apk` (versionCode 116).

`input_group_name`, `input_amount`, and the per-member amount field have no
accessibility id of their own — same Flutter label/field split as
`login_po.py` / `add_member_po.py`. Located by class + on-screen order.
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class CreateGroupPage(BasePage):
    # --- Locators ---
    _txt_create_group_acc = (AppiumBy.ACCESSIBILITY_ID, "Create group")
    _input_group_name_uia = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)',
    )
    _input_amount_uia = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(1)',
    )
    _btn_fee_collection_day_acc = (AppiumBy.ACCESSIBILITY_ID, "Select payment collection day")
    _input_member_amount_uia = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(2)',
    )
    _btn_save_acc = (AppiumBy.ACCESSIBILITY_ID, "Save")

    # "Schedule payment collection" modal
    _btn_apply_acc = (AppiumBy.ACCESSIBILITY_ID, "Apply")

    # --- Public API ---
    def is_loaded(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._txt_create_group_acc, timeout=timeout or self.timeout)

    def find_input_group_name(self):
        return self.find(*self._input_group_name_uia)

    def find_input_amount(self):
        return self.find(*self._input_amount_uia)

    def find_btn_fee_collection_day(self):
        return self.find(*self._btn_fee_collection_day_acc)

    def loc_input_member_amount(self) -> tuple[str, str]:
        return self._input_member_amount_uia

    def find_input_member_amount(self):
        return self.find(*self._input_member_amount_uia)

    def find_btn_apply(self):
        return self.find(*self._btn_apply_acc)

    def find_btn_save(self):
        return self.find(*self._btn_save_acc)
