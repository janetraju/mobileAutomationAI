"""CoFee create group E2E tests."""

from __future__ import annotations

import allure
import pytest

from dataprovider.dp_create_group import (
    get_create_group_test_data,
    get_create_group_weekly_test_data,
)
from src.steps.cofee.group_steps import user_creates_and_verifies_group_from_home
from tests.parallel_groups import PARALLEL_GROUP_GROUPS

pytestmark = [pytest.mark.xdist_group(PARALLEL_GROUP_GROUPS)]


@allure.epic("CoFee")
@allure.feature("Groups")
@pytest.mark.e2e
@pytest.mark.p0
@pytest.mark.android
@pytest.mark.authenticated
@pytest.mark.auth_profile("default")
class TestCreateGroup:
    """Create group with manual member — P0 smoke."""

    @allure.story("Create group with manual member")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "member_name,member_mobile,group_name,amount,formatted_fee,fee_schedule",
        get_create_group_test_data(),
    )
    def test_create_group_with_manual_member(
        self,
        driver,
        member_name: str,
        member_mobile: str,
        group_name: str,
        amount: str,
        formatted_fee: str,
        fee_schedule: str,
    ) -> None:
        """Creates a fixed-fee group with manual member and verifies detail."""
        allure.dynamic.title(f"Create group {group_name} with manual member")
        user_creates_and_verifies_group_from_home(
            driver,
            member_name=member_name,
            member_mobile=member_mobile,
            group_name=group_name,
            amount=amount,
            formatted_fee=formatted_fee,
            fee_schedule=fee_schedule,
        )

    @allure.story("Create group with weekly fee collection")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "member_name,member_mobile,group_name,amount,formatted_fee,fee_schedule",
        get_create_group_weekly_test_data(),
    )
    def test_create_group_with_weekly_fee_collection(
        self,
        driver,
        member_name: str,
        member_mobile: str,
        group_name: str,
        amount: str,
        formatted_fee: str,
        fee_schedule: str,
    ) -> None:
        """Create group with Weekly / Monday fee schedule (product WeeklyFrequencySelector)."""
        allure.dynamic.title(f"Create group {group_name} with weekly Monday fee")
        user_creates_and_verifies_group_from_home(
            driver,
            member_name=member_name,
            member_mobile=member_mobile,
            group_name=group_name,
            amount=amount,
            formatted_fee=formatted_fee,
            fee_schedule=fee_schedule,
        )
