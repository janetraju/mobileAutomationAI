"""Login and onboarding interactions for CoFee."""

from __future__ import annotations

import subprocess
import time
from contextlib import suppress

from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from src.core.page_actions import PageActions
from src.core.settings import get_settings
from src.page_objects.cofee.login_po import LoginPo


class LoginActions(PageActions):
    """Business logic for phone + OTP login."""

    def __init__(self, driver: WebDriver) -> None:
        self._login_po = LoginPo(driver)
        super().__init__(driver, self._login_po)

    def dismiss_notification_permission_if_visible(self) -> None:
        """Tap Allow on the system notification permission dialog when shown."""
        try:
            allow = self._wait(5).until(lambda _: self._login_po.find_permission_allow_button())
            self.tap(allow)
            self.wait_for_element_gone(self._login_po.loc_permission_allow(), timeout=3)
        except TimeoutException:
            pass

    def dismiss_phone_hint_sheet_if_visible(self) -> None:
        """Dismiss the Google Play Services phone-number-hint bottom sheet if shown.

        This is a separate system window (com.google.android.gms) that appears
        automatically the instant the phone EditText gains focus, fully covering
        the screen including wherever "Next" would render. Left unhandled, waits
        for `loc_btn_next` time out with no useful error.
        """
        try:
            cancel = self._wait(3).until(lambda _: self._login_po.find_gms_phone_hint_cancel())
            self.tap(cancel)
            self.wait_for_element_gone(self._login_po.loc_gms_phone_hint_cancel(), timeout=3)
        except TimeoutException:
            pass

    def _advance_onboarding_carousel(self) -> None:
        """Tap the onboarding next arrow (no stable content-desc on early slides)."""
        size = self._driver.get_window_size()
        self._driver.execute_script(
            "mobile: clickGesture",
            {
                "x": int(size["width"] * 0.87),
                "y": int(size["height"] * 0.70),
            },
        )

    def _relaunch_app_if_on_launcher(self) -> None:
        """Bring CoFee back if a tap/reset left us on the Android home screen."""
        settings = get_settings()
        package = settings.app_package
        activity = settings.app_activity
        if not package:
            return
        try:
            current = self._driver.current_package or ""
        except Exception:
            current = ""
        if current == package:
            return
        if activity:
            subprocess.run(
                ["adb", "shell", "am", "start", "-W", "-n", f"{package}/{activity}"],
                check=False,
                capture_output=True,
            )
        with suppress(Exception):
            self._driver.activate_app(package)

    def navigate_to_phone_entry_screen(self, max_taps: int = 8) -> None:
        """Advance onboarding carousel until the phone number screen is visible."""
        self._relaunch_app_if_on_launcher()
        self.dismiss_notification_permission_if_visible()
        if self.is_phone_screen_visible(timeout=3):
            return
        for _ in range(max_taps):
            self._relaunch_app_if_on_launcher()
            self._advance_onboarding_carousel()
            self.dismiss_notification_permission_if_visible()
            if self.is_phone_screen_visible(timeout=1.5):
                return
        raise TimeoutException("Phone entry screen not reached after onboarding")

    def is_phone_screen_visible(self, timeout: float | None = None) -> bool:
        """Return True when phone number entry screen is displayed."""
        try:
            self.wait_for_element_visible(self._login_po.loc_phone_title(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_otp_screen_visible(self, timeout: float | None = None) -> bool:
        """Return True when OTP verification screen is displayed."""
        try:
            self.wait_for_element_visible(self._login_po.loc_otp_title(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_home_screen_visible(self, timeout: float | None = None) -> bool:
        """Return True when home tab is visible after successful login."""
        try:
            self.wait_for_element_visible(self._login_po.loc_tab_home(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def enter_phone_number(self, mobile: str) -> None:
        """Enter mobile number with digit-by-digit input (reliable on Flutter).

        Deliberately does not call `hide_keyboard()`: on this build the
        driver's hideKeyboard command falls back to a BACK press even when
        `is_keyboard_shown()` reports true, and BACK exits the app entirely
        from this root screen (no back stack). "Next" is fully visible and
        tappable with the keyboard still up, so hiding it isn't needed.
        """
        field = self.wait_for_element_visible(self._login_po.loc_phone_input(), timeout=10)
        self.tap(field)
        self.dismiss_phone_hint_sheet_if_visible()
        self._type_digits_with_verification(mobile)

    def _type_digits_with_verification(self, value: str, whole_entry_retries: int = 3) -> None:
        """Type a digit string, verifying the final result and retrying the whole entry on mismatch.

        Per-digit retry (`_send_digit_verified`) handles most dropped
        keystrokes, but on this build a stale/miscounted read can still let a
        digit slip through silently (confirmed by comparing the final result
        against the intended value, not just incremental length). Comparing
        the full digit-only result against ground truth and retyping from
        scratch on mismatch is more robust than trusting any single
        incremental heuristic.
        """
        for _ in range(whole_entry_retries):
            field = self.wait_for_element_visible(self._login_po.loc_phone_input(), timeout=5)
            field.clear()
            for i, digit in enumerate(value, start=1):
                self._send_digit_verified(digit, expected_length=i)
            actual = "".join(c for c in self._read_text_safe() if c.isdigit())
            if actual == value:
                return

    def _read_text_safe(self, retries: int = 3) -> str:
        """Read the shared input field's text, refetching on stale-element races."""
        for _ in range(retries):
            field = self.wait_for_element_visible(self._login_po.loc_phone_input(), timeout=5)
            try:
                return self.get_text(field)
            except StaleElementReferenceException:
                continue
        return ""

    def _send_digit_verified(self, digit: str, expected_length: int, retries: int = 4) -> None:
        """Send one digit into the shared input field, retrying on dropped keystrokes.

        Uses `adb shell input text` rather than Appium's `send_keys()`: on
        this Flutter EditText, `send_keys()` intermittently drops keystrokes
        or even truncates already-entered characters under device load (
        confirmed by direct comparison — the same sequence typed via adb was
        100% reliable). Still verify + retry as a safety net.

        Counts digits only, not raw text length: the phone field auto-inserts
        a formatting space after 5 digits (e.g. "63210 20200"), which would
        otherwise inflate the length and make this return one digit early,
        silently dropping the next real digit.
        """
        for _ in range(retries):
            digit_count = sum(c.isdigit() for c in self._read_text_safe())
            if digit_count >= expected_length:
                return
            subprocess.run(
                ["adb", "shell", "input", "text", digit],
                check=False,
                capture_output=True,
            )
            time.sleep(0.15)

    def _tap_primary_cta(self, element) -> None:
        """Tap left-center of bottom CTA — right side overlaps the debug FAB."""
        loc = element.location
        size = element.size
        self._driver.execute_script(
            "mobile: clickGesture",
            {
                "x": int(loc["x"] + size["width"] * 0.35),
                "y": int(loc["y"] + size["height"] / 2),
            },
        )

    def submit_phone_number(self) -> None:
        """Tap Next to request OTP (avoid debug FAB on the right)."""
        self.dismiss_phone_hint_sheet_if_visible()
        next_btn = self.wait_for_element_visible(self._login_po.loc_btn_next(), timeout=12)
        self._tap_primary_cta(next_btn)

    def enter_otp(self, otp: str) -> None:
        """Enter OTP code on the verification screen.

        See `enter_phone_number` — `hide_keyboard()` is intentionally omitted
        for the same reason (BACK-press fallback exits the app on this build).
        """
        field = self.wait_for_element_visible(self._login_po.loc_phone_input(), timeout=10)
        self.tap(field)
        self._type_digits_with_verification(otp)

    def submit_otp(self) -> None:
        """Tap Next to verify OTP when still on the OTP screen."""
        with suppress(Exception):
            self._tap_primary_cta(self._login_po.find_btn_next())

    def is_account_picker_visible(self, timeout: float | None = None) -> bool:
        """Return True when post-OTP account selection is shown."""
        try:
            self.wait_for_element_visible(self._login_po.loc_account_welcome(), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def dismiss_debug_overlay_if_visible(self) -> None:
        """Close the Flutter network-logs overlay if the Back control is shown."""
        with suppress(Exception):
            back = self._wait(1).until(lambda _: self._login_po.find_debug_back())
            self.tap(back)

    def select_account_and_continue(self) -> None:
        """Select Individual account and tap Continue (avoid debug FAB on the right)."""
        self.dismiss_debug_overlay_if_visible()
        with suppress(Exception):
            self.tap(self._login_po.find_account_individual())
        continue_el = self.wait_for_element_visible(self._login_po.loc_btn_continue(), timeout=20)
        loc = continue_el.location
        size = continue_el.size
        self._driver.execute_script(
            "mobile: clickGesture",
            {
                "x": int(loc["x"] + size["width"] * 0.35),
                "y": int(loc["y"] + size["height"] / 2),
            },
        )

    def complete_otp_and_reach_home(self, otp: str) -> None:
        """Enter OTP, handle optional account picker, wait for home."""
        self.enter_otp(otp)
        self.submit_otp()
        if self.is_account_picker_visible(timeout=20):
            self.select_account_and_continue()
            self.dismiss_debug_overlay_if_visible()
            if self.is_home_screen_visible(timeout=45):
                return
        # Network blip: still on OTP — resubmit once
        if self.is_otp_screen_visible(timeout=2):
            self.enter_otp(otp)
            self.submit_otp()
            if self.is_account_picker_visible(timeout=20):
                self.select_account_and_continue()
            self.dismiss_debug_overlay_if_visible()
        if not self.is_home_screen_visible(timeout=45):
            raise TimeoutException("Home screen not reached after OTP / account selection")
