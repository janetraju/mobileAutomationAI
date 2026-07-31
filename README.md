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

More detail: [`docs/cofee-flow.md`](docs/cofee-flow.md) · feature notes: `docs/context/`

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
| `docs/` | Flow + context docs |
| `tasks.py` | `invoke` commands |

Rules for agents and contributors: **[`AGENTS.md`](AGENTS.md)**.

---

## Prerequisites

Python 3.10+ · Node 18+ (Appium 2) · JDK 11+ · Android SDK (`ANDROID_HOME`) · Allure CLI  
(iOS: Xcode 15+ on macOS)

---

## Quick start

```bash
cp .env.example .env          # set APP_* , APP_PATH, TEST_MOBILE, TEST_OTP
export ANDROID_HOME=/path/to/Android/Sdk

python -m venv .venv && source .venv/bin/activate
invoke install
invoke install-precommit
invoke appium:install-drivers

invoke emulator:start         # terminal 1
invoke appium:start           # terminal 2

invoke test --markers "e2e and p0"
invoke report
```

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

Each pytest run wipes `target/allure-results` (`--clean-alluredir`), so reports
match the last run only.

**New feature order:** page object → actions → steps → dataprovider → test  
(`AGENTS.md` / `mobile-appium-python` skill).

---

## Adding another app

1. Point `.env` at the new `APP_SLUG` / package / APK  
2. Register the app in `src/core/settings.py` (`APP_REGISTRY`)  
3. Add folders under `src/**/<slug>/` and `tests/test/<slug>/`  
4. Add `docs/<slug>-flow.md` and discover locators on device  

Or run skill **`get-context`** (Phase 0 asks for APK if the app is not configured yet).
