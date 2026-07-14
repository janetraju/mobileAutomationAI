"""Tracks active Appium session and credential profile for current test context."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver


class SessionState:
    """Module-level state for resolving the current user/driver without threading."""

    _active_profile: str | None = None
    _drivers: dict[str, WebDriver] = {}
    _logged_in_profiles: set[str] = set()

    @classmethod
    def set_active(cls, profile: str, driver: WebDriver) -> None:
        cls._active_profile = profile
        cls._drivers[profile] = driver

    @classmethod
    def get_active_profile(cls) -> str | None:
        return cls._active_profile

    @classmethod
    def get_driver(cls, profile: str | None = None) -> WebDriver | None:
        key = profile or cls._active_profile
        if key is None:
            return None
        return cls._drivers.get(key)

    @classmethod
    def mark_logged_in(cls, profile: str | None = None) -> None:
        """Record that the given profile completed login in the current session."""
        key = profile or cls._active_profile or "default"
        cls._logged_in_profiles.add(key)

    @classmethod
    def is_logged_in(cls, profile: str | None = None) -> bool:
        """Return True when login was completed for this profile in the session."""
        key = profile or cls._active_profile or "default"
        return key in cls._logged_in_profiles

    @classmethod
    def clear(cls, profile: str | None = None) -> None:
        if profile:
            cls._drivers.pop(profile, None)
            cls._logged_in_profiles.discard(profile)
            if cls._active_profile == profile:
                cls._active_profile = None
            return
        cls._active_profile = None
        cls._drivers.clear()
        cls._logged_in_profiles.clear()
