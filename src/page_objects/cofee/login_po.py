"""Login and onboarding screen locators for CoFee."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class LoginPo(BasePage):
    """Locators for phone + OTP login flow."""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        # --- Locators ---
        self._phone_title_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("phone number")',
        )
        self._otp_title_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("6-digit code")',
        )
        self._input_phone_class = (AppiumBy.CLASS_NAME, "android.widget.EditText")
        self._btn_next_acc = (AppiumBy.ACCESSIBILITY_ID, "Next")
        self._btn_continue_acc = (AppiumBy.ACCESSIBILITY_ID, "Continue")
        # descriptionContains("Individual") is case-insensitive on this UiAutomator2
        # build and false-matches the non-interactive "Welcome test individual!"
        # header (an android.view.View, appears earlier in the tree) before ever
        # reaching the real, clickable account row ("test individual\nIndividual",
        # an android.widget.ImageView). Constrain by class to target the row.
        self._account_individual_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiSelector()"
            '.className("android.widget.ImageView")'
            '.descriptionContains("Individual")',
        )
        self._tab_home_acc = (AppiumBy.ACCESSIBILITY_ID, "Home")
        self._account_welcome_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Welcome")',
        )
        self._btn_allow_text = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Allow")',
        )
        self._btn_debug_back_acc = (AppiumBy.ACCESSIBILITY_ID, "Back")
        # Google Play Services phone-number-hint bottom sheet — separate
        # system window (com.google.android.gms), pops up the instant the
        # phone EditText gains focus and fully covers the "Next" button.
        self._gms_phone_hint_cancel_id = (AppiumBy.ID, "com.google.android.gms:id/cancel")

    def find_phone_title(self):
        """Phone entry screen title."""
        return self._driver.find_element(*self._phone_title_uia)

    def find_otp_title(self):
        """OTP verification screen title."""
        return self._driver.find_element(*self._otp_title_uia)

    def find_phone_input(self):
        """Phone number text field."""
        return self._driver.find_element(*self._input_phone_class)

    def find_otp_input(self):
        """OTP code text field."""
        return self._driver.find_element(*self._input_phone_class)

    def find_btn_next(self):
        """Primary continue / submit button on phone or OTP."""
        return self._driver.find_element(*self._btn_next_acc)

    def find_btn_continue(self):
        """Continue button on account selection after OTP."""
        return self._driver.find_element(*self._btn_continue_acc)

    def find_account_individual(self):
        """Individual account row on account picker."""
        return self._driver.find_element(*self._account_individual_uia)

    def find_tab_home(self):
        """Bottom navigation Home tab."""
        return self._driver.find_element(*self._tab_home_acc)

    def find_permission_allow_button(self):
        """Android notification permission Allow button."""
        return self._driver.find_element(*self._btn_allow_text)

    def find_debug_back(self):
        """Back control on the dev network-logs overlay."""
        return self._driver.find_element(*self._btn_debug_back_acc)

    def find_gms_phone_hint_cancel(self):
        """Cancel control on the Google Play Services phone-number-hint sheet."""
        return self._driver.find_element(*self._gms_phone_hint_cancel_id)

    def loc_permission_allow(self) -> tuple[str, str]:
        """Locator tuple for permission Allow button."""
        return self._btn_allow_text

    def loc_phone_title(self) -> tuple[str, str]:
        """Locator tuple for phone title wait."""
        return self._phone_title_uia

    def loc_phone_input(self) -> tuple[str, str]:
        """Locator tuple for phone EditText."""
        return self._input_phone_class

    def loc_btn_next(self) -> tuple[str, str]:
        """Locator tuple for Next button."""
        return self._btn_next_acc

    def loc_otp_title(self) -> tuple[str, str]:
        """Locator tuple for OTP title wait."""
        return self._otp_title_uia

    def loc_account_welcome(self) -> tuple[str, str]:
        """Locator tuple for post-OTP account picker."""
        return self._account_welcome_uia

    def loc_btn_continue(self) -> tuple[str, str]:
        """Locator tuple for Continue on account picker."""
        return self._btn_continue_acc

    def loc_tab_home(self) -> tuple[str, str]:
        """Locator tuple for home tab wait."""
        return self._tab_home_acc

    def loc_gms_phone_hint_cancel(self) -> tuple[str, str]:
        """Locator tuple for the Google phone-number-hint sheet Cancel control."""
        return self._gms_phone_hint_cancel_id
