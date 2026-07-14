"""Appium session lifecycle — one driver per credential profile."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from src.core.capabilities import build_capabilities
from src.core.session_state import SessionState
from src.core.settings import Settings, get_settings

if TYPE_CHECKING:
    pass


class SessionManager:
    """Singleton manager for Appium WebDriver sessions keyed by profile name."""

    _instance: SessionManager | None = None
    _sessions: dict[str, WebDriver]

    def __new__(cls) -> SessionManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._sessions = {}
        return cls._instance

    def get_driver(
        self,
        profile: str = "default",
        settings: Settings | None = None,
        capability_overrides: dict[str, Any] | None = None,
    ) -> WebDriver:
        """Return existing or create new Appium session for profile."""
        if profile in self._sessions:
            return self._sessions[profile]

        cfg = settings or get_settings()
        caps = build_capabilities(cfg, overrides=capability_overrides)
        driver = AppiumWebDriver(cfg.appium_url, options=_caps_to_options(caps))
        self._sessions[profile] = driver
        SessionState.set_active(profile, driver)
        return driver

    def quit(self, profile: str | None = None) -> None:
        """Quit one or all sessions."""
        if profile:
            driver = self._sessions.pop(profile, None)
            if driver:
                driver.quit()
            SessionState.clear(profile)
            return

        for name, driver in list(self._sessions.items()):
            driver.quit()
            SessionState.clear(name)
        self._sessions.clear()

    def quit_all(self) -> None:
        """Quit all active sessions."""
        self.quit()


def _caps_to_options(caps: dict[str, Any]) -> Any:
    """Convert flat W3C caps dict to platform-specific Appium Options."""
    platform = str(caps.get("platformName", "")).lower()
    if platform == "ios":
        from appium.options.ios import XCUITestOptions

        options = XCUITestOptions()
    else:
        from appium.options.android import UiAutomator2Options

        options = UiAutomator2Options()
    options.load_capabilities(caps)
    return options


def get_session_manager() -> SessionManager:
    """Return the singleton SessionManager."""
    return SessionManager()
