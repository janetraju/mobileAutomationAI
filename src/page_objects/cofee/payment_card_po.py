"""Payment card / kebab-menu locators shared across CoFee's three payment-list
screens (per-member history, "Group payments", and the global "All payments"
tab) — all three use the same underlying widget, confirmed live.
"""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from src.core.base_page import BasePage


class PaymentCardPo(BasePage):
    """Locators for a payment card's kebab menu and the enable-partial-payment dialog."""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        # --- Locators ---
        self._btn_view_payments_acc = (AppiumBy.ACCESSIBILITY_ID, "View payments")
        self._title_group_payments_acc = (AppiumBy.ACCESSIBILITY_ID, "Group payments")
        self._title_all_payments_uia = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("All payments")',
        )
        self._btn_mark_as_paid_acc = (AppiumBy.ACCESSIBILITY_ID, "Mark as paid")
        self._btn_share_payment_link_acc = (AppiumBy.ACCESSIBILITY_ID, "Share payment link")
        self._btn_disable_acc = (AppiumBy.ACCESSIBILITY_ID, "Disable")
        self._btn_enable_partial_payment_acc = (
            AppiumBy.ACCESSIBILITY_ID,
            "Enable Partial Payment",
        )
        self._title_confirm_dialog_acc = (
            AppiumBy.ACCESSIBILITY_ID,
            "Enable partial payment?",
        )
        self._btn_confirm_acc = (AppiumBy.ACCESSIBILITY_ID, "Confirm")
        self._btn_cancel_acc = (AppiumBy.ACCESSIBILITY_ID, "Cancel")
        self._tab_pending_acc = (AppiumBy.ACCESSIBILITY_ID, "Pending")
        self._btn_send_reminder_acc = (AppiumBy.ACCESSIBILITY_ID, "Send reminder")
        # Search icon has empty content-desc (live dump); sibling of title is stable.
        self._icn_search_xpath = (
            AppiumBy.XPATH,
            '//android.widget.ImageView[@content-desc="All payments"]'
            "/following-sibling::android.widget.ImageView[1]",
        )
        self._input_search_class = (AppiumBy.CLASS_NAME, "android.widget.EditText")

    def loc_payment_card(self, identifier: str) -> tuple[str, str]:
        """Payment card whose merged content-desc contains `identifier`
        (e.g. a unique group name or Quick Collect note)."""
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().descriptionContains("{identifier}")',
        )

    def loc_show_menu_for_card(self, identifier: str) -> tuple[str, str]:
        """'Show menu' kebab trigger for the card matching `identifier`.

        Live-confirmed tree shape: the node carrying the card's merged
        content-desc is a *container* whose descendants include "Send
        reminder" and "Show menu" — not a sibling relationship. Both
        `fromParent()` (assumes immediate-parent siblings) and XPath
        `following::` (assumes document-order siblings) failed against the
        real tree; the descendant axis is what actually matches.
        """
        return (
            AppiumBy.XPATH,
            f'//*[contains(@content-desc,"{identifier}")]//*[@content-desc="Show menu"]',
        )

    def loc_view_payments(self) -> tuple[str, str]:
        """'View payments' button on a Monthly Insights month card."""
        return self._btn_view_payments_acc

    def loc_group_payments_title(self) -> tuple[str, str]:
        """Screen title on the Monthly-Insights-scoped 'Group payments' screen."""
        return self._title_group_payments_acc

    def loc_all_payments_title(self) -> tuple[str, str]:
        """Screen title on the global 'All payments' tab."""
        return self._title_all_payments_uia

    def loc_btn_mark_as_paid(self) -> tuple[str, str]:
        return self._btn_mark_as_paid_acc

    def loc_btn_share_payment_link(self) -> tuple[str, str]:
        return self._btn_share_payment_link_acc

    def loc_btn_disable(self) -> tuple[str, str]:
        return self._btn_disable_acc

    def loc_btn_enable_partial_payment(self) -> tuple[str, str]:
        return self._btn_enable_partial_payment_acc

    def loc_confirm_dialog_title(self) -> tuple[str, str]:
        return self._title_confirm_dialog_acc

    def loc_btn_confirm(self) -> tuple[str, str]:
        return self._btn_confirm_acc

    def loc_btn_cancel(self) -> tuple[str, str]:
        return self._btn_cancel_acc

    def loc_tab_pending(self) -> tuple[str, str]:
        """Pending filter chip on All payments."""
        return self._tab_pending_acc

    def loc_btn_send_reminder(self) -> tuple[str, str]:
        """Action on a pending payment card — used to assert dues are listed."""
        return self._btn_send_reminder_acc

    def loc_icn_search(self) -> tuple[str, str]:
        """Magnifying-glass icon in the All payments header."""
        return self._icn_search_xpath

    def loc_input_search(self) -> tuple[str, str]:
        """Search field revealed after tapping the search icon."""
        return self._input_search_class
