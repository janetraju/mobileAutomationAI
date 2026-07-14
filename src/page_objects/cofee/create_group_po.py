"""Create group flow locators for CoFee."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class CreateGroupPo(BasePage):
    """Locators for select members through group save."""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        # --- Locators ---
        self._title_select_members_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Select members")',
        )
        self._opt_manually_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Manually")',
        )
        self._title_add_member_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Add member")',
        )
        self._label_name_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Name")',
        )
        self._label_mobile_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Mobile Number")',
        )
        self._input_fields_class = (AppiumBy.CLASS_NAME, "android.widget.EditText")
        self._btn_add_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Add")',
        )
        self._title_create_group_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Create group")',
        )
        self._fee_collection_day_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Select payment collection day")',
        )
        self._fee_collection_day_filled_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Last day of the month")',
        )
        self._title_schedule_payment_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Schedule payment collection")',
        )
        self._opt_last_day_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Last day of the month")',
        )
        self._btn_apply_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Apply")',
        )
        self._btn_cancel_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Cancel")',
        )
        self._btn_save_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Save")',
        )
        self._btn_save_enabled_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Save").enabled(true).clickable(true)',
        )
        self._title_share_promo_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Get paid faster with CoFee")',
        )
        self._btn_share_later_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("I\'ll share later")',
        )

    def find_manually_option(self):
        """Manually option on select members sheet."""
        return self._driver.find_element(*self._opt_manually_uia)

    def find_add_member_inputs(self) -> list:
        """Name and mobile EditText fields on add member screen."""
        return self._driver.find_elements(*self._input_fields_class)

    def find_create_group_inputs(self) -> list:
        """Group name and amount EditText fields."""
        return self._driver.find_elements(*self._input_fields_class)

    def find_btn_add(self):
        """Add button on add member screen."""
        return self._driver.find_element(*self._btn_add_uia)

    def find_fee_collection_day(self):
        """Fee Collection Day picker field on create group form."""
        if self.is_displayed(self._fee_collection_day_uia):
            return self._driver.find_element(*self._fee_collection_day_uia)
        return self._driver.find_element(*self._fee_collection_day_filled_uia)

    def loc_fee_collection_day_field(self) -> tuple[str, str]:
        """Locator for empty or filled fee collection day field."""
        if self.is_displayed(self._fee_collection_day_uia):
            return self._fee_collection_day_uia
        return self._fee_collection_day_filled_uia

    def loc_fee_collection_day_last_of_month(self) -> tuple[str, str]:
        """Locator when fee collection day is set to last day of month."""
        return self._fee_collection_day_filled_uia

    def find_last_day_of_month(self):
        """Last day of the month radio on schedule modal."""
        return self._driver.find_element(*self._opt_last_day_uia)

    def find_btn_apply(self):
        """Apply button on schedule payment modal."""
        return self._driver.find_element(*self._btn_apply_uia)

    def find_btn_cancel(self):
        """Cancel button on schedule payment modal."""
        return self._driver.find_element(*self._btn_cancel_uia)

    def loc_btn_cancel(self) -> tuple[str, str]:
        return self._btn_cancel_uia

    def find_btn_save(self):
        """Save button on create group form."""
        return self._driver.find_element(*self._btn_save_uia)

    def loc_btn_save(self) -> tuple[str, str]:
        """Locator for Save button (any state)."""
        return self._btn_save_uia

    def loc_btn_save_enabled(self) -> tuple[str, str]:
        """Locator for enabled, clickable Save button."""
        return self._btn_save_enabled_uia

    def find_share_later(self):
        """I'll share later on post-save promo modal."""
        return self._driver.find_element(*self._btn_share_later_uia)

    def loc_select_members_title(self) -> tuple[str, str]:
        return self._title_select_members_uia

    def loc_manually(self) -> tuple[str, str]:
        return self._opt_manually_uia

    def loc_add_member_title(self) -> tuple[str, str]:
        return self._title_add_member_uia

    def loc_create_group_title(self) -> tuple[str, str]:
        return self._title_create_group_uia

    def loc_schedule_payment_title(self) -> tuple[str, str]:
        return self._title_schedule_payment_uia

    def loc_share_promo_title(self) -> tuple[str, str]:
        return self._title_share_promo_uia

    def loc_share_later(self) -> tuple[str, str]:
        return self._btn_share_later_uia

    def loc_group_name_header(self, group_name: str) -> tuple[str, str]:
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().description("{group_name}")',
        )
