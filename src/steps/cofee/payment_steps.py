"""Reusable Enable Partial Payment steps for CoFee."""

from __future__ import annotations

import allure
from appium.webdriver.webdriver import WebDriver

from src.core.assert_helper import assert_element_visible, assert_false, assert_true
from src.page_actions.cofee.group_detail_actions import GroupDetailActions
from src.page_actions.cofee.home_actions import HomeActions
from src.page_actions.cofee.payment_card_actions import PaymentCardActions
from src.page_actions.cofee.quick_collect_actions import QuickCollectActions
from src.steps.cofee.group_steps import (
    user_creates_group_with_manual_member,
    user_opens_create_group_from_home,
)


@allure.step("User creates a Quick Collect payment request of ₹{amount} for {member_name}")
def user_creates_quick_collect_payment(
    driver: WebDriver, member_name: str, amount: int, note: str
) -> None:
    """From group detail, create a payment request via Quick Collect."""
    detail = GroupDetailActions(driver)
    detail.tap_quick_collect()
    quick_collect = QuickCollectActions(driver)
    quick_collect.create_payment_request(member_name, amount, note)


@allure.step("User sets up group {group_name} with a ₹{amount} payment request")
def user_sets_up_group_with_payment_request(
    driver: WebDriver,
    member_name: str,
    member_mobile: str,
    group_name: str,
    amount: int,
    note: str,
) -> None:
    """Create a fresh group + member, then a Quick Collect payment request."""
    user_opens_create_group_from_home(driver)
    user_creates_group_with_manual_member(
        driver,
        member_name=member_name,
        member_mobile=member_mobile,
        group_name=group_name,
        amount="5000",  # group fee is irrelevant — Quick Collect uses its own amount
    )
    user_creates_quick_collect_payment(driver, member_name, amount, note)


@allure.step("User opens the kebab menu from per-member payment history")
def user_opens_kebab_menu_from_member_history(
    driver: WebDriver, member_name: str, card_identifier: str
) -> None:
    """Groups detail → tap member row → open kebab on the matching card."""
    GroupDetailActions(driver).tap_member_row(member_name)
    PaymentCardActions(driver).open_kebab_menu(card_identifier)


@allure.step("User opens the kebab menu from the 'Group payments' screen")
def user_opens_kebab_menu_from_group_payments(driver: WebDriver, card_identifier: str) -> None:
    """Group detail → Monthly Insights → View payments → open kebab on the matching card."""
    GroupDetailActions(driver).tap_monthly_insights()
    card_actions = PaymentCardActions(driver)
    card_actions.open_group_payments_via_monthly_insights()
    assert_element_visible(
        card_actions.is_group_payments_screen_visible(timeout=10),
        "'Group payments' screen title",
    )
    card_actions.open_kebab_menu(card_identifier)


@allure.step("User opens the kebab menu from the global 'All payments' tab")
def user_opens_kebab_menu_from_all_payments(driver: WebDriver, card_identifier: str) -> None:
    """Group detail has no bottom nav (full-screen stacked view) — return to
    Home first, then bottom nav Payments tab → open kebab on the matching card."""
    home = HomeActions(driver)
    assert_element_visible(home.return_to_home_dashboard(), "home screen (bottom nav visible)")
    home.tap_payments_tab()
    card_actions = PaymentCardActions(driver)
    assert_element_visible(
        card_actions.is_all_payments_screen_visible(timeout=10), "'All payments' screen title"
    )
    card_actions.open_kebab_menu(card_identifier)


@allure.step("User verifies Enable Partial Payment option presence (expected={expected})")
def user_verifies_enable_partial_payment_option(driver: WebDriver, expected: bool) -> None:
    """Assert the already-open kebab menu shows/hides Enable Partial Payment."""
    card_actions = PaymentCardActions(driver)
    is_visible = card_actions.is_enable_partial_payment_visible(timeout=5)
    if expected:
        assert_true(is_visible, "Enable Partial Payment option should be present")
    else:
        assert_false(is_visible, "Enable Partial Payment option should be absent")
    card_actions.dismiss_kebab_menu()


@allure.step("User enables partial payment and verifies the option disappears")
def user_enables_partial_payment_and_verifies(driver: WebDriver, card_identifier: str) -> None:
    """Confirm enable-partial-payment, then reopen the same card's kebab menu
    and assert the option is immediately gone (confirmed live — no refresh needed)."""
    card_actions = PaymentCardActions(driver)
    card_actions.tap_enable_partial_payment()
    assert_element_visible(
        card_actions.is_confirm_dialog_visible(timeout=10), "enable partial payment dialog"
    )
    card_actions.confirm_enable_partial_payment()
    card_actions.open_kebab_menu(card_identifier, timeout=15)
    assert_false(
        card_actions.is_enable_partial_payment_visible(timeout=5),
        "Enable Partial Payment option should disappear immediately after enabling",
    )
    card_actions.dismiss_kebab_menu()


@allure.step("User opens All payments Pending from home Dues View All")
def user_opens_pending_dues_via_view_all(driver: WebDriver) -> None:
    """Home → Dues 'View All' → All payments with Pending dues listed."""
    HomeActions(driver).tap_dues_view_all()
    card_actions = PaymentCardActions(driver)
    assert_element_visible(
        card_actions.is_all_payments_screen_visible(timeout=10),
        "'All payments' screen title",
    )
    assert_element_visible(
        card_actions.is_pending_tab_visible(timeout=10),
        "Pending filter on payments tab",
    )
    assert_element_visible(
        card_actions.are_pending_dues_listed(timeout=10),
        "pending dues list (Send reminder)",
    )


@allure.step("User searches All payments for '{query}' and verifies '{expected_name}'")
def user_searches_all_payments_and_verifies(
    driver: WebDriver, query: str, expected_name: str | None = None
) -> None:
    """Tap search, type `query`, assert a card matching `expected_name` is listed.

    `expected_name` defaults to `query`. Pass a distinct value when the UI
    search is case-insensitive but content-desc casing differs (e.g. user1 →
    User1).
    """
    card_actions = PaymentCardActions(driver)
    card_actions.tap_search_icon()
    card_actions.search_payments(query)
    match = expected_name if expected_name is not None else query
    assert_element_visible(
        card_actions.is_payment_listed(match, timeout=10),
        f"payment card matching {match!r}",
    )
