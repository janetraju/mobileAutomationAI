# CoFee Mobile Automation

Agent entry point for the **app-agnostic** Pytest + Appium + Allure mobile UI framework configured for **CoFee** (`APP_SLUG=cofee`).

## Stack

**Appium 2.x + Pytest + Python + Allure. Four-layer POM.**

- Sync `appium.webdriver.webdriver.WebDriver` API only — no async drivers
- Config: `python-dotenv` + Pydantic (`src/core/settings.py`)
- Task runner: `invoke` (`tasks.py`)
- **App type:** Flutter (`APP_TYPE=flutter`)

## Quick start

```bash
cp .env.example .env          # set APP_NAME, APP_SLUG, identifiers
invoke install
invoke install-precommit
invoke appium:install-drivers
invoke emulator:start         # Android only
invoke app:install            # install APK from APP_PATH
invoke appium:start           # separate terminal
invoke test --markers "e2e and p0"
invoke report
```

## Invoke commands

| Task | Description |
|------|-------------|
| `invoke install` | Install Python deps (`pip install -e .`) |
| `invoke install-precommit` | Install git pre-commit hooks |
| `invoke emulator:start` | Start Android emulator + wait for device |
| `invoke app:analyze` | Extract package/activity/type from APK |
| `invoke app:install` | Install APK on connected device |
| `invoke ui:dump --screen=<name>` | Save UI tree to `docs/locators/<name>.xml` |
| `invoke appium:start` | Start Appium 2.x server |
| `invoke appium:doctor` | Environment health check |
| `invoke appium:install-drivers` | Install UiAutomator2 + XCUITest drivers |
| `invoke lint` | Auto-fix with ruff (`--fix`) + black |
| `invoke lint --no-fix` | Check-only (no writes) |
| `invoke precommit` | Run all pre-commit hooks |
| `invoke clean` | Remove `target/`, caches |
| `invoke test` | clean → lint (auto-fix) → pytest |
| `invoke report` | Generate + open Allure report |

## Directory tree

```
src/
  core/                    # Framework base — no app imports upward
  page_objects/cofee/      # Layer 1: locators only (*_po.py)
  page_actions/cofee/      # Layer 2: interactions (*_actions.py)
  steps/cofee/             # Layer 3: @allure.step orchestration
  constants/cofee/         # Static strings (no secrets)
tests/
  conftest.py
  parallel_groups.py
  dataprovider/            # dp_<feature>.py
  test/cofee/              # Layer 4: test_*.py
data/cofee/                # Structured fixtures
docs/cofee-flow.md         # Product flows — read before authoring tests
docs/locators/             # UI dumps per screen (discover-mobile-locators)
environment/               # Per-env .properties overrides
scripts/                   # Emulator / Appium / install / dump helpers
```

## Layer rules (strict)

Import direction: **tests → steps → page_actions → page_objects → core**

| Layer | May call | Must not call |
|-------|----------|---------------|
| Tests | steps, assert_helper | page_actions, POs, driver |
| Steps | page_actions | POs, driver |
| Page actions | page_objects, core | driver.find_element (use PO) |
| Page objects | core BasePage | business logic, gestures |

- Locators only in `*_po.py` under `# --- Locators ---` block
- `driver.find_element()` forbidden outside page objects
- No `time.sleep()` — explicit waits only
- Re-query elements after navigation / animation
- Platform branching only in POs or `*_android_po.py` / `*_ios_po.py`

## Locator priority

1. `AppiumBy.ACCESSIBILITY_ID`
2. Android `ANDROID_UIAUTOMATOR` / resource-id
3. iOS `IOS_PREDICATE` / `IOS_CLASS_CHAIN`
4. Text / content-desc / label
5. XPath — last resort

Prefix convention: `btn_`, `txt_`, `input_`, `chk_`, `ddl_`, `lnk_`, `msg_`, `icn_`, etc.

## Key `.env` variables

`APP_NAME`, `APP_SLUG`, `APP_TYPE`, `APP_ENV`, `PLATFORM`, `APPIUM_HOST`, `APPIUM_PORT`, `DEVICE_NAME`, `APP_PATH`, `APP_PACKAGE`, `APP_ACTIVITY`, `API_BASE_URL`, `TEST_MOBILE`, `OTP_GENERATE_PATH`, `OTP_VALIDATE_PATH`, `NO_RESET`, `EXPLICIT_WAIT_TIMEOUT`

