"""CoFee Enable Partial Payment E2E tests.

Covers TC-enable-partial-payment-HP-01, NEG-01, HP-04 from
docs/context/cofee-enable-partial-payment-testcases.md. HP-02/HP-03
(Mark As Paid) and STATE/REG cases are not yet automated — see that file's
"Test data setup" section.
"""

from __future__ import annotations

import allure
import pytest

from dataprovider.dp_enable_partial_payment import (
    get_enable_partial_payment_test_data,
    get_entry_point_test_data,
    get_threshold_boundary_test_data,
)
from src.steps.cofee.login_steps import user_ensures_logged_in_home
from src.steps.cofee.payment_steps import (
    user_enables_partial_payment_and_verifies,
    user_opens_kebab_menu_from_all_payments,
    user_opens_kebab_menu_from_group_payments,
    user_opens_kebab_menu_from_member_history,
    user_sets_up_group_with_payment_request,
    user_verifies_enable_partial_payment_option,
)
from tests.parallel_groups import PARALLEL_GROUP_PAYMENTS

pytestmark = [pytest.mark.xdist_group(PARALLEL_GROUP_PAYMENTS)]


def _open_kebab_menu_from_entry_point(
    driver, entry_point: str, member_name: str, card_identifier: str
) -> None:
    """Dispatch to the right navigation path for the given entry point."""
    if entry_point == "member_history":
        user_opens_kebab_menu_from_member_history(driver, member_name, card_identifier)
    elif entry_point == "group_payments":
        user_opens_kebab_menu_from_group_payments(driver, card_identifier)
    elif entry_point == "all_payments":
        user_opens_kebab_menu_from_all_payments(driver, card_identifier)
    else:
        raise ValueError(f"Unknown entry point: {entry_point}")


@allure.epic("CoFee")
@allure.feature("Payments")
@pytest.mark.e2e
@pytest.mark.android
@pytest.mark.auth_profile("default")
class TestEnablePartialPayment:
    """Enable Partial Payment — threshold, entry points, and core flow."""

    @allure.story("Enable partial payment on an eligible payment")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    @pytest.mark.parametrize(
        "group_name,member_name,member_mobile,note,amount",
        get_enable_partial_payment_test_data(),
    )
    def test_enable_partial_payment_on_eligible_payment(
        self,
        driver,
        mobile: str,
        otp: str,
        group_name: str,
        member_name: str,
        member_mobile: str,
        note: str,
        amount: int,
    ) -> None:
        """TC-enable-partial-payment-HP-01: enable partial payment and verify
        the option disappears immediately (no refresh needed)."""
        allure.dynamic.title(f"Enable partial payment on ₹{amount} request ({note})")
        user_ensures_logged_in_home(driver, mobile, otp)
        user_sets_up_group_with_payment_request(
            driver, member_name, member_mobile, group_name, amount, note
        )
        user_opens_kebab_menu_from_member_history(driver, member_name, note)
        user_enables_partial_payment_and_verifies(driver, note)

    @allure.story("Partial-payment option respects the ₹2,000 threshold")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    @pytest.mark.parametrize(
        "group_name,member_name,member_mobile,note,amount,expected_option",
        get_threshold_boundary_test_data(),
    )
    def test_partial_payment_option_visibility_at_threshold(
        self,
        driver,
        mobile: str,
        otp: str,
        group_name: str,
        member_name: str,
        member_mobile: str,
        note: str,
        amount: int,
        expected_option: bool,
    ) -> None:
        """TC-enable-partial-payment-NEG-01: ₹1,999 → option absent,
        ₹2,000 → option present (confirmed live, exact boundary)."""
        allure.dynamic.title(f"Partial payment option at ₹{amount} (expect={expected_option})")
        user_ensures_logged_in_home(driver, mobile, otp)
        user_sets_up_group_with_payment_request(
            driver, member_name, member_mobile, group_name, amount, note
        )
        user_opens_kebab_menu_from_member_history(driver, member_name, note)
        user_verifies_enable_partial_payment_option(driver, expected_option)

    @allure.story("Partial-payment option is available from every entry point")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    @pytest.mark.parametrize(
        "group_name,member_name,member_mobile,note,amount,entry_point",
        get_entry_point_test_data(),
    )
    def test_partial_payment_option_available_from_all_entry_points(
        self,
        driver,
        mobile: str,
        otp: str,
        group_name: str,
        member_name: str,
        member_mobile: str,
        note: str,
        amount: int,
        entry_point: str,
    ) -> None:
        """TC-enable-partial-payment-HP-04: per-member history, 'Group payments'
        (Monthly Insights), and the global 'All payments' tab all expose the
        same kebab-menu action for the same eligible payment."""
        allure.dynamic.title(f"Enable Partial Payment option via {entry_point}")
        user_ensures_logged_in_home(driver, mobile, otp)
        user_sets_up_group_with_payment_request(
            driver, member_name, member_mobile, group_name, amount, note
        )
        _open_kebab_menu_from_entry_point(driver, entry_point, member_name, note)
        user_verifies_enable_partial_payment_option(driver, expected=True)
