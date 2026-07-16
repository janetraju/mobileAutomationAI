"""Quick Collect payment-request flow locators for CoFee."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class QuickCollectPo(BasePage):
    """Locators for the Quick Collect member-select → amount → send flow."""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        # --- Locators ---
        self._opt_from_group_members_acc = (AppiumBy.ACCESSIBILITY_ID, "From Group Members")
        # Live-confirmed: button text is dynamic ("Add 1 member" / "Add N members"),
        # not the static "Add members" assumed during manual discovery. This flow
        # always selects exactly one member, so the singular form is the real value.
        self._btn_add_members_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Add 1 member")',
        )
        self._title_enter_amount_acc = (AppiumBy.ACCESSIBILITY_ID, "Enter amount")
        self._input_edittext_class = (AppiumBy.CLASS_NAME, "android.widget.EditText")
        self._btn_send_payment_link_acc = (AppiumBy.ACCESSIBILITY_ID, "Send Payment Link")
        self._msg_success_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Payment link sent successfully")',
        )
        self._btn_go_back_acc = (AppiumBy.ACCESSIBILITY_ID, "Go Back")

    def loc_from_group_members(self) -> tuple[str, str]:
        """'From Group Members' option in the member-select-strategy sheet."""
        return self._opt_from_group_members_acc

    def loc_member_checkbox(self, member_name: str) -> tuple[str, str]:
        """Member row in the group-members picker."""
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{member_name}")',
        )

    def loc_add_members(self) -> tuple[str, str]:
        """'Add 1 member' confirm button on the picker (dynamic count text)."""
        return self._btn_add_members_uia

    def loc_enter_amount_title(self) -> tuple[str, str]:
        """Amount-entry screen title."""
        return self._title_enter_amount_acc

    def loc_edittext_field(self) -> tuple[str, str]:
        """Generic EditText — used for both the amount and note fields."""
        return self._input_edittext_class

    def loc_send_payment_link(self) -> tuple[str, str]:
        """Submit button on the amount-entry screen."""
        return self._btn_send_payment_link_acc

    def loc_success_message(self) -> tuple[str, str]:
        """Success confirmation after sending a payment link."""
        return self._msg_success_uia

    def loc_go_back(self) -> tuple[str, str]:
        """'Go Back' button on the success screen."""
        return self._btn_go_back_acc
