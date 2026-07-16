"""Group detail screen interactions for CoFee."""

from __future__ import annotations

from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.page_actions import PageActions
from src.page_objects.cofee.group_detail_po import GroupDetailPo


class GroupDetailActions(PageActions):
    """Assertions helpers for group detail after creation."""

    def __init__(self, driver: WebDriver) -> None:
        self._detail_po = GroupDetailPo(driver)
        super().__init__(driver, self._detail_po)

    def is_group_detail_visible(
        self,
        group_name: str,
        member_count: int = 1,
        timeout: float | None = None,
    ) -> bool:
        """Return True when group detail header is shown."""
        try:
            self.wait_for_element_visible(
                self._detail_po.loc_group_name(group_name), timeout=timeout
            )
            self.wait_for_element_visible(
                self._detail_po.loc_active_member_count(member_count), timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def is_member_with_fee_visible(
        self,
        member_name: str,
        formatted_amount: str,
        timeout: float | None = None,
    ) -> bool:
        """Return True when member row shows expected fee amount."""
        try:
            self.wait_for_element_visible(
                self._detail_po.loc_member_card(member_name), timeout=timeout
            )
            self.wait_for_element_visible(
                self._detail_po.loc_member_fee_amount(formatted_amount), timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def is_overview_visible(self, timeout: float | None = None) -> bool:
        try:
            self.wait_for_element_visible(self._detail_po.loc_overview(), timeout=timeout)
            self.wait_for_element_visible(self._detail_po.loc_amount_collected(), timeout=timeout)
            self.wait_for_element_visible(self._detail_po.loc_amount_due(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def tap_member_row(self, member_name: str) -> None:
        """Open a member's payment history from group detail."""
        row = self.wait_for_element_visible(
            self._detail_po.loc_member_card(member_name), timeout=10
        )
        self.tap(row)

    def tap_quick_collect(self) -> None:
        """Open the Quick Collect flow from group detail."""
        button = self.wait_for_element_visible(self._detail_po.loc_quick_collect(), timeout=10)
        self.tap(button)

    def tap_monthly_insights(self) -> None:
        """Open the Monthly Insights bottom sheet from group detail."""
        button = self.wait_for_element_visible(self._detail_po.loc_monthly_insights(), timeout=10)
        self.tap(button)
