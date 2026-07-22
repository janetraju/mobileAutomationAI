# [APP NAME] Mobile UI Automation

App-agnostic **Pytest + Appium 2.x + Allure** framework with a strict four-layer Page Object Model. Swap apps by changing `.env` — no code changes required in `src/core/`.

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.10+ | 3.11+ recommended |
| Node.js | 18+ | For Appium 2.x (`npm install -g appium@2`) |
| Java JDK | 11+ | Android SDK / emulator |
| Android SDK | API 30+ | Set `ANDROID_HOME` |
| Xcode | 15+ | iOS only (macOS) |
| Allure CLI | 2.x | `invoke report` |

## Setup

```bash
# 1. Configure app
cp .env.example .env
# Edit: APP_NAME, APP_SLUG, PLATFORM, APP_PATH or package/bundle IDs

# 2. Optional per-environment overrides
cp .env.dev.example .env.dev
cp environment/dev.properties.example environment/dev.properties

# 2b. Appium MCP (for AI-assisted testing via .mcp.json)
# export ANDROID_HOME to your local Android SDK path — .mcp.json reads it via ${ANDROID_HOME}
export ANDROID_HOME=/path/to/your/Android/Sdk

# 3. Install
python -m venv .venv && source .venv/bin/activate
invoke install
invoke install-precommit
invoke appium:install-drivers

# 4. Start infrastructure (Android)
invoke emulator:start    # terminal 1
invoke appium:start      # terminal 2

# 5. Run tests (each pytest run starts with a fresh Allure results folder)
invoke test --markers "e2e and p0"
# or: APP_PATH= pytest tests/test/cofee/ -m "e2e and p0" --env=dev -v -s -n 0
invoke report   # HTML report for this run only (pass/fail + failure screenshots)
```

## Allure reports

Pytest uses `--clean-alluredir`, so **`target/allure-results` is wiped at the start of every run**. That way `invoke report` shows only the latest execution (not historical pile-up).

```bash
allure generate target/allure-results -o target/allure-report --clean
allure open target/allure-report
```

## Swapping / adding apps

1. Set `APP_NAME` and `APP_SLUG` in `.env`
2. Add package/bundle IDs under `APP_REGISTRY` in `src/core/settings.py`
3. Create layers under `src/page_objects/<slug>/`, `page_actions/`, `steps/`, `tests/test/<slug>/`
4. Add `docs/<slug>-flow.md` and run locator discovery
5. Update `AGENTS.md` skill paths if needed

See skill `onboard-mobile-app` for the full checklist.

## Architecture

```
tests  →  steps  →  page_actions  →  page_objects  →  core
```

See **`AGENTS.md`** for layer rules, locator priority, and Cursor agent guidance.

## Project layout

```
src/core/           # base_page, page_actions, session_manager, settings, capabilities
src/page_objects/   # locators only
src/page_actions/   # interactions + gestures
src/steps/          # @allure.step user actions
tests/              # pytest tests, conftest, dataproviders
data/               # structured fixtures (encrypt secrets at rest)
docs/               # flow documentation per app
scripts/            # emulator + Appium helpers
tasks.py            # invoke task runner
```

## CLI overrides

```bash
pytest --env=uat --platform=android --device=emulator-5554
pytest --record-video --headless-emulator
```

## Linting

```bash
invoke lint            # auto-fix (ruff --fix + black) — default
invoke lint --no-fix   # check-only
invoke test            # clean → lint (auto-fix) → pytest
invoke precommit       # all hooks
```

Pre-commit runs **ruff** (with fix) and **black**. `invoke lint` and `invoke test`
always auto-fix unless you pass `--no-fix` to lint.

## Current app: CoFee

Configured via `.env` (`APP_SLUG=cofee`, `APP_TYPE=flutter`).

| Item | Path |
|------|------|
| Flow doc | `docs/cofee-flow.md` |
| APK | `builds/cofee-dev.apk` |
| P0 tests | Login + create group under `tests/test/cofee/` |
| Locator dumps | `docs/locators/` (confirmed screens only) |

Add a new feature in order: page object → actions → steps → dataprovider → test. See `AGENTS.md`.
