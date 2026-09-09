"""Central config: python-dotenv + Pydantic. No app-specific imports.

Load order: `.env` first, then `.env.<APP_ENV>` on top (later values win) so
per-environment overrides (dev/stg/uat) never require duplicating the whole
file. Neither is committed — see `.env.example` / `.env.<env>.example`.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_env_files() -> None:
    load_dotenv(REPO_ROOT / ".env", override=False)
    app_env = os.environ.get("APP_ENV")
    if app_env:
        load_dotenv(REPO_ROOT / f".env.{app_env}", override=True)


_load_env_files()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True)

    # --- App identity ---
    app_name: str = Field(default="", alias="APP_NAME")
    app_slug: str = Field(default="", alias="APP_SLUG")
    app_type: str = Field(default="native", alias="APP_TYPE")  # native | flutter | rn | hybrid
    app_env: str = Field(default="dev", alias="APP_ENV")

    # --- Platform / Appium ---
    platform: str = Field(default="android", alias="PLATFORM")  # android | ios
    appium_host: str = Field(default="127.0.0.1", alias="APPIUM_HOST")
    appium_port: int = Field(default=4723, alias="APPIUM_PORT")
    device_name: str = Field(default="", alias="DEVICE_NAME")
    avd_name: str = Field(default="", alias="AVD_NAME")
    platform_version: str = Field(default="", alias="PLATFORM_VERSION")
    udid: str | None = Field(default=None, alias="UDID")

    # --- App install target ---
    app_path: str | None = Field(default=None, alias="APP_PATH")
    app_package: str | None = Field(default=None, alias="APP_PACKAGE")
    app_activity: str | None = Field(default=None, alias="APP_ACTIVITY")
    bundle_id: str | None = Field(default=None, alias="BUNDLE_ID")

    # --- Backend ---
    api_base_url: str = Field(default="", alias="API_BASE_URL")

    # --- Reset behaviour ---
    no_reset: bool = Field(default=True, alias="NO_RESET")
    full_reset: bool = Field(default=False, alias="FULL_RESET")

    # --- Waits ---
    explicit_wait_timeout: int = Field(default=15, alias="EXPLICIT_WAIT_TIMEOUT")

    # --- Credentials / test data (never hardcode elsewhere) ---
    test_mobile: str | None = Field(default=None, alias="TEST_MOBILE")
    test_otp: str | None = Field(default=None, alias="TEST_OTP")
    default_username: str | None = Field(default=None, alias="DEFAULT_USERNAME")
    default_password: str | None = Field(default=None, alias="DEFAULT_PASSWORD")
    feature_org_id: str | None = Field(default=None, alias="FEATURE_ORG_ID")
    feature_account_id: str | None = Field(default=None, alias="FEATURE_ACCOUNT_ID")

    # --- Debug / MCP ---
    no_ui: bool = Field(default=False, alias="NO_UI")

    @property
    def is_android(self) -> bool:
        return self.platform.lower() == "android"

    @property
    def is_ios(self) -> bool:
        return self.platform.lower() == "ios"

    @property
    def app_path_resolved(self) -> Path | None:
        if not self.app_path:
            return None
        p = Path(self.app_path)
        return p if p.is_absolute() else REPO_ROOT / p


@lru_cache
def get_settings() -> Settings:
    return Settings()
