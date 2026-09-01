"""Platform-aware device operations (Android emulator and iOS Simulator).

Login/reset/taps must not call bare ``adb`` — Android uses ANDROID_HOME adb when
needed; iOS uses Appium XCUITest (no adb).
"""

from __future__ import annotations

import os
import subprocess
import time
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.settings import Settings, get_settings

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


def _adb_bin() -> str:
    """Resolve adb from ANDROID_HOME, then PATH."""
    home = os.environ.get("ANDROID_HOME") or str(Path.home() / "Android" / "Sdk")
    candidate = Path(home) / "platform-tools" / "adb"
    if candidate.is_file():
        return str(candidate)
    return "adb"


class DeviceHelper:
    """Clear / launch / tap / type using the current PLATFORM."""

    def __init__(self, driver: WebDriver, settings: Settings | None = None) -> None:
        self._driver = driver
        self._settings = settings or get_settings()

    @property
    def app_id(self) -> str:
        """Android package or iOS bundle id."""
        cfg = self._settings
        app_id = cfg.bundle_id if cfg.is_ios else cfg.app_package
        if not app_id:
            raise ValueError(
                "BUNDLE_ID is required on iOS" if cfg.is_ios else "APP_PACKAGE is required on Android"
            )
        return app_id

    def activate_app(self) -> None:
        with suppress(Exception):
            self._driver.activate_app(self.app_id)

    def terminate_app(self) -> None:
        with suppress(Exception):
            self._driver.terminate_app(self.app_id)

    def clear_and_relaunch(self) -> None:
        """Reset app data and bring the app to the foreground (fresh login)."""
        if self._settings.is_ios:
            self._clear_and_relaunch_ios()
        else:
            self._clear_and_relaunch_android()

    def _clear_and_relaunch_android(self) -> None:
        package = self.app_id
        activity = self._settings.app_activity
        self.terminate_app()
        subprocess.run(
            [_adb_bin(), "shell", "pm", "clear", package],
            check=False,
            capture_output=True,
        )
        if activity:
            subprocess.run(
                [_adb_bin(), "shell", "am", "start", "-W", "-n", f"{package}/{activity}"],
                check=False,
                capture_output=True,
            )
        self.activate_app()

    def _clear_and_relaunch_ios(self) -> None:
        bundle = self.app_id
        self.terminate_app()
        with suppress(Exception):
            self._driver.execute_script("mobile: clearApp", {"bundleId": bundle})
        app_path = self._settings.app_path
        if app_path:
            resolved = Path(app_path)
            if not resolved.is_absolute():
                from src.core.settings import REPO_ROOT

                resolved = REPO_ROOT / app_path
            if resolved.exists():
                with suppress(Exception):
                    self._driver.remove_app(bundle)
                with suppress(Exception):
                    self._driver.install_app(str(resolved.resolve()))
        self.activate_app()
        time.sleep(1)

    def launch_if_not_foreground(self) -> None:
        """Bring the app back if a tap left the launcher / SpringBoard."""
        if self._settings.is_ios:
            self.activate_app()
            return
        try:
            current = self._driver.current_package or ""
        except Exception:
            current = ""
        if current == self.app_id:
            return
        activity = self._settings.app_activity
        if activity:
            subprocess.run(
                [_adb_bin(), "shell", "am", "start", "-W", "-n", f"{self.app_id}/{activity}"],
                check=False,
                capture_output=True,
            )
        self.activate_app()

    def tap_at(self, x: int, y: int) -> None:
        """Tap a screen coordinate (Android UiAutomator2 or iOS XCUITest)."""
        if self._settings.is_ios:
            self._driver.execute_script("mobile: tap", {"x": x, "y": y})
            return
        self._driver.execute_script("mobile: clickGesture", {"x": x, "y": y})

    def tap_element(self, element: WebElement, x_ratio: float = 0.5, y_ratio: float = 0.5) -> None:
        """Tap a point inside an element (left-biased CTAs use x_ratio < 0.5)."""
        loc = element.location
        size = element.size
        x = int(loc["x"] + size["width"] * x_ratio)
        y = int(loc["y"] + size["height"] * y_ratio)
        if self._settings.is_android:
            # Flutter Android: adb tap is more reliable than Appium click/gesture
            subprocess.run(
                [_adb_bin(), "shell", "input", "tap", str(x), str(y)],
                check=False,
                capture_output=True,
            )
            return
        self.tap_at(x, y)

    def type_chars(self, text: str, pause_s: float = 0.15) -> None:
        """Type characters without focusing a field (Android adb; iOS send_keys fallback)."""
        if self._settings.is_android:
            for char in text:
                subprocess.run(
                    [_adb_bin(), "shell", "input", "text", char],
                    check=False,
                    capture_output=True,
                )
                time.sleep(pause_s)
            return
        # iOS Simulator: no adb — caller should prefer element.send_keys
        with suppress(Exception):
            self._driver.switch_to.active_element.send_keys(text)


def get_device_helper(driver: Any, settings: Settings | None = None) -> DeviceHelper:
    return DeviceHelper(driver, settings)
