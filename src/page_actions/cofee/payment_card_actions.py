"""Payment card / kebab-menu interactions for CoFee.

Shared across the three payment-list screens confirmed live to use the same
underlying widget (`payment_card_bottom_actions.dart`): per-member payment
history, the Monthly-Insights-scoped "Group payments" screen, and the
global "All payments" tab.
"""

from __future__ import annotations

from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.page_actions import PageActions
from src.page_objects.cofee.payment_card_po import PaymentCardPo


class PaymentCardActions(PageActions):
    """Business logic for opening a payment card's kebab menu and enabling
    partial payment."""

    def __init__(self, driver: WebDriver) -> None:
        self._card_po = PaymentCardPo(driver)
        super().__init__(driver, self._card_po)

    def open_kebab_menu(self, card_identifier: str, timeout: float | None = None) -> None:
        """Open the '⋮' kebab menu on the card matching `card_identifier`."""
        self.wait_for_element_visible(
            self._card_po.loc_payment_card(card_identifier), timeout=timeout or 15
        )
        menu_button = self.wait_for_element_visible(
            self._card_po.loc_show_menu_for_card(card_identifier), timeout=timeout or 10
        )
        self.tap(menu_button)

    def is_enable_partial_payment_visible(self, timeout: float | None = None) -> bool:
        """Return True when the kebab menu shows 'Enable Partial Payment'."""
        try:
            self.wait_for_element_visible(
                self._card_po.loc_btn_enable_partial_payment(), timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def dismiss_kebab_menu(self) -> None:
        """Close the kebab menu without selecting an action."""
        self._driver.press_keycode(4)

    def tap_enable_partial_payment(self) -> None:
        """Tap 'Enable Partial Payment' in the open kebab menu."""
        option = self.wait_for_element_visible(
            self._card_po.loc_btn_enable_partial_payment(), timeout=10
        )
        self.tap(option)

    def is_confirm_dialog_visible(self, timeout: float | None = None) -> bool:
        """Return True when the enable-partial-payment confirm dialog is shown."""
        try:
            self.wait_for_element_visible(self._card_po.loc_confirm_dialog_title(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def confirm_enable_partial_payment(self) -> None:
        """Tap Confirm and wait for the dialog to dismiss (API round-trip)."""
        confirm = self.wait_for_element_visible(self._card_po.loc_btn_confirm(), timeout=10)
        self.tap(confirm)
        self.wait_for_element_gone(self._card_po.loc_confirm_dialog_title(), timeout=15)

    def enable_partial_payment(self, card_identifier: str) -> None:
        """Open the kebab menu, tap Enable Partial Payment, confirm."""
        self.open_kebab_menu(card_identifier)
        self.tap_enable_partial_payment()
        self.confirm_enable_partial_payment()

    def open_group_payments_via_monthly_insights(self) -> None:
        """From group detail (Monthly Insights already tapped), open 'View payments'."""
        view_payments = self.wait_for_element_visible(self._card_po.loc_view_payments(), timeout=10)
        self.tap(view_payments)

    def is_group_payments_screen_visible(self, timeout: float | None = None) -> bool:
        """Return True when the literal 'Group payments' screen is shown."""
        try:
            self.wait_for_element_visible(self._card_po.loc_group_payments_title(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_all_payments_screen_visible(self, timeout: float | None = None) -> bool:
        """Return True when the global 'All payments' screen is shown."""
        try:
            self.wait_for_element_visible(self._card_po.loc_all_payments_title(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_pending_tab_visible(self, timeout: float | None = None) -> bool:
        """Return True when the Pending filter chip is on screen.

        Live-confirmed: UiAutomator `selected` stays false even when Pending
        is the active filter (Dues View All lands here by default), so callers
        assert chip presence + listed dues rather than the selected flag.
        """
        try:
            self.wait_for_element_visible(self._card_po.loc_tab_pending(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def are_pending_dues_listed(self, timeout: float | None = None) -> bool:
        """Return True when at least one pending card exposes 'Send reminder'."""
        try:
            self.wait_for_element_visible(self._card_po.loc_btn_send_reminder(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def tap_search_icon(self) -> None:
        """Open the All payments search field via the header magnifying glass."""
        search = self.wait_for_element_visible(self._card_po.loc_icn_search(), timeout=10)
        self.tap(search)
        self.wait_for_element_visible(self._card_po.loc_input_search(), timeout=10)

    def search_payments(self, query: str) -> None:
        """Type into the All payments search field (field must already be open)."""
        field = self.wait_for_element_visible(self._card_po.loc_input_search(), timeout=10)
        self.tap(field)
        # Flutter EditText often keeps prior text after clear(); backspace first.
        current = field.text or ""
        for _ in range(len(current) + 2):
            self._driver.press_keycode(67)
        self.type_text(field, query)

    def is_payment_listed(self, identifier: str, timeout: float | None = None) -> bool:
        """Return True when a payment card matching `identifier` is visible."""
        try:
            self.wait_for_element_visible(
                self._card_po.loc_payment_card(identifier), timeout=timeout
            )
            return True
        except TimeoutException:
            return False
