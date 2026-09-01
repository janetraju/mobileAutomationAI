# CoFee Mobile UI Automation

**Updated on:** 31 July 2026

## App description

**CoFee** helps organizers collect fees and payments from groups (clubs, classes,
communities, small businesses). Users create groups, add members, set amounts and
collection schedules, track dues, and send reminders or payment links.

| | |
|--|--|
| Platform under test | Android (Flutter) |
| Package | `cofee.life.app.dev` |
| Dev API | `https://api.dev.cofee.life` |
| Login | Phone + OTP |
| Dev APK | `builds/cofee-dev.apk` |

**Automation focus today**

- Login / onboarding  
- Create group (manual member; monthly or weekly fee schedule)  
- Payments (including enable partial payment)  

More detail: [`docs/cofee-flow.md`](docs/cofee-flow.md) (coverage index) ·
feature context: [`docs/context/`](docs/context/README.md)

---

## Framework

This repo is a **Pytest + Appium 2.x + Allure** UI automation framework with a
four-layer Page Object Model. It is app-agnostic at the core (`src/core/`); CoFee
is the product wired in via `.env` (`APP_SLUG=cofee`).

```text
tests → steps → page_actions → page_objects → core
```

| Path | Role |
|------|------|
| `src/page_objects/` | Locators |
| `src/page_actions/` | Taps, type, gestures |
| `src/steps/` | `@allure.step` flows |
| `tests/` | Pytest + dataproviders |
| `docs/` | Flow **index** + `docs/context/` feature context & approved testcases |
| `tasks.py` | `invoke` commands |

Rules for agents and contributors: **[`AGENTS.md`](AGENTS.md)**.

---

## Prerequisites

Python 3.10+ · Node 18+ (Appium 2) · JDK 11+ · Android SDK (`ANDROID_HOME`) · Allure CLI  
**iOS Simulator:** macOS + Xcode 15+ only (cannot boot on Linux/Windows)

---

## Quick start

```bash
cp .env.example .env          # set APP_* , APP_PATH, TEST_MOBILE, TEST_OTP
export ANDROID_HOME=/path/to/Android/Sdk

python -m venv .venv && source .venv/bin/activate
invoke install
invoke install-precommit
invoke appium:install-drivers

invoke emulator:start         # terminal 1 (Android)
invoke appium:start           # terminal 2

invoke test --markers "e2e and p0"
invoke report
```

### iOS Simulator (macOS only)

```bash
cp .env.ios.example .env      # PLATFORM=ios, DEVICE_NAME=iPhone 16, APP_PATH=.app
invoke simulator:start        # boots Simulator via simctl (fails clearly on Linux)
invoke appium:start
pytest --platform=ios -m "e2e and p0"
```

On Linux, `invoke simulator:start` exits with an error — use Android emulator instead.
Login is marked for both platforms; groups/payments/home stay `@pytest.mark.android`
until iOS locators are confirmed live.

Optional env overrides: `.env.dev` · `environment/dev.properties`  
Appium MCP (AI device walkthrough): `.mcp.json` + `environment/appium-mcp.capabilities.json`

---

## Day-to-day commands

```bash
invoke test --markers "e2e and p0"   # clean → lint → pytest
invoke report                        # latest Allure HTML only
invoke lint                          # ruff --fix + black
invoke lint --no-fix                 # check only
pytest --env=uat --platform=android --device=emulator-5554
```

### Parallel runs (one worker → one device)

By default every worker would use the same `DEVICE_NAME` and fight over one
emulator. For safe parallel runs, set a pool and match `-n` to the pool size:

```bash
# .env
DEVICE_POOL=emulator-5554,emulator-5556,emulator-5558

# Optional: separate Appium servers per worker
# APPIUM_PORT_POOL=4723,4725,4727

pytest -n 3 -m "e2e and p0"
# or: invoke test --markers "e2e and p0" --parallel 3
```

Worker `gw0` gets the first device, `gw1` the second, and so on. If the pool is
smaller than `-n`, the run fails fast with a clear error.

### Test isolation (no “login first”)

Feature tests use `@pytest.mark.authenticated` — before the test body runs, a
fixture ensures logged-in home on **that** device (login if needed). Login tests
use `@pytest.mark.fresh` and clear the app themselves. You can run groups or
payments alone; they no longer depend on the login test running earlier.

### Flake auto-retry

Mobile UI tests can fail once from lag, then pass on retry. By default pytest
retries a failed test **1 extra time** (2 second delay) via `pytest-rerunfailures`
(`--reruns 1` in `pytest.ini`).

```bash
pytest -m "e2e and p0"              # default: 1 retry
pytest --reruns 0                   # disable retries (debug real failures)
invoke test --reruns 2              # allow 2 retries
# Optional per-test: @pytest.mark.flaky(reruns=2)
```

Retries hide rare timing noise — still fix root causes (waits, locators, data).

Each pytest run wipes `target/allure-results` (`--clean-alluredir`), so reports
match the last run only.

**New feature order:** page object → actions → steps → dataprovider → test  
(`AGENTS.md` / `testscript-generator` skill).

---

## Adding another app

1. Point `.env` at the new `APP_SLUG` / package / APK  
2. Register the app in `src/core/settings.py` (`APP_REGISTRY`)  
3. Add folders under `src/**/<slug>/` and `tests/test/<slug>/`  
4. Add `docs/<slug>-flow.md` and discover locators on device  

Or run skill **`get-context`** (Phase 0 asks for APK if the app is not configured yet).
