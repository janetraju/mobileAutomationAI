"""Reusable login steps for CoFee."""

from __future__ import annotations

from contextlib import suppress

import allure
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.assert_helper import assert_element_visible
from src.core.device_helper import DeviceHelper
from src.core.session_state import SessionState
from src.page_actions.cofee.home_actions import HomeActions
from src.page_actions.cofee.login_actions import LoginActions


def _active_profile() -> str:
    return SessionState.get_active_profile() or "default"


def _activate_app(driver: WebDriver) -> None:
    with suppress(Exception):
        DeviceHelper(driver).activate_app()


def _return_to_home_if_logged_in(driver: WebDriver) -> bool:
    """Activate app and return True when home is already visible."""
    actions = LoginActions(driver)
    _activate_app(driver)
    actions.dismiss_debug_overlay_if_visible()
    home = HomeActions(driver)
    return home.return_to_home_dashboard()


@allure.step("User logs in without clearing app data")
def user_logs_in_without_fresh_install(driver: WebDriver, mobile: str, otp: str) -> None:
    """Complete login when app data is preserved (no pm clear)."""
    if _return_to_home_if_logged_in(driver):
        SessionState.mark_logged_in(_active_profile())
        return

    actions = LoginActions(driver)
    if actions.is_otp_screen_visible(timeout=2):
        user_enters_otp_and_logs_in(driver, otp)
    elif actions.is_account_picker_visible(timeout=2):
        actions.select_account_and_continue()
        assert_element_visible(actions.is_home_screen_visible(timeout=20), "home screen")
    elif actions.is_phone_screen_visible(timeout=2):
        user_enters_phone_and_requests_otp(driver, mobile)
        user_enters_otp_and_logs_in(driver, otp)
    else:
        user_reaches_phone_login_screen(driver)
        user_enters_phone_and_requests_otp(driver, mobile)
        user_enters_otp_and_logs_in(driver, otp)

    SessionState.mark_logged_in(_active_profile())


@allure.step("User ensures logged-in home (session reuse)")
def user_ensures_logged_in_home(driver: WebDriver, mobile: str, otp: str) -> None:
    """Reuse login when home is already reachable; otherwise login without pm clear."""
    if _return_to_home_if_logged_in(driver):
        return
    try:
        user_logs_in_without_fresh_install(driver, mobile, otp)
    except TimeoutException:
        user_logs_in_with_phone_otp(driver, mobile, otp)


@allure.step("App reset for fresh login")
def user_starts_from_fresh_install(driver: WebDriver) -> None:
    """Clear app data and relaunch for a clean login path (Android or iOS)."""
    DeviceHelper(driver).clear_and_relaunch()


@allure.step("User reaches phone login screen")
def user_reaches_phone_login_screen(driver: WebDriver) -> None:
    """Dismiss permission once, then advance onboarding to phone entry."""
    actions = LoginActions(driver)
    actions.dismiss_notification_permission_if_visible()
    actions.navigate_to_phone_entry_screen()
    assert_element_visible(actions.is_phone_screen_visible(timeout=5), "phone login screen")


@allure.step("User enters phone number {mobile} and requests OTP")
def user_enters_phone_and_requests_otp(driver: WebDriver, mobile: str) -> None:
    """Enter phone number and tap Next to trigger OTP."""
    actions = LoginActions(driver)
    actions.enter_phone_number(mobile)
    actions.submit_phone_number()
    assert_element_visible(actions.is_otp_screen_visible(timeout=20), "OTP screen")


@allure.step("User enters OTP and completes login")
def user_enters_otp_and_logs_in(driver: WebDriver, otp: str) -> None:
    """Enter OTP, handle account picker if shown, and reach home."""
    actions = LoginActions(driver)
    actions.complete_otp_and_reach_home(otp)
    assert_element_visible(actions.is_home_screen_visible(timeout=5), "home screen")


@allure.step("User logs in with phone {mobile} and OTP")
def user_logs_in_with_phone_otp(driver: WebDriver, mobile: str, otp: str) -> None:
    """Full phone + OTP login flow — single straight path."""
    user_starts_from_fresh_install(driver)
    user_reaches_phone_login_screen(driver)
    user_enters_phone_and_requests_otp(driver, mobile)
    user_enters_otp_and_logs_in(driver, otp)
    SessionState.mark_logged_in(_active_profile())
