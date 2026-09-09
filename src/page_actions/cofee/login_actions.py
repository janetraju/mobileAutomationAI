from __future__ import annotations

from src.core.base_actions import PageActions
from src.page_objects.cofee.login_po import LoginPage


class LoginActions(PageActions):
    def __init__(self, driver, settings=None):
        super().__init__(driver, settings)
        self.page = LoginPage(driver, self.settings)

    def enter_mobile_number(self, mobile: str) -> None:
        field = self.page.find_input_mobile()
        self.type_text(field, mobile)

    def tap_next(self) -> None:
        self.tap(self.page.find_btn_next())

    def wait_for_otp_screen(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(lambda _: self.page.is_otp_prompt_visible(timeout=2))

    def enter_otp(self, otp: str) -> None:
        field = self.page.find_input_otp()
        self.type_text(field, otp, clear_first=False)

    def wait_for_home(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(lambda _: self.page.is_home_visible(timeout=2))

    def is_already_logged_in(self) -> bool:
        # Cold Appium session start includes the splash screen -- give it
        # enough time to resolve to either Home or the login screen before
        # deciding which branch to take.
        return self.page.is_home_visible(timeout=10)
