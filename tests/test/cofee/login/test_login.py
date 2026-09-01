"""CoFee login E2E tests."""

from __future__ import annotations

import allure
import pytest

from dataprovider.dp_login import get_login_test_data
from src.steps.cofee.login_steps import user_logs_in_with_phone_otp
from tests.parallel_groups import PARALLEL_GROUP_AUTH

pytestmark = [pytest.mark.xdist_group(PARALLEL_GROUP_AUTH)]


@allure.epic("CoFee")
@allure.feature("Login")
@pytest.mark.e2e
@pytest.mark.p0
@pytest.mark.android
@pytest.mark.ios
@pytest.mark.login
@pytest.mark.fresh
@pytest.mark.auth_profile("default")
class TestLogin:
    """Phone + OTP login scenarios — owns a clean app (no shared login-first)."""

    @allure.story("Valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("mobile,otp", get_login_test_data())
    def test_phone_otp_login_success(self, driver, mobile: str, otp: str) -> None:
        """User logs in with valid phone number and OTP."""
        allure.dynamic.title(f"Login success with phone ending {mobile[-4:]}")
        user_logs_in_with_phone_otp(driver, mobile, otp)
