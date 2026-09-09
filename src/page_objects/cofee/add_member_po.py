""" "Select members" modal + "Add member" screen. Locators confirmed live on
`builds/cofee-dev.apk` (versionCode 116). `input_name` / `input_mobile` have
no accessibility id of their own (Flutter renders the field label as a
sibling Semantics node) — located by class + on-screen order instead, which
is the highest-priority strategy actually available for these two fields.
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class AddMemberPage(BasePage):
    # --- Locators ---
    _txt_select_members_acc = (AppiumBy.ACCESSIBILITY_ID, "Select members")
    _btn_manually_acc = (AppiumBy.ACCESSIBILITY_ID, "Manually")
    _btn_from_contacts_acc = (AppiumBy.ACCESSIBILITY_ID, "From Contacts")

    _txt_add_member_acc = (AppiumBy.ACCESSIBILITY_ID, "Add member")
    _input_name_uia = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)',
    )
    _input_mobile_uia = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(1)',
    )
    _btn_add_acc = (AppiumBy.ACCESSIBILITY_ID, "Add")

    # --- Public API ---
    def is_select_members_modal_visible(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._txt_select_members_acc, timeout=timeout or self.timeout)

    def find_btn_manually(self):
        return self.find(*self._btn_manually_acc)

    def find_btn_from_contacts(self):
        return self.find(*self._btn_from_contacts_acc)

    def is_add_member_screen_visible(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._txt_add_member_acc, timeout=timeout or self.timeout)

    def find_input_name(self):
        return self.find(*self._input_name_uia)

    def find_input_mobile(self):
        return self.find(*self._input_mobile_uia)

    def find_btn_add(self):
        return self.find(*self._btn_add_acc)
