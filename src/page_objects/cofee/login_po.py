"""Login (mobile + OTP). Locators confirmed live on `builds/cofee-dev.apk`
(versionCode 116) via a real Appium session against `emulator-5554`.

Flutter app: every static label exposes a Semantics content-desc equal to
its visible text, but the phone-number and OTP `EditText` inputs expose no
content-desc of their own (Flutter renders the label as a *sibling*
Semantics node, not an accessible-name on the field). There's exactly one
input on each of these two screens, so `ANDROID_UIAUTOMATOR` by class +
instance is the highest-priority strategy actually available (accessibility
id doesn't exist on these fields) — not XPath, and not a guess.
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class LoginPage(BasePage):
    # --- Locators ---
    _txt_phone_prompt_acc = (AppiumBy.ACCESSIBILITY_ID, "What's your phone number?")
    _input_mobile_uia = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)',
    )
    _btn_next_acc = (AppiumBy.ACCESSIBILITY_ID, "Next")

    _txt_otp_prompt_acc = (AppiumBy.ACCESSIBILITY_ID, "We've sent a 6-digit code to")
    _input_otp_uia = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)',
    )

    # "Overview" merges with an adjacent promo-banner Semantics node on some
    # Home states ("Overview\nInstant payment links\n...") -- "Add New" is
    # the stable, always-standalone content-desc confirmed live instead.
    _txt_home_loaded_acc = (AppiumBy.ACCESSIBILITY_ID, "Add New")

    # --- Public API ---
    def find_txt_phone_prompt(self):
        return self.find(*self._txt_phone_prompt_acc)

    def loc_input_mobile(self):
        return self._input_mobile_uia

    def find_input_mobile(self):
        return self.find(*self._input_mobile_uia)

    def find_btn_next(self):
        return self.find(*self._btn_next_acc)

    def is_otp_prompt_visible(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._txt_otp_prompt_acc, timeout=timeout or self.timeout)

    def find_input_otp(self):
        return self.find(*self._input_otp_uia)

    def is_home_visible(self, timeout: int | None = None) -> bool:
        return self.is_displayed(*self._txt_home_loaded_acc, timeout=timeout or self.timeout)
