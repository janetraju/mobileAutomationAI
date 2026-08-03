"""Pydantic settings and environment resolution for the mobile automation framework."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]
ENVIRONMENT_DIR = REPO_ROOT / "environment"

# CLI / alias mapping for environment names (e.g. uat1 → uat01)
ENV_ALIASES: dict[str, str] = {
    "uat1": "uat01",
    "uat2": "uat02",
    "stg1": "stg01",
}

Platform = Literal["android", "ios"]
AppEnv = Literal["dev", "stg", "uat", "prod"]
AppType = Literal["native", "flutter", "rn", "hybrid"]


def _resolve_env_name(raw: str) -> str:
    """Normalize environment name via alias map."""
    normalized = raw.strip().lower()
    return ENV_ALIASES.get(normalized, normalized)


def _load_env_files(app_env: str) -> None:
    """Load .env then environment-specific overrides."""
    load_dotenv(REPO_ROOT / ".env", override=False)
    env_file = REPO_ROOT / f".env.{app_env}"
    if env_file.exists():
        load_dotenv(env_file, override=True)
    props = ENVIRONMENT_DIR / f"{app_env}.properties"
    if props.exists():
        load_dotenv(props, override=True)


# Per-app registry — get-context Phase 0 updates this when adding a new app
APP_REGISTRY: dict[str, dict[str, dict[str, dict[str, str]]]] = {
    "cofee": {
        "android": {
            "dev": {
                "app_package": "cofee.life.app.dev",
                "app_activity": "cofee.life.app.MainActivity",
                "api_base_url": "https://api.dev.cofee.life",
            },
            "stg": {
                "app_package": "cofee.life.app.stg",
                "app_activity": "cofee.life.app.MainActivity",
                "api_base_url": "https://api.stg.cofee.life",
            },
            "uat": {
                "app_package": "cofee.life.app.uat",
                "app_activity": "cofee.life.app.MainActivity",
                "api_base_url": "https://api.uat.cofee.life",
            },
            "prod": {
                "app_package": "cofee.life.app",
                "app_activity": "cofee.life.app.MainActivity",
                "api_base_url": "https://api.cofee.life",
            },
        },
        "ios": {
            "dev": {
                "bundle_id": "cofee.life.app.dev",
                "api_base_url": "https://api.dev.cofee.life",
            },
            "stg": {
                "bundle_id": "cofee.life.app.stg",
                "api_base_url": "https://api.stg.cofee.life",
            },
            "uat": {
                "bundle_id": "cofee.life.app.uat",
                "api_base_url": "https://api.uat.cofee.life",
            },
            "prod": {"bundle_id": "cofee.life.app", "api_base_url": "https://api.cofee.life"},
        },
    },
}


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(alias="APP_NAME", default="[APP NAME]")
    app_slug: str = Field(alias="APP_SLUG", default="app_slug")
    app_type: AppType = Field(alias="APP_TYPE", default="native")
    app_env: AppEnv = Field(alias="APP_ENV", default="dev")
    platform: Platform = Field(alias="PLATFORM", default="android")

    appium_host: str = Field(alias="APPIUM_HOST", default="127.0.0.1")
    appium_port: int = Field(alias="APPIUM_PORT", default=4723)
    appium_path: str = Field(alias="APPIUM_PATH", default="/")

    device_name: str = Field(alias="DEVICE_NAME", default="emulator-5554")
    platform_version: str = Field(alias="PLATFORM_VERSION", default="14")
    udid: str | None = Field(alias="UDID", default=None)

    app_path: str | None = Field(alias="APP_PATH", default=None)
    no_reset: bool = Field(alias="NO_RESET", default=True)
    full_reset: bool = Field(alias="FULL_RESET", default=False)
    auto_grant_permissions: bool = Field(alias="AUTO_GRANT_PERMISSIONS", default=True)
    new_command_timeout: int = Field(alias="NEW_COMMAND_TIMEOUT", default=300)
    android_idle_timeout: int = Field(alias="ANDROID_IDLE_TIMEOUT", default=1000)

    default_username: str | None = Field(alias="DEFAULT_USERNAME", default=None)
    default_password: str | None = Field(alias="DEFAULT_PASSWORD", default=None)

    api_base_url: str | None = Field(alias="API_BASE_URL", default=None)
    test_mobile: str | None = Field(alias="TEST_MOBILE", default=None)
    test_otp: str | None = Field(alias="TEST_OTP", default=None)
    app_package: str | None = Field(alias="APP_PACKAGE", default=None)
    app_activity: str | None = Field(alias="APP_ACTIVITY", default=None)
    bundle_id: str | None = Field(alias="BUNDLE_ID", default=None)

    record_video: bool = Field(alias="RECORD_VIDEO", default=False)
    headless_emulator: bool = Field(alias="HEADLESS_EMULATOR", default=False)

    feature_org_id: str | None = Field(alias="FEATURE_ORG_ID", default=None)
    feature_account_id: str | None = Field(alias="FEATURE_ACCOUNT_ID", default=None)

    db_host: str | None = Field(alias="DB_HOST", default=None)
    db_port: int = Field(alias="DB_PORT", default=5432)
    db_name: str | None = Field(alias="DB_NAME", default=None)
    db_user: str | None = Field(alias="DB_USER", default=None)
    db_password: str | None = Field(alias="DB_PASSWORD", default=None)

    explicit_wait_timeout: int = Field(alias="EXPLICIT_WAIT_TIMEOUT", default=20)
    poll_frequency: float = Field(alias="POLL_FREQUENCY", default=0.5)

    @field_validator("app_env", mode="before")
    @classmethod
    def normalize_env(cls, value: Any) -> str:
        if value is None:
            return "dev"
        return _resolve_env_name(str(value))

    @model_validator(mode="after")
    def apply_env_maps(self) -> Settings:
        """Derive app identifiers and API URL from APP_REGISTRY when not explicitly set."""
        env = self.app_env
        app_config = APP_REGISTRY.get(self.app_slug, {})
        platform_config = app_config.get(self.platform, {})
        env_map = platform_config.get(env, {})

        if self.platform == "android":
            if not self.app_package:
                self.app_package = env_map.get("app_package")
            if not self.app_activity:
                self.app_activity = env_map.get("app_activity")
        elif not self.bundle_id:
            self.bundle_id = env_map.get("bundle_id")

        if not self.api_base_url:
            self.api_base_url = env_map.get("api_base_url")
        return self

    @property
    def is_flutter(self) -> bool:
        return self.app_type == "flutter"

    @property
    def appium_url(self) -> str:
        """Full Appium server URL (Appium 2 base path is `/`)."""
        base = f"http://{self.appium_host}:{self.appium_port}"
        path = (self.appium_path or "/").strip()
        if path in {"", "/"}:
            return base
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{base}{path.rstrip('/')}"

    @property
    def is_android(self) -> bool:
        return self.platform == "android"

    @property
    def is_ios(self) -> bool:
        return self.platform == "ios"


def _validate_required(settings: Settings) -> None:
    """Fail fast when required configuration is missing."""
    missing: list[str] = []
    if not settings.app_name or settings.app_name == "[APP NAME]":
        missing.append("APP_NAME")
    if not settings.app_slug or settings.app_slug == "[APP_SLUG]":
        missing.append("APP_SLUG")
    if settings.platform == "android":
        if not settings.app_path and not settings.app_package:
            missing.append("APP_PATH or APP_PACKAGE")
        if not settings.app_path and not settings.app_activity:
            missing.append("APP_ACTIVITY (when APP_PATH is unset)")
    elif settings.platform == "ios":
        if not settings.app_path and not settings.bundle_id:
            missing.append("APP_PATH or BUNDLE_ID")
    if missing:
        raise ValueError(
            f"Missing or placeholder required settings: {', '.join(missing)}. "
            "Copy .env.example to .env and set values for [APP NAME]."
        )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings singleton. Loads dotenv on first call."""
    raw_env = os.getenv("APP_ENV", "dev")
    resolved = _resolve_env_name(raw_env)
    _load_env_files(resolved)
    os.environ.setdefault("APP_ENV", resolved)
    settings = Settings()
    _validate_required(settings)
    return settings


def reset_settings_cache() -> None:
    """Clear settings cache (useful in tests)."""
    get_settings.cache_clear()
