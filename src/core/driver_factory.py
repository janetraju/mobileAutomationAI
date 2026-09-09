"""Builds Appium capabilities from `Settings` and starts/stops a session.

Sync `appium.webdriver.webdriver.WebDriver` only — no async Appium clients.
"""

from __future__ import annotations

from appium import webdriver
from appium.options.common import AppiumOptions

from src.core.settings import Settings


def build_capabilities(settings: Settings) -> dict:
    caps: dict = {
        "platformName": "Android" if settings.is_android else "iOS",
        "appium:deviceName": settings.device_name,
        "appium:noReset": settings.no_reset,
        "appium:fullReset": settings.full_reset,
        "appium:newCommandTimeout": 120,
    }

    if settings.platform_version:
        caps["appium:platformVersion"] = settings.platform_version
    if settings.udid:
        caps["appium:udid"] = settings.udid

    if settings.is_android:
        caps["appium:automationName"] = "UiAutomator2"
        # noReset keeps the app's login session (see docs/cofee-flow.md ->
        # Known blockers / Test data), but on its own it also *resumes*
        # whatever screen the app process was last on instead of cold
        # launching. forceAppLaunch restarts the process fresh each session
        # -- still logged in, but always starting from a known screen.
        caps["appium:forceAppLaunch"] = True
        caps["appium:shouldTerminateApp"] = True
        app_path = settings.app_path_resolved
        if app_path is not None:
            caps["appium:app"] = str(app_path)
        elif settings.app_package and settings.app_activity:
            caps["appium:appPackage"] = settings.app_package
            caps["appium:appActivity"] = settings.app_activity
        else:
            raise ValueError(
                "Set either APP_PATH (to install) or APP_PACKAGE + APP_ACTIVITY "
                "(to target an already-installed build) in .env"
            )
    else:
        caps["appium:automationName"] = "XCUITest"
        app_path = settings.app_path_resolved
        if app_path is not None:
            caps["appium:app"] = str(app_path)
        elif settings.bundle_id:
            caps["appium:bundleId"] = settings.bundle_id
        else:
            raise ValueError("Set either APP_PATH or BUNDLE_ID (iOS) in .env")

    return caps


def build_driver(settings: Settings) -> webdriver.Remote:
    server_url = f"http://{settings.appium_host}:{settings.appium_port}"
    options = AppiumOptions().load_capabilities(build_capabilities(settings))
    return webdriver.Remote(command_executor=server_url, options=options)
