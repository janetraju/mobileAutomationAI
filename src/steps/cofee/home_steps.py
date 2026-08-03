"""Reusable Home dashboard steps for CoFee."""

from __future__ import annotations

import allure
from appium.webdriver.webdriver import WebDriver

from src.core.assert_helper import assert_element_visible
from src.page_actions.cofee.groups_list_actions import GroupsListActions
from src.page_actions.cofee.home_actions import HomeActions


@allure.step("User opens My active groups via home Groups View All")
def user_opens_groups_list_via_home_view_all(driver: WebDriver) -> None:
    """Home → Groups section View All → My active groups list."""
    HomeActions(driver).tap_groups_view_all()
    groups = GroupsListActions(driver)
    assert_element_visible(
        groups.is_my_active_groups_visible(timeout=10),
        "'My active groups' list title",
    )
