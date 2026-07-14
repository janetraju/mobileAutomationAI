"""W3C Appium capabilities built from settings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.core.settings import REPO_ROOT, Settings, get_settings


def _resolve_app_path(app_path: str | None) -> str | None:
    """Return absolute path for APK/IPA when a relative path is configured."""
    if not app_path:
        return None
    path = Path(app_path)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return str(path.resolve())


def build_capabilities(
    settings: Settings | None = None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build W3C Appium capabilities from resolved settings."""
    cfg = settings or get_settings()
    caps: dict[str, Any] = {
        "platformName": cfg.platform.capitalize(),
        "appium:deviceName": cfg.device_name,
        "appium:platformVersion": cfg.platform_version,
        "appium:newCommandTimeout": cfg.new_command_timeout,
        "appium:noReset": cfg.no_reset,
        "appium:fullReset": cfg.full_reset,
        "appium:autoGrantPermissions": cfg.auto_grant_permissions,
        "appium:adbExecTimeout": 120000,
    }

    if cfg.udid:
        caps["appium:udid"] = cfg.udid

    if cfg.is_android:
        caps["appium:automationName"] = "UiAutomator2"
        caps["appium:settings[waitForIdleTimeout]"] = cfg.android_idle_timeout
        resolved_app = _resolve_app_path(cfg.app_path)
        if resolved_app:
            caps["appium:app"] = resolved_app
        if cfg.app_package:
            caps["appium:appPackage"] = cfg.app_package
        if cfg.app_activity:
            caps["appium:appActivity"] = cfg.app_activity
    else:
        caps["appium:automationName"] = "XCUITest"
        resolved_app = _resolve_app_path(cfg.app_path)
        if resolved_app:
            caps["appium:app"] = resolved_app
        elif cfg.bundle_id:
            caps["appium:bundleId"] = cfg.bundle_id

    if cfg.record_video:
        caps["appium:recordVideo"] = True

    if overrides:
        caps.update(overrides)

    return caps