## Skills

Canonical copies live in `.cursor/skills/`. `.claude/skills/` are **symlinks** to
those same folders (not duplicates) so Claude slash-commands resolve.

### Feature lifecycle (use in order)

| Skill | Role | Output / handoff |
|-------|------|------------------|
| `onboard-mobile-app` | New APK/IPA → registry, `.env`, folder rename | Ready for discovery |
| `get-context` | **Preferred** feature intake (PRD/Figma/Jira/app source) | `docs/context/<app_slug>-<feature>-context.md` |
| `author-mobile-flow-docs` | **Fallback** only when `get-context` was not run — screenshots / walkthrough / product repo → flow doc | `docs/<app_slug>-flow.md` |
| `extract-p0-test-cases` | Generate P0/P1/P2 cases from context or flow doc (approval gated) | `docs/context/<app_slug>-<feature>-testcases.md` |
| `discover-mobile-locators` | Live UI dump / Appium MCP — confirm locators (never invent) | `docs/locators/<screen>.xml` + locator sheet |
| `setup-mobile-test-data` | OTP, API seeding, credentials via `.env` | Test data ready |
| `automate-a-flow` | **Orchestrate** an approved scenario: prerequisites → MCP walkthrough → then call coding skill | Working E2E for one flow |
| `mobile-appium-python` | **Write code** — PO / actions / steps / dataprovider / test patterns, markers, flaky playbook | Layered automation files |

`automate-a-flow` and `mobile-appium-python` are **not** duplicates:
orchestration vs layer authoring. Prefer `automate-a-flow` when the user says
"automate this"; use `mobile-appium-python` when editing an existing layer or
debugging flaky locators/markers.

### Supporting (any time)

| Skill | When to use |
|-------|-------------|
| `read-test-reports` | **Generate** Allure HTML (`invoke report`) and **read**/triage failure artifacts |
| `review-changes` | Code review checklist before merge |
| `author-pr-description` | Draft PR body from real branch diff (approval before `gh pr create`) |

### Pipeline

```text
# Preferred
get-context
  → extract-p0-test-cases
  → discover-mobile-locators   # invoke ui:dump and/or Appium MCP
  → setup-mobile-test-data
  → automate-a-flow            # MCP walkthrough mandatory before new TC
  → mobile-appium-python       # layer implementation

# Fallback (no get-context this session)
author-mobile-flow-docs → extract-p0-test-cases → (same from discover onward)

# New app binary only
onboard-mobile-app → get-context | author-mobile-flow-docs → …
```

Treat context / flow docs as the **flow spec**. Locators must always be
confirmed on a running app — product source alone is never enough.

## MCP Tools

### Appium MCP (project-local)

| File | Purpose |
|------|---------|
| `.cursor/mcp.json` | Cursor MCP server (`npx appium-mcp@latest`) |
| `environment/appium-mcp.capabilities.json` | Android/iOS caps — keep aligned with `.env` |

**Prerequisites:** `ANDROID_HOME`, device/emulator up, `invoke appium:install-drivers`.
**Enable:** Restart Cursor / reload MCP → toggle **appium-mcp** under Customize → MCP.

Full walkthrough steps live in **`automate-a-flow` Step 2d** (and
`discover-mobile-locators` §3b). Screenshots → `target/mcp-screenshots/` when
`NO_UI=true`.

### Figma MCP

Design copy only — confirm via live dump. See **`get-context`**.

## Product flows

Read **`docs/cofee-flow.md`** before writing tests. Do not invent flows or
selectors not documented **or** inspected on device.

## Adding a feature (code order)

Use **`automate-a-flow`** for the full workflow. Layer files:

1. `src/page_objects/cofee/<screen>_po.py`
2. `src/page_actions/cofee/<screen>_actions.py`
3. `src/steps/cofee/<feature>_steps.py`
4. `tests/dataprovider/dp_<feature>.py`
5. `tests/test/cofee/<feature>/test_<feature>.py`

Every UI test: `@pytest.mark.e2e`, priority (`p0`/`p1`/`p2`), Allure labels,
platform marker when needed.
