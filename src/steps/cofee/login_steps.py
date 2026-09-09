from __future__ import annotations

import allure

from src.page_actions.cofee.login_actions import LoginActions


class LoginSteps:
    def __init__(self, driver, settings=None):
        self.actions = LoginActions(driver, settings)

    @allure.step("Log in with mobile {mobile} + fixed dev OTP")
    def login_with_otp(self, mobile: str, otp: str) -> None:
        if self.actions.is_already_logged_in():
            # NO_RESET=true keeps the app's session across launches (per
            # docs/cofee-flow.md -> Known blockers / Test data) -- a fresh
            # Appium session may land straight on Home instead of the phone
            # number screen. Only drive the OTP flow when it's actually shown.
            return
        self.actions.enter_mobile_number(mobile)
        self.actions.tap_next()
        self.actions.wait_for_otp_screen()
        self.actions.enter_otp(otp)
        self.actions.wait_for_home()
