"""Create group flow interactions for CoFee."""

from __future__ import annotations

import subprocess
from contextlib import suppress

from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.page_actions import PageActions
from src.page_actions.cofee.login_actions import LoginActions
from src.page_objects.cofee.create_group_po import CreateGroupPo


class CreateGroupActions(PageActions):
    """Business logic for create group with manual member."""

    def __init__(self, driver: WebDriver) -> None:
        self._group_po = CreateGroupPo(driver)
        super().__init__(driver, self._group_po)

    def _tap_left_center(self, element, x_ratio: float = 0.35) -> None:
        """Tap left portion of CTA — avoids dev debug FAB on the right."""
        loc = element.location
        size = element.size
        self._driver.execute_script(
            "mobile: clickGesture",
            {
                "x": int(loc["x"] + size["width"] * x_ratio),
                "y": int(loc["y"] + size["height"] / 2),
            },
        )

    def _adb_tap_element(self, element, x_ratio: float = 0.5) -> None:
        """Tap via adb using element bounds (more reliable than Flutter click/gesture)."""
        loc = element.location
        size = element.size
        x = int(loc["x"] + size["width"] * x_ratio)
        y = int(loc["y"] + size["height"] / 2)
        subprocess.run(
            ["adb", "shell", "input", "tap", str(x), str(y)],
            check=False,
            capture_output=True,
        )

    def _type_digit_by_digit(self, field, text: str) -> None:
        """Type text digit-by-digit (reliable on Flutter EditText)."""
        self.tap(field)
        field.clear()
        for char in text:
            field.send_keys(char)

    def is_select_members_visible(self, timeout: float | None = None) -> bool:
        try:
            self.wait_for_element_visible(
                self._group_po.loc_select_members_title(), timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def select_manually(self) -> None:
        """Choose Manually on the select members bottom sheet."""
        manually = self.wait_for_element_visible(self._group_po.loc_manually(), timeout=10)
        self.tap(manually)

    def is_add_member_visible(self, timeout: float | None = None) -> bool:
        try:
            self.wait_for_element_visible(self._group_po.loc_add_member_title(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def enter_member_details(self, name: str, mobile: str) -> None:
        """Fill name and mobile on add member screen."""
        self.wait_for_element_visible(self._group_po.loc_add_member_title(), timeout=10)
        fields = self._group_po.find_add_member_inputs()
        if len(fields) < 2:
            raise TimeoutException("Expected name and mobile fields on add member screen")
        self._type_digit_by_digit(fields[0], name)
        self.hide_keyboard()
        self._type_digit_by_digit(fields[1], mobile)
        self.hide_keyboard()

    def submit_add_member(self) -> None:
        """Tap Add to return to create group form."""
        add_btn = self._group_po.find_btn_add()
        self._tap_left_center(add_btn, x_ratio=0.25)
        self.wait_for_element_visible(self._group_po.loc_create_group_title(), timeout=15)

    def is_create_group_visible(self, timeout: float | None = None) -> bool:
        try:
            self.wait_for_element_visible(self._group_po.loc_create_group_title(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_schedule_modal_visible(self, timeout: float | None = None) -> bool:
        try:
            self.wait_for_element_visible(
                self._group_po.loc_schedule_payment_title(), timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def enter_group_details(self, group_name: str, amount: str) -> None:
        """Enter group name and fixed fee amount."""
        self.wait_for_element_visible(self._group_po.loc_create_group_title(), timeout=15)
        fields = self._group_po.find_create_group_inputs()
        if len(fields) < 2:
            raise TimeoutException("Expected group name and amount fields")
        self._type_digit_by_digit(fields[0], group_name)
        self.hide_keyboard()
        self._type_digit_by_digit(fields[1], amount)
        self.hide_keyboard()

    def open_fee_collection_day_picker(self) -> None:
        """Open schedule payment collection modal."""
        for _ in range(2):
            self.swipe_up(percent=0.4)
        field = self.wait_for_element_visible(
            self._group_po.loc_fee_collection_day_field(), timeout=10
        )
        self.tap(field)

    def _close_schedule_modal(self) -> None:
        """Close schedule modal via Apply, falling back to Cancel (keeps selection)."""
        for _ in range(3):
            if not self.is_schedule_modal_visible(timeout=1):
                break
            with suppress(Exception):
                self._adb_tap_element(self._group_po.find_btn_apply(), x_ratio=0.5)
            if not self.is_schedule_modal_visible(timeout=1):
                break
            with suppress(Exception):
                self._adb_tap_element(self._group_po.find_btn_cancel(), x_ratio=0.5)
        if self.is_schedule_modal_visible(timeout=2):
            raise TimeoutException("Schedule payment modal did not close")

    def select_last_day_of_month_and_apply(self) -> None:
        """Pick last day of month and close schedule modal until it is truly gone."""
        self.wait_for_element_visible(self._group_po.loc_schedule_payment_title(), timeout=10)
        last_day = self._group_po.find_last_day_of_month()
        self._adb_tap_element(last_day, x_ratio=0.08)
        self._close_schedule_modal()
        self.wait_for_element_visible(
            self._group_po.loc_fee_collection_day_last_of_month(), timeout=5
        )

    def select_weekly_monday_and_apply(self) -> None:
        """Switch frequency to Weekly, select Mon, and close schedule modal.

        Product: WeeklyFrequencySelector (chips Sun–Sat) + field text
        ``Weekly: Monday`` (dayOfWeekLabels).
        """
        self.wait_for_element_visible(self._group_po.loc_schedule_payment_title(), timeout=10)
        monthly = self.wait_for_element_visible(self._group_po.loc_frequency_monthly(), timeout=10)
        self._adb_tap_element(monthly, x_ratio=0.5)
        weekly = self.wait_for_element_visible(self._group_po.loc_frequency_weekly(), timeout=5)
        self._adb_tap_element(weekly, x_ratio=0.5)
        # Wait for weekly chip grid (default selection is Sun) before tapping Mon
        self.wait_for_element_visible(self._group_po.loc_chip_sun(), timeout=10)
        mon = self.wait_for_element_visible(self._group_po.loc_chip_mon(), timeout=5)
        self._adb_tap_element(mon, x_ratio=0.5)
        self._close_schedule_modal()
        self.wait_for_element_visible(
            self._group_po.loc_fee_collection_day_weekly_monday(), timeout=5
        )

    def _wait_for_save_ready(self, timeout: float = 15):
        """Wait for Save after schedule modal is closed."""
        if self.is_schedule_modal_visible(timeout=1):
            with suppress(Exception):
                self._adb_tap_element(self._group_po.find_btn_cancel(), x_ratio=0.5)
        return self.wait_for_element_visible(self._group_po.loc_btn_save(), timeout=timeout)

    def _post_save_reached(self, timeout: float = 10) -> bool:
        """Return True when share promo appears or create-group screen is gone."""
        end_polls = max(1, int(timeout / 0.5))
        for _ in range(end_polls):
            LoginActions(self._driver).dismiss_debug_overlay_if_visible()
            if self._page.is_displayed(self._group_po.loc_share_promo_title()):
                return True
            if not self.is_create_group_visible(timeout=0.4):
                return True
        return False

    def _tap_save_once(self) -> None:
        """Hide keyboard, ensure modal closed, tap far-left of Save (avoid debug FAB)."""
        self.hide_keyboard()
        with suppress(Exception):
            self.swipe_up(percent=0.3)
        save_btn = self._wait_for_save_ready(timeout=15)
        # Prefer adb tap at 20% width — clears purple debug FAB on the right
        self._adb_tap_element(save_btn, x_ratio=0.20)

    def save_group(self) -> None:
        """Tap Save and confirm we left the create-group form (retry once if needed)."""
        self._tap_save_once()
        if self._post_save_reached(timeout=12):
            return

        LoginActions(self._driver).dismiss_debug_overlay_if_visible()
        if not self.is_create_group_visible(timeout=2):
            return

        self._tap_save_once()
        if not self._post_save_reached(timeout=12):
            raise TimeoutException(
                "Save did not navigate away from create group (promo or detail expected)"
            )

    def dismiss_share_promo_if_visible(self, timeout: float = 15) -> None:
        """Dismiss post-save share promo when shown."""
        try:
            self.wait_for_element_visible(self._group_po.loc_share_promo_title(), timeout=timeout)
            share_later = self._group_po.find_share_later()
            self._adb_tap_element(share_later, x_ratio=0.5)
            self.wait_for_element_gone(self._group_po.loc_share_promo_title(), timeout=10)
        except TimeoutException:
            pass

    def create_group_with_manual_member(
        self,
        member_name: str,
        member_mobile: str,
        group_name: str,
        amount: str,
        fee_schedule: str = "monthly_last_day",
    ) -> None:
        """Full create-group happy path from select members through promo dismiss.

        fee_schedule:
          - monthly_last_day — existing P0 (Monthly / last day of month)
          - weekly_monday — Weekly / Mon chip (product WeeklyFrequencySelector)
        """
        self.select_manually()
        self.enter_member_details(member_name, member_mobile)
        self.submit_add_member()
        self.enter_group_details(group_name, amount)
        self.open_fee_collection_day_picker()
        if fee_schedule == "weekly_monday":
            self.select_weekly_monday_and_apply()
        elif fee_schedule == "monthly_last_day":
            self.select_last_day_of_month_and_apply()
        else:
            raise ValueError(f"Unsupported fee_schedule: {fee_schedule}")
        self.save_group()
        self.dismiss_share_promo_if_visible()
