"""Invoke task runner for the mobile automation framework.

Device / Appium helpers live here (no separate scripts/ folder).
"""

from __future__ import annotations

import glob
import os
import shutil
import subprocess
import time
import zipfile
from pathlib import Path

from invoke import task

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "target"


def _android_home() -> Path:
    return Path(os.environ.get("ANDROID_HOME") or Path.home() / "Android" / "Sdk")


def _adb() -> Path:
    adb = _android_home() / "platform-tools" / "adb"
    if not adb.is_file():
        raise SystemExit(f"ERROR: adb not found at {adb}. Set ANDROID_HOME.")
    return adb


def _emulator_bin() -> Path:
    emu = _android_home() / "emulator" / "emulator"
    if not emu.is_file():
        raise SystemExit(f"ERROR: emulator not found at {emu}. Set ANDROID_HOME.")
    return emu


def _aapt() -> Path | None:
    build_tools = _android_home() / "build-tools"
    if not build_tools.is_dir():
        return None
    candidates = sorted(build_tools.glob("*/aapt"))
    return candidates[-1] if candidates else None


def _load_app_path_from_env_file() -> str:
    env_file = ROOT / ".env"
    if not env_file.is_file():
        return ""
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line.startswith("APP_PATH=") and not line.startswith("#"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _wait_for_device(timeout: int | None = None) -> None:
    """Wait until adb reports a device and Android has finished booting."""
    adb = _adb()
    timeout = timeout or int(os.environ.get("DEVICE_WAIT_TIMEOUT", "180"))
    interval = 2
    elapsed = 0
    print(f"Waiting for Android device (timeout {timeout}s)...")
    while elapsed < timeout:
        result = subprocess.run(
            [str(adb), "devices"],
            capture_output=True,
            text=True,
            check=False,
        )
        ready = any(
            line.strip().endswith("\tdevice")
            for line in result.stdout.splitlines()[1:]
            if line.strip()
        )
        if ready:
            boot = subprocess.run(
                [str(adb), "shell", "getprop", "sys.boot_completed"],
                capture_output=True,
                text=True,
                check=False,
            )
            if boot.stdout.strip() == "1":
                print("Device connected.")
                return
        time.sleep(interval)
        elapsed += interval
    subprocess.run([str(adb), "devices"], check=False)
    raise SystemExit(f"ERROR: No ready device within {timeout}s.")


def _apk_type_hint(apk: Path) -> str:
    with zipfile.ZipFile(apk) as zf:
        names = zf.namelist()
    joined = "\n".join(names)
    if "libflutter.so" in joined or "flutter_assets/" in joined:
        return "flutter"
    if "index.android.bundle" in joined:
        return "rn"
    if "webview" in joined.lower():
        return "hybrid"
    return "native"


@task
def install(c):
    """Install Python dependencies from pyproject.toml."""
    c.run("pip install -e .", pty=True)


@task
def install_precommit(c):
    """Install pre-commit hooks."""
    c.run("pre-commit install", pty=True)


@task(name="emulator:start")
def emulator_start(c, avd=None, headless=False):
    """Start Android emulator and wait until it is ready (requires ANDROID_HOME)."""
    avd_name = avd or os.environ.get("AVD_NAME", "Pixel_10")
    use_headless = headless or os.environ.get("HEADLESS", "false").lower() == "true"
    emu = _emulator_bin()
    args = [str(emu), "-avd", avd_name, "-no-snapshot-load"]
    if use_headless:
        args.extend(["-no-window", "-no-audio"])
    print(f"Starting emulator: {avd_name} (headless={use_headless})")
    proc = subprocess.Popen(args)
    try:
        _wait_for_device()
        print(f"Emulator ready (PID {proc.pid})")
        # Keep this process attached so the emulator is not SIGHUP'd when invoke exits.
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        raise


@task(name="appium:start")
def appium_start(c, port=4723):
    """Start Appium 2.x server."""
    c.run(f"appium --port {port}", pty=True)


@task(name="appium:doctor")
def appium_doctor(c):
    """Run Appium environment health checks."""
    print("=== Appium version ===")
    c.run("appium --version", warn=True, pty=True)
    print("\n=== Installed drivers ===")
    c.run("appium driver list --installed", warn=True, pty=True)
    print("\n=== Node / npm ===")
    c.run("node --version", warn=True, pty=True)
    c.run("npm --version", warn=True, pty=True)
    print("\n=== Java ===")
    c.run("java -version", warn=True, pty=True)
    print("\n=== Android SDK ===")
    print(f"ANDROID_HOME={os.environ.get('ANDROID_HOME', 'not set')}")
    adb = _android_home() / "platform-tools" / "adb"
    if adb.is_file():
        c.run(f'"{adb}" version', warn=True, pty=True)
    print("\n=== Xcode (macOS / iOS) ===")
    if shutil.which("xcodebuild"):
        c.run("xcodebuild -version", warn=True, pty=True)
    else:
        print("xcodebuild not available (skip for Android-only hosts)")
    print("\nDoctor complete.")


@task(name="appium:install-drivers")
def appium_install_drivers(c):
    """Install UiAutomator2 and XCUITest drivers."""
    c.run("appium driver install uiautomator2", pty=True)
    c.run("appium driver install xcuitest", pty=True)


@task(name="app:analyze")
def app_analyze(c, apk=""):
    """Extract package, activity, and app-type hints from APK."""
    path = apk or os.environ.get("APP_PATH", "") or _load_app_path_from_env_file()
    if not path:
        matches = sorted(glob.glob(str(ROOT / "builds" / "*.apk")))
        if not matches:
            raise SystemExit("Usage: invoke app:analyze --apk=<path>  OR set APP_PATH")
        path = matches[0]
        print(f"Using {path}")
    apk_path = Path(path)
    if not apk_path.is_file():
        raise SystemExit(f"ERROR: APK not found: {apk_path}")

    print("=== File ===")
    c.run(f'file "{apk_path}"', warn=True, pty=True)
    print()

    aapt = _aapt()
    if aapt and aapt.is_file():
        print("=== Badging ===")
        c.run(
            f'"{aapt}" dump badging "{apk_path}" | grep -E '
            f'"package:|application-label:|launchable-activity:"',
            warn=True,
            pty=True,
        )
        print()

    print("=== App type hints ===")
    print(f"APP_TYPE={_apk_type_hint(apk_path)}")

    with zipfile.ZipFile(apk_path) as zf:
        env_member = "assets/flutter_assets/.env"
        if env_member in zf.namelist():
            print("\n=== Bundled flutter .env (non-secret keys only) ===")
            raw = zf.read(env_member).decode("utf-8", errors="ignore")
            for line in raw.splitlines():
                if line.startswith(("env=", "base_url=", "web_base_url=")):
                    print(line)


@task(name="app:install")
def app_install(c, apk=""):
    """Install APK on connected Android device."""
    path = apk or os.environ.get("APP_PATH", "") or _load_app_path_from_env_file()
    if not path:
        raise SystemExit("Usage: invoke app:install --apk=<path>  OR set APP_PATH in .env")
    apk_path = Path(path)
    if not apk_path.is_file():
        raise SystemExit(f"ERROR: App binary not found: {apk_path}")
    adb = _adb()
    print(f"Installing {apk_path} ...")
    c.run(f'"{adb}" install -r -d "{apk_path}"', pty=True)
    print("Install complete.")


@task(name="ui:dump")
def ui_dump(c, screen="screen"):
    """Dump Android UI hierarchy to docs/locators/<screen>.xml."""
    adb = _adb()
    out_dir = ROOT / "docs" / "locators"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{screen}.xml"
    remote = "/sdcard/window_dump.xml"
    print(f"Dumping UI to {out_file} ...")
    c.run(f'"{adb}" shell uiautomator dump {remote}', hide=True, pty=True)
    c.run(f'"{adb}" pull {remote} "{out_file}"', hide=True, pty=True)
    c.run(f'"{adb}" shell rm -f {remote}', warn=True, hide=True, pty=True)
    lines = sum(1 for _ in out_file.open()) if out_file.is_file() else 0
    print(f"UI dump saved: {out_file} ({lines} lines)")


@task
def lint(c, fix=True):
    """Auto-fix with ruff + black (use --no-fix for check-only)."""
    if fix:
        c.run("ruff check src tests --fix", pty=True)
        c.run("black src tests", pty=True)
    else:
        c.run("ruff check src tests", pty=True)
        c.run("black --check src tests", pty=True)


@task
def precommit(c):
    """Run all pre-commit hooks."""
    c.run("pre-commit run --all-files", pty=True)


@task
def clean(c):
    """Remove build and test artifacts."""
    for path in [TARGET, ROOT / ".pytest_cache", ROOT / ".ruff_cache"]:
        if path.exists():
            shutil.rmtree(path)
    c.run("find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true")


@task
def test(c, markers="", env="", platform="", parallel="auto", extra=""):
    """Clean, auto-fix lint (ruff + black), and run pytest."""
    clean(c)
    lint(c, fix=True)
    cmd = "pytest"
    if markers:
        cmd += f' -m "{markers}"'
    if env:
        cmd += f" --env={env}"
    if platform:
        cmd += f" --platform={platform}"
    if parallel:
        cmd += f" -n {parallel}"
    if extra:
        cmd += f" {extra}"
    c.run(cmd, pty=True)


@task
def report(c, port=5050):
    """Generate and open Allure report from the latest pytest run only."""
    results = TARGET / "allure-results"
    report_dir = TARGET / "allure-report"
    if not results.exists() or not any(results.iterdir()):
        print("No allure-results found. Run tests first (pytest clears results each run).")
        return
    c.run(f"allure generate {results} -o {report_dir} --clean", pty=True)
    c.run(f"allure open {report_dir} -h 127.0.0.1 -p {port}", pty=True)
