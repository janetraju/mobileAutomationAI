"""Groups list (My active groups) interactions for CoFee."""

from __future__ import annotations

from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.page_actions import PageActions
from src.page_objects.cofee.groups_list_po import GroupsListPo


class GroupsListActions(PageActions):
    """Business logic for the My active groups list."""

    def __init__(self, driver: WebDriver) -> None:
        self._groups_list_po = GroupsListPo(driver)
        super().__init__(driver, self._groups_list_po)

    def is_my_active_groups_visible(self, timeout: float | None = None) -> bool:
        """Return True when the My active groups title is visible."""
        try:
            self.wait_for_element_visible(
                self._groups_list_po.loc_txt_my_active_groups(), timeout=timeout
            )
            return True
        except TimeoutException:
            return False
