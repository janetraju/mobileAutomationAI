"""Pytest fixtures, CLI options, and hooks for mobile UI automation."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import allure
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tests"))

from src.core.device_pool import apply_device_pool_for_worker
from src.core.session_manager import get_session_manager
from src.core.settings import get_settings, reset_settings_cache


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register CLI options for environment and device overrides."""
    parser.addoption(
        "--env", action="store", default=None, help="Target environment (dev|stg|uat|prod)"
    )
    parser.addoption(
        "--platform", action="store", default=None, help="Platform override (android|ios)"
    )
    parser.addoption("--device", action="store", default=None, help="Device name / UDID override")
    parser.addoption(
        "--headless-emulator",
        action="store_true",
        default=False,
        help="Run Android emulator headless",
    )
    parser.addoption(
        "--record-video",
        action="store_true",
        default=False,
        help="Record session video via Appium",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Register markers and bind this xdist worker to its own device."""
    config.addinivalue_line("markers", "e2e: End-to-end UI tests")
    config.addinivalue_line("markers", "p0: Priority 0 smoke tests")
    config.addinivalue_line("markers", "p1: Priority 1 tests")
    config.addinivalue_line("markers", "p2: Priority 2 tests")
    config.addinivalue_line("markers", "android: Android-only tests")
    config.addinivalue_line("markers", "ios: iOS-only tests")
    config.addinivalue_line("markers", "ignore: Excluded from default runs")
    config.addinivalue_line(
        "markers",
        'auth_profile(name): Credential profile for Appium session reuse (e.g. "default", "admin")',
    )
    config.addinivalue_line(
        "markers",
        "authenticated: Ensure logged-in home before the test (no login-order dependency)",
    )
    config.addinivalue_line(
        "markers",
        "fresh: Test owns a clean app (e.g. login); no auto login-from-session",
    )

    # Each xdist worker process must claim a unique device before Settings load.
    assignment = apply_device_pool_for_worker()
    if assignment is not None:
        reset_settings_cache()
        port_note = (
            f"appium=:{assignment.appium_port}"
            if assignment.appium_port is not None
            else "appium=shared"
        )
        extra = ""
        if assignment.android_system_port is not None:
            extra = f" systemPort={assignment.android_system_port}"
        print(
            f"[device-pool] {assignment.worker_id} → "
            f"{assignment.device_name} ({port_note}{extra})",
            flush=True,
        )


def _apply_cli_overrides(config: pytest.Config) -> None:
    """Apply CLI flags to environment before settings load."""
    if config.getoption("--env"):
        os.environ["APP_ENV"] = config.getoption("--env")
    if config.getoption("--platform"):
        os.environ["PLATFORM"] = config.getoption("--platform")
    # --device is for sequential runs only; under xdist, DEVICE_POOL owns assignment
    if config.getoption("--device") and not os.environ.get("PYTEST_XDIST_WORKER"):
        os.environ["DEVICE_NAME"] = config.getoption("--device")
    if config.getoption("--headless-emulator"):
        os.environ["HEADLESS_EMULATOR"] = "true"
    if config.getoption("--record-video"):
        os.environ["RECORD_VIDEO"] = "true"
    reset_settings_cache()


@pytest.fixture(scope="session", autouse=True)
def _configure_settings(request: pytest.FixtureRequest) -> None:
    """Apply CLI overrides once per session."""
    _apply_cli_overrides(request.config)


@pytest.fixture(scope="session")
def settings():
    """Session-scoped settings singleton."""
    return get_settings()


@pytest.fixture(scope="session")
def mobile(settings):
    """Test user mobile from environment."""
    if not settings.test_mobile:
        raise ValueError("TEST_MOBILE must be set in .env")
    return settings.test_mobile


@pytest.fixture(scope="session")
def otp(settings):
    """Test OTP from environment."""
    if not settings.test_otp:
        raise ValueError("TEST_OTP must be set in .env")
    return settings.test_otp


def _resolve_auth_profile(request: pytest.FixtureRequest) -> str:
    """Resolve auth_profile marker value for the current test."""
    marker = request.node.get_closest_marker("auth_profile")
    if marker and marker.args:
        return str(marker.args[0])
    return "default"


@pytest.fixture(scope="session")
def driver(request: pytest.FixtureRequest, settings):
    """Session-scoped Appium WebDriver via SessionManager."""
    profile = _resolve_auth_profile(request)
    manager = get_session_manager()
    drv = manager.get_driver(profile=profile, settings=settings)
    yield drv
    manager.quit_all()


@pytest.fixture(autouse=True)
def _explicit_wait_timeout(settings) -> None:
    """Ensure explicit wait timeout from settings is active per test."""
    _ = settings.explicit_wait_timeout


@pytest.fixture(autouse=True)
def _isolate_app_state(request: pytest.FixtureRequest):
    """Bring the app to a known state from markers — tests do not need login-first order.

    - ``authenticated``: login (or reuse on this device) until home is reachable
    - ``fresh``: leave setup to the test (login flows call pm clear themselves)
    """
    is_fresh = request.node.get_closest_marker("fresh") is not None
    is_authenticated = request.node.get_closest_marker("authenticated") is not None

    if is_fresh or not is_authenticated:
        yield
        return

    from src.steps.cofee.login_steps import user_ensures_logged_in_home

    driver = request.getfixturevalue("driver")
    mobile = request.getfixturevalue("mobile")
    otp = request.getfixturevalue("otp")
    user_ensures_logged_in_home(driver, mobile, otp)
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Attach diagnostics on test failure."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    driver_fixture = item.funcargs.get("driver")
    if driver_fixture is None:
        return

    try:
        png = driver_fixture.get_screenshot_as_png()
        allure.attach(
            png,
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    try:
        source = driver_fixture.page_source
        allure.attach(
            source,
            name="page_source",
            attachment_type=allure.attachment_type.XML,
        )
    except Exception:
        pass

    settings = get_settings()
    if settings.is_android:
        try:
            logcat = driver_fixture.get_log("logcat")
            log_text = "\n".join(entry.get("message", "") for entry in logcat[-200:])
            allure.attach(
                log_text,
                name="logcat",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception:
            pass


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip platform-mismatched and ignored tests.

    A test with both ``android`` and ``ios`` markers runs on either platform.
    A test with neither runs on both (e.g. unit tests).
    """
    settings = get_settings()
    platform = settings.platform
    skip_wrong_platform = pytest.mark.skip(reason=f"Not applicable on {platform}")
    skip_ignore = pytest.mark.skip(reason="Marked @pytest.mark.ignore")

    for item in items:
        if item.get_closest_marker("ignore"):
            item.add_marker(skip_ignore)
        names = {marker.name for marker in item.iter_markers()}
        has_android = "android" in names
        has_ios = "ios" in names
        if has_android or has_ios:
            if platform == "android" and not has_android:
                item.add_marker(skip_wrong_platform)
            if platform == "ios" and not has_ios:
                item.add_marker(skip_wrong_platform)
