"""CoFee Home exploratory E2E.

Flow: home Groups View All → My active groups list visible.
"""

from __future__ import annotations

import allure
import pytest

from src.steps.cofee.home_steps import user_opens_groups_list_via_home_view_all
from tests.parallel_groups import PARALLEL_GROUP_GROUPS

pytestmark = [pytest.mark.xdist_group(PARALLEL_GROUP_GROUPS)]


@allure.epic("CoFee")
@allure.feature("Home")
@pytest.mark.e2e
@pytest.mark.android
@pytest.mark.authenticated
@pytest.mark.auth_profile("default")
class TestHomeExplore:
    """Exploratory smoke from the logged-in home dashboard."""

    @allure.story("Groups View All from home")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p1
    @pytest.mark.home
    def test_open_groups_list_via_home_view_all(self, driver) -> None:
        """Open My active groups from the home Groups View All CTA."""
        allure.dynamic.title("Home Groups View All opens My active groups")
        user_opens_groups_list_via_home_view_all(driver)
