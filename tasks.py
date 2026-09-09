"""`invoke` tasks — see `AGENTS.md` → Invoke commands for the full reference.

`invoke`'s namespace separator is `.`, but AGENTS.md documents `app:analyze`,
`appium:start`, `ui:dump`, etc. with colons — so those are registered as flat
task names containing a literal `:` (invoke allows arbitrary characters in a
task name; only `.` triggers sub-collection lookup) rather than as real
sub-collections, to keep the commands every skill documents copy-pasteable.
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

from invoke import Collection, task

REPO_ROOT = Path(__file__).resolve().parent


# --- Root tasks ---


@task
def install(c):
    """Install Python deps (pip install -e .)."""
    c.run("pip install -e .")


@task
def install_precommit(c):
    """Install git pre-commit hooks."""
    c.run("pre-commit install")


@task(help={"no_fix": "Check only, don't auto-fix"})
def lint(c, no_fix=False):
    """Auto-fix with ruff (--fix) + black; pass --no-fix to check only."""
    if no_fix:
        c.run("ruff check .")
        c.run("black --check .")
    else:
        c.run("ruff check . --fix")
        c.run("black .")


@task
def precommit(c):
    """Run all pre-commit hooks against every file."""
    c.run("pre-commit run --all-files")


@task
def clean(c):
    """Remove target/ and caches."""
    for path in (
        REPO_ROOT / "target",
        REPO_ROOT / ".pytest_cache",
        REPO_ROOT / ".ruff_cache",
    ):
        if path.exists():
            shutil.rmtree(path)
    for cache_dir in REPO_ROOT.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


@task(help={"markers": 'pytest -m expression, e.g. "e2e and p0"'})
def test(c, markers=None):
    """clean -> lint (auto-fix) -> pytest."""
    clean(c)
    lint(c)
    expr = markers or "e2e"
    exclude_ignored = f"({expr}) and not ignore"
    c.run(f'pytest -m "{exclude_ignored}"', pty=sys.platform != "win32")


@task(help={"port": "Local port to serve the Allure report on"})
def report(c, port=5050):
    """Generate + open the Allure HTML report."""
    c.run(
        "allure generate target/allure-results -o target/allure-report --clean",
    )
    c.run(f"allure open target/allure-report -h 127.0.0.1 -p {port}")


# --- app:* ---


@task(name="app:analyze", help={"apk": "Path to the APK to inspect"})
def app_analyze(c, apk):
    """Extract package/activity/app-type from an APK (Android)."""
    from loguru import logger as _androguard_logger

    _androguard_logger.remove()  # androguard logs via loguru; quiet its DEBUG noise
    from androguard.core.apk import APK

    apk_obj = APK(apk)
    files = apk_obj.get_files()
    app_type = "native"
    if any("flutter" in f.lower() for f in files):
        app_type = "flutter"
    elif any("index.android.bundle" in f for f in files):
        app_type = "rn"

    version = f"{apk_obj.get_androidversion_name()} ({apk_obj.get_androidversion_code()})"
    print(f"Package:       {apk_obj.get_package()}")
    print(f"Main activity: {apk_obj.get_main_activity()}")
    print(f"App name:      {apk_obj.get_app_name()}")
    print(f"Version:       {version}")
    print(f"Min SDK:       {apk_obj.get_min_sdk_version()}")
    print(f"Target SDK:    {apk_obj.get_target_sdk_version()}")
    print(f"App type:      {app_type} (heuristic — confirm manually for hybrid apps)")


@task(
    name="app:install",
    help={"device": "Target device/emulator serial (defaults to DEVICE_NAME)"},
)
def app_install(c, device=None):
    """Install the configured APP_PATH onto a connected device."""
    from src.core.settings import get_settings

    settings = get_settings()
    apk = settings.app_path_resolved
    if not apk or not apk.exists():
        sys.exit(f"APP_PATH not set or file not found: {settings.app_path}")
    serial = device or settings.device_name
    serial_flag = f"-s {serial} " if serial else ""
    c.run(f"adb {serial_flag}install -r {apk}")


# --- appium:* ---


@task(name="appium:start")
def appium_start(c):
    """Start the Appium 2.x server in the foreground."""
    c.run("appium", pty=sys.platform != "win32")


@task(name="appium:doctor")
def appium_doctor(c):
    """Run the Appium environment health check."""
    c.run("appium-doctor")


@task(name="appium:install-drivers")
def appium_install_drivers(c):
    """Install the UiAutomator2 + XCUITest Appium drivers."""
    c.run("appium driver install uiautomator2")
    c.run("appium driver install xcuitest")


# --- emulator:* ---


_EMULATOR_AVD_HELP = (
    "AVD name to boot (defaults to AVD_NAME in .env -- NOT DEVICE_NAME, which is "
    "the adb serial an already-running device/emulator answers to)"
)


@task(name="emulator:start", help={"avd": _EMULATOR_AVD_HELP})
def emulator_start(c, avd=None):
    """Start an Android emulator and wait for the device to come online."""
    from src.core.settings import get_settings

    name = avd or get_settings().avd_name
    if not name:
        sys.exit("No AVD name given and AVD_NAME is not set in .env")
    c.run(f"emulator -avd {name} &", asynchronous=True)
    c.run("adb wait-for-device")
    booted = False
    for _ in range(60):
        result = c.run("adb shell getprop sys.boot_completed", warn=True, hide=True)
        if result.ok and result.stdout.strip() == "1":
            booted = True
            break
        time.sleep(2)
    if not booted:
        sys.exit("Emulator did not finish booting within the timeout")


# --- ui:* ---


@task(name="ui:dump", help={"screen": "Name to save the dump under, e.g. 'home'"})
def ui_dump(c, screen):
    """Save the current UI tree to target/ui-dumps/<screen>.xml via adb."""
    out_dir = REPO_ROOT / "target" / "ui-dumps"
    out_dir.mkdir(parents=True, exist_ok=True)
    device_path = "/sdcard/window_dump.xml"
    c.run(f"adb shell uiautomator dump {device_path}")
    c.run(f"adb pull {device_path} {out_dir / f'{screen}.xml'}")


ns = Collection()
ns.add_task(install)
ns.add_task(install_precommit, name="install-precommit")
ns.add_task(lint)
ns.add_task(precommit)
ns.add_task(clean)
ns.add_task(test)
ns.add_task(report)
ns.add_task(app_analyze)
ns.add_task(app_install)
ns.add_task(appium_start)
ns.add_task(appium_doctor)
ns.add_task(appium_install_drivers)
ns.add_task(emulator_start)
ns.add_task(ui_dump)
