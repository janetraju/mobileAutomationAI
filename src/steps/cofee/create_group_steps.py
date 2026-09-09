from __future__ import annotations

import allure
from selenium.common.exceptions import TimeoutException

from src.core import assert_helper
from src.page_actions.cofee.add_member_actions import AddMemberActions
from src.page_actions.cofee.create_group_actions import CreateGroupActions
from src.page_actions.cofee.group_detail_actions import GroupDetailActions
from src.page_actions.cofee.groups_list_actions import GroupsListActions
from src.page_actions.cofee.home_actions import HomeActions


class CreateGroupSteps:
    def __init__(self, driver, settings=None):
        self.home = HomeActions(driver, settings)
        self.member = AddMemberActions(driver, settings)
        self.group = CreateGroupActions(driver, settings)
        self.groups_list = GroupsListActions(driver, settings)
        self.detail = GroupDetailActions(driver, settings)

    @allure.step("Add a single member manually: {name} / {mobile}")
    def add_member_manually(self, name: str, mobile: str) -> None:
        self.home.tap_add_new()
        self.member.wait_for_select_members_modal()
        self.member.tap_manually()
        self.member.wait_for_add_member_screen()
        self.member.enter_name(name)
        self.member.enter_mobile(mobile)
        self.member.tap_add()

    @allure.step("Create a Fixed fee group: {group_name}, amount {amount}")
    def create_fixed_fee_group(self, group_name: str, amount: str) -> None:
        self.group.wait_for_form()
        self.group.enter_group_name(group_name)
        self.group.enter_amount(amount)
        self.group.enter_member_amount(amount)
        self.group.accept_default_fee_collection_day()
        self.group.tap_save()

    @allure.step("Verify group {group_name} was created")
    def assert_group_created(self, group_name: str) -> None:
        # Save's backend round-trip is variably slow; give it real headroom
        # rather than a tight wait -- confirmed live to take anywhere from
        # ~4s to 20s+ before the detail screen (or, sometimes, a "Get paid
        # faster" share interstitial first) appears.
        self.detail.dismiss_share_prompt_if_present()
        by, value = self.detail.page.loc_group_title(group_name)
        try:
            self.detail.page.wait_visible(by, value, timeout=30)
        except TimeoutException:
            pass  # let assert_helper below report the failure with context
        assert_helper.assert_visible(
            self.detail.page,
            by,
            value,
            message=f"Expected the new group's detail screen to show its name {group_name!r}",
        )
