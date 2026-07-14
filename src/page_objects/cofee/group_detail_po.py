"""Group detail screen locators for CoFee."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class GroupDetailPo(BasePage):
    """Locators for group overview after creation."""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        # --- Locators ---
        self._section_overview_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Overview")',
        )
        self._section_members_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Members")',
        )
        self._lbl_amount_collected_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Amount Collected")',
        )
        self._lbl_amount_due_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Amount Due")',
        )

    def loc_group_name(self, group_name: str) -> tuple[str, str]:
        """Header group name."""
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().description("{group_name}")',
        )

    def loc_active_member_count(self, count: int) -> tuple[str, str]:
        """Subtitle active member count."""
        suffix = "Member" if count == 1 else "Members"
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().description("{count} Active {suffix}")',
        )

    def loc_member_card(self, member_name: str) -> tuple[str, str]:
        """Member row containing name and fee details."""
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{member_name}")',
        )

    def loc_member_fee_amount(self, formatted_amount: str) -> tuple[str, str]:
        """Fee amount text inside member card (e.g. 5,000)."""
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{formatted_amount}")',
        )

    def loc_overview(self) -> tuple[str, str]:
        return self._section_overview_uia

    def loc_members_section(self) -> tuple[str, str]:
        return self._section_members_uia

    def loc_amount_collected(self) -> tuple[str, str]:
        return self._lbl_amount_collected_uia

    def loc_amount_due(self) -> tuple[str, str]:
        return self._lbl_amount_due_uia
