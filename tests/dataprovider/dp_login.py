"""Login test data for CoFee."""

from __future__ import annotations

import pytest

from src.core.settings import get_settings


def get_login_test_data() -> list:
    """Return parametrized login credentials from environment settings."""
    settings = get_settings()
    if not settings.test_mobile or not settings.test_otp:
        raise ValueError("TEST_MOBILE and TEST_OTP must be set in .env for login tests")
    return [
        pytest.param(
            settings.test_mobile,
            settings.test_otp,
            id="cofee_dev_user",
        )
    ]
