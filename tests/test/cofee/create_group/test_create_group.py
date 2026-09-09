from __future__ import annotations

import allure
import pytest

from src.steps.cofee.create_group_steps import CreateGroupSteps
from src.steps.cofee.login_steps import LoginSteps
from tests.dataprovider.dp_create_group import get_create_fixed_fee_group_test_data


@allure.epic("CoFee")
@allure.feature("Create Group")
@pytest.mark.e2e
@pytest.mark.p0
@pytest.mark.android
@pytest.mark.parametrize("data", get_create_fixed_fee_group_test_data())
@allure.story("Create a Fixed fee group")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_fixed_fee_group(driver, settings, mobile, otp, data):
    login = LoginSteps(driver, settings)
    login.login_with_otp(mobile, otp)

    group = CreateGroupSteps(driver, settings)
    group.add_member_manually(data["member_name"], data["member_mobile"])
    group.create_fixed_fee_group(data["group_name"], data["amount"])
    group.assert_group_created(data["group_name"])
