"""Reusable create group steps for CoFee."""

from __future__ import annotations

import allure
from appium.webdriver.webdriver import WebDriver

from src.core.assert_helper import assert_element_visible
from src.page_actions.cofee.create_group_actions import CreateGroupActions
from src.page_actions.cofee.group_detail_actions import GroupDetailActions
from src.page_actions.cofee.home_actions import HomeActions
from src.page_actions.cofee.login_actions import LoginActions


@allure.step("User opens create group from home")
def user_opens_create_group_from_home(driver: WebDriver) -> None:
    """Tap Add New on home and wait for select members sheet."""
    LoginActions(driver).dismiss_debug_overlay_if_visible()
    home = HomeActions(driver)
    assert_element_visible(home.is_home_screen_visible(timeout=5), "home screen")
    home.tap_add_new_group()
    group = CreateGroupActions(driver)
    assert_element_visible(group.is_select_members_visible(timeout=10), "select members sheet")


@allure.step("User creates group {group_name} with manual member {member_name}")
def user_creates_group_with_manual_member(
    driver: WebDriver,
    member_name: str,
    member_mobile: str,
    group_name: str,
    amount: str,
) -> None:
    """Complete create group flow through promo dismiss."""
    actions = CreateGroupActions(driver)
    actions.create_group_with_manual_member(
        member_name=member_name,
        member_mobile=member_mobile,
        group_name=group_name,
        amount=amount,
    )


@allure.step("User verifies group {group_name} detail screen")
def user_verifies_group_detail(
    driver: WebDriver,
    group_name: str,
    member_name: str,
    formatted_fee: str,
    member_count: int = 1,
) -> None:
    """Assert group detail shows name, member count, fee, and overview."""
    detail = GroupDetailActions(driver)
    assert_element_visible(
        detail.is_group_detail_visible(group_name, member_count=member_count, timeout=20),
        "group detail header",
    )
    assert_element_visible(
        detail.is_member_with_fee_visible(member_name, formatted_fee, timeout=10),
        "member fee amount",
    )
    assert_element_visible(detail.is_overview_visible(timeout=5), "group overview section")


@allure.step("User creates and verifies group from home")
def user_creates_and_verifies_group_from_home(
    driver: WebDriver,
    member_name: str,
    member_mobile: str,
    group_name: str,
    amount: str,
    formatted_fee: str,
) -> None:
    """End-to-end create group P0 flow from home through verification."""
    user_opens_create_group_from_home(driver)
    user_creates_group_with_manual_member(
        driver, member_name, member_mobile, group_name, amount
    )
    user_verifies_group_detail(
        driver, group_name, member_name, formatted_fee
    )
