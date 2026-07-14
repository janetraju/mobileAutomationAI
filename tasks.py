"""Invoke task runner for the mobile automation framework."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from invoke import task

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "target"


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
    """Start Android emulator (requires ANDROID_HOME)."""
    script = ROOT / "scripts" / "start-emulator.sh"
    env = os.environ.copy()
    if avd:
        env["AVD_NAME"] = avd
    if headless:
        env["HEADLESS"] = "true"
    c.run(f"bash {script}", env=env, pty=True)


@task(name="appium:start")
def appium_start(c, port=4723):
    """Start Appium 2.x server."""
    c.run(f"appium --port {port}", pty=True)


@task(name="appium:doctor")
def appium_doctor(c):
    """Run Appium environment health checks."""
    script = ROOT / "scripts" / "appium-doctor.sh"
    c.run(f"bash {script}", pty=True)


@task(name="appium:install-drivers")
def appium_install_drivers(c):
    """Install UiAutomator2 and XCUITest drivers."""
    c.run("appium driver install uiautomator2", pty=True)
    c.run("appium driver install xcuitest", pty=True)


@task(name="app:analyze")
def app_analyze(c, apk=""):
    """Extract package, activity, and app-type hints from APK."""
    script = ROOT / "scripts" / "analyze-apk.sh"
    path = apk or os.environ.get("APP_PATH", "")
    if not path:
        c.run(f"bash {script} builds/*.apk", warn=True, pty=True)
    else:
        c.run(f'bash {script} "{path}"', pty=True)


@task(name="app:install")
def app_install(c, apk=""):
    """Install APK on connected Android device."""
    script = ROOT / "scripts" / "install-app.sh"
    if apk:
        c.run(f'bash {script} "{apk}"', pty=True)
    else:
        c.run(f"bash {script}", pty=True)


@task(name="ui:dump")
def ui_dump(c, screen="screen"):
    """Dump Android UI hierarchy to docs/locators/<screen>.xml."""
    script = ROOT / "scripts" / "dump-ui.sh"
    c.run(f'bash {script} "{screen}"', pty=True)


@task
def lint(c, fix=False):
    """Run ruff and black."""
    fix_flag = "--fix" if fix else ""
    c.run(f"ruff check src tests {fix_flag}", pty=True)
    c.run("black --check src tests" if not fix else "black src tests", pty=True)


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
    """Clean, lint, and run pytest."""
    clean(c)
    lint(c)
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
