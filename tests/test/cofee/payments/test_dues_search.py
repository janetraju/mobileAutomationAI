"""CoFee Dues View All → Pending payments search E2E.

Flow: home Dues View All → verify Pending dues listed → search member.
"""

from __future__ import annotations

import allure
import pytest

from dataprovider.dp_dues_search import get_dues_search_test_data
from src.steps.cofee.payment_steps import (
    user_opens_pending_dues_via_view_all,
    user_searches_all_payments_and_verifies,
)
from tests.parallel_groups import PARALLEL_GROUP_PAYMENTS

pytestmark = [pytest.mark.xdist_group(PARALLEL_GROUP_PAYMENTS)]


@allure.epic("CoFee")
@allure.feature("Payments")
@pytest.mark.e2e
@pytest.mark.android
@pytest.mark.authenticated
@pytest.mark.auth_profile("default")
class TestDuesSearch:
    """Home Dues View All → Pending list → search."""

    @allure.story("Search pending dues from home View All")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p0
    @pytest.mark.dues
    @pytest.mark.parametrize("search_query,expected_name", get_dues_search_test_data())
    def test_search_pending_due_from_dues_view_all(
        self,
        driver,
        search_query: str,
        expected_name: str,
    ) -> None:
        """Open Pending via Dues View All, search for a member, assert listed."""
        allure.dynamic.title(f"Search pending dues for {search_query}")
        user_opens_pending_dues_via_view_all(driver)
        user_searches_all_payments_and_verifies(driver, search_query, expected_name)
