"""HTTP client for test-data setup and backend assertions."""

from __future__ import annotations

from typing import Any

import httpx

from src.core.settings import Settings, get_settings


class ApiClient:
    """Sync httpx client scoped to API_BASE_URL from settings."""

    def __init__(self, settings: Settings | None = None) -> None:
        cfg = settings or get_settings()
        if not cfg.api_base_url:
            raise ValueError("API_BASE_URL is not configured")
        self._settings = cfg
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if cfg.api_auth_token:
            headers["Authorization"] = f"Bearer {cfg.api_auth_token}"
        self._client = httpx.Client(
            base_url=cfg.api_base_url.rstrip("/"),
            headers=headers,
            timeout=30.0,
        )

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        """HTTP GET."""
        return self._client.get(path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        """HTTP POST."""
        return self._client.post(path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> httpx.Response:
        """HTTP PUT."""
        return self._client.put(path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        """HTTP DELETE."""
        return self._client.delete(path, **kwargs)

    def close(self) -> None:
        """Close the underlying client."""
        self._client.close()

    def __enter__(self) -> ApiClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


def generate_otp(mobile: str, settings: Settings | None = None) -> httpx.Response:
    """Request OTP for a mobile number via configured OTP_GENERATE_PATH."""
    cfg = settings or get_settings()
    path = cfg.otp_generate_path or "/auth/generate-otp"
    with ApiClient(cfg) as client:
        return client.post(path, json={"mobile": mobile})


def validate_otp(mobile: str, otp: str, settings: Settings | None = None) -> httpx.Response:
    """Validate OTP via configured OTP_VALIDATE_PATH."""
    cfg = settings or get_settings()
    path = cfg.otp_validate_path or "/auth/validate-otp"
    with ApiClient(cfg) as client:
        return client.post(path, json={"mobile": mobile, "otp": otp})
