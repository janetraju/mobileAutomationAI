"""Framework fixtures every test/step/page-action layer relies on:
`driver`, `settings`, `mobile`, `otp`. Also owns Allure failure attachments
(screenshot + page source) so no individual test needs its own screenshot
code, and the collection-time fail-fast check for OTP-marked tests missing
`TEST_MOBILE`.
"""

from __future__ import annotations

import allure
import pytest

from src.core.driver_factory import build_driver
from src.core.settings import Settings, get_settings


def pytest_collection_modifyitems(config, items):
    """Fail fast if TEST_MOBILE is missing for any collected test that
    exercises mobile+OTP login, rather than failing deep inside the test."""
    settings = get_settings()
    if settings.test_mobile:
        return

    otp_dependent = [
        item
        for item in items
        if "otp" in item.fixturenames or item.get_closest_marker("manual_otp")
    ]
    if otp_dependent:
        names = ", ".join(item.nodeid for item in otp_dependent)
        raise pytest.UsageError(
            "TEST_MOBILE is not set in .env, but these collected tests need "
            f"mobile+OTP login: {names}"
        )


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture
def driver(settings: Settings):
    drv = build_driver(settings)
    yield drv
    drv.quit()


@pytest.fixture
def mobile(settings: Settings) -> str:
    """The test mobile number for OTP-based login flows."""
    if not settings.test_mobile:
        pytest.fail("TEST_MOBILE is not set in .env — required for OTP login tests")
    return settings.test_mobile


@pytest.fixture
def otp(settings: Settings) -> str:
    """The fixed dev OTP for OTP-based login flows (never used in stg/uat CI)."""
    if not settings.test_otp:
        pytest.fail("TEST_OTP is not set in .env — required for OTP login tests")
    return settings.test_otp


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    drv = item.funcargs.get("driver")
    if drv is None:
        return

    try:
        allure.attach(
            drv.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    try:
        allure.attach(
            drv.page_source,
            name="page_source",
            attachment_type=allure.attachment_type.XML,
        )
    except Exception:
        pass
