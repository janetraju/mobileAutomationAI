# CoFee Mobile Automation

Agent entry point for the **app-agnostic** Pytest + Appium + Allure mobile UI
framework configured for **CoFee** (`APP_SLUG=cofee`).

## How this repo is governed

| Document | Owns |
|----------|------|
| **`AGENTS.md` (this file)** | Always-on **repo contract** — architecture, layers, waits, assertions, stability, markers; locator *policy* (never invent; confirm live) |
| **`discover-mobile-locators`** | Locator **priority, naming, dumps** + dump/MCP workflow |
| **Other `.cursor/skills/*/SKILL.md`** | Task workflows only — do not restate repo contract |
| **`.cursor/rules/testscript-generator.mdc`** | Short always-apply pointer to this contract |

Skills must **not** restate layer rules, wait policy, or markers. For locator
priority/naming, follow **`discover-mobile-locators`** (referenced under Locator
strategy below).

---

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
| `invoke ui:dump --screen=<name>` | Save UI tree to `target/ui-dumps/<name>.xml` |
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
docs/context/              # Feature context + approved testcases
target/ui-dumps/           # UI dumps from invoke ui:dump (local; under target/)
environment/               # Per-env .properties overrides
tasks.py                   # invoke tasks (emulator, install, dump, test, report)
```

---

## Repo contract (always-on)

Shared behavioral rules for every agent and contributor. Skills implement
*workflows*; they do not redefine these rules.

### Architecture & layer boundaries

Import direction: **tests → steps → page_actions → page_objects → core**

| Layer | May call | Must not call |
|-------|----------|---------------|
| Tests | steps, assert_helper | page_actions, POs, driver APIs for find/click |
| Steps | page_actions | POs, driver find/click |
| Page actions | page_objects, core | `driver.find_element` (use PO `find_*` / `loc_*`) |
| Page objects | core `BasePage` | business logic, gestures, assertions |

- Locators only in `*_po.py` under `# --- Locators ---`
- No page object imports in tests or steps
- No `page_actions` imports in tests when a step exists for the flow
- Platform branching only in page objects (`self._platform` or `*_android_po.py` / `*_ios_po.py`)
- Sync WebDriver only — never mix async Appium clients

### Locator strategy

**Never invent locators.** Screenshots, Figma, and product source are flow/spec
only — confirm every selector on a running app before treating a PO as final.

**Full priority order, PO naming (`btn_` / `find_*` / `loc_*`), and dump paths:**
see skill **`discover-mobile-locators`**.

### Wait & stability

- No `time.sleep()` — use explicit waits from `PageActions` / `BasePage`
- Use `EXPLICIT_WAIT_TIMEOUT` from settings — no magic timeouts
- Re-query elements after navigation / animation — no stale `WebElement` caching across screens
- Prefer left-biased taps when a known overlay (e.g. debug FAB) covers CTAs — document quirks in the flow doc

### Assertions

- Assertions belong in **tests** (via `assert_helper`) or thin step wrappers — not in page objects
- No `assert_helper` in page actions
- Assert **observable UI outcomes** (screen, copy, counts, amounts) — not just “navigation happened”
- On failure, Allure attachments (screenshot / page source) are handled in `conftest` — do not skip triage

### Tests, markers & Allure

Every UI test:

```python
@pytest.mark.e2e
@pytest.mark.p0  # or p1, p2
@pytest.mark.android  # or ios when platform-specific
@allure.epic("CoFee")
# + feature, story, severity
```

- `@pytest.mark.ignore` excluded from default runs
- Use `PARALLEL_GROUP_*` when sharing a session/device with other features
- Dataproviders: `get_*_test_data()` → `list[pytest.param(..., id="...")]` — **no secrets**

### Code quality

- No bare `except:` — use `except Exception:`
- Imports at module top only
- No `pytest.skip()` in page actions
- No hardcoded credentials or product names — `.env` / `get_settings()` / `APP_NAME`
- Lint: `invoke lint` / `invoke test` auto-fix (ruff + black); do not leave formatting for humans

### Test data & credentials

**OTP strategy** — pick one per app, document the choice in
`docs/<app_slug>-flow.md` → Known blockers / Test data:

| Strategy | Implementation |
|----------|----------------|
| Fixed OTP in dev | Set `TEST_OTP` in `.env` / `.env.dev` (never commit) |
| Manual | Mark test `@pytest.mark.manual_otp` or pause — avoid in CI |
| Bypass | Deep link / `auth_profile` + `NO_RESET` session reuse |

- Credentials live in `.env`/`.env.<env>` only — never in a committed context/flow doc, dataprovider, PO, or step
- No production credentials — dev/stg/uat only
- Fail fast if `TEST_MOBILE` is missing when login tests are collected
- Backend/SQL assertions: keep queries in `data/<app_slug>/` scripts — never in page layers

### Feature context vs automation

| Input | Role |
|-------|------|
| Screenshots / walkthrough / Figma / product repo / PRD | **Flow spec** (what to automate) |
| Live device dump / Appium MCP | **Locator source of truth** (how to find elements) |

Read **`docs/cofee-flow.md`** (and `docs/context/` when present) before writing tests.
Do not invent flows or selectors not documented **or** inspected on device.

---

## Key `.env` variables

`APP_NAME`, `APP_SLUG`, `APP_TYPE`, `APP_ENV`, `PLATFORM`, `APPIUM_HOST`,
`APPIUM_PORT`, `DEVICE_NAME`, `APP_PATH`, `APP_PACKAGE`, `APP_ACTIVITY`,
`API_BASE_URL`, `TEST_MOBILE`, `TEST_OTP`, `DEFAULT_USERNAME`,
`DEFAULT_PASSWORD`, `FEATURE_ORG_ID`, `FEATURE_ACCOUNT_ID`, `NO_RESET`,
`EXPLICIT_WAIT_TIMEOUT`

---

## Skills (execution helpers)

Canonical copies: `.cursor/skills/`. `.claude/skills/` are **symlinks** to the
same folders.

Each skill describes **only its workflow**. Shared behavior → **Repo contract**
above.

### Feature lifecycle (use in order)

| Skill | Role | Output / handoff |
|-------|------|------------------|
| `get-context` | Feature intake; **also** bootstraps a new app if not configured (asks for APK/IPA) | `docs/context/<app_slug>-<feature>-context.md` (+ registry/`.env` if new app) |
| `testcase-generator` | Generate P0/P1/P2 cases (approval gated) | `docs/context/<app_slug>-<feature>-testcases.md` |
| `discover-mobile-locators` | Live UI dump / Appium MCP | `target/ui-dumps/<screen>.xml` + confirmed PO locators |
| `testscript-generator` | Orchestrate **and** implement one approved scenario end-to-end (test data source decided in its Step 1); also the skill for writing/editing layer files or fixing flaky tests on their own | Working E2E for one flow / layered automation files |

Use `testscript-generator` for anything from "automate this feature" to
editing a single existing layer file or debugging a locator/marker — it's
one skill covering the full path from prerequisites through implementation.

### Supporting (any time)

| Skill | When to use |
|-------|-------------|
| `read-test-reports` | Generate Allure HTML and triage failures |
| `pr-review-changes` | Review against this **Repo contract** before merge |
| `add-pr-description` | Draft PR body from real branch diff |

### Pipeline

```text
# Preferred (app already configured, e.g. CoFee)
get-context
  → testcase-generator
  → discover-mobile-locators
  → testscript-generator

# New product (not in APP_REGISTRY / slug folders)
get-context Phase 0 asks for APK/IPA → wires repo → then same preferred pipeline
```

---

## MCP Tools

### Appium MCP (project-local)

| File | Purpose |
|------|---------|
| `.mcp.json` | Cursor MCP server (`npx appium-mcp@…`) |
| `environment/appium-mcp.capabilities.json` | Caps — keep aligned with `.env` |

**Prerequisites:** `ANDROID_HOME`, device/emulator up, `invoke appium:install-drivers`.  
**Enable:** Restart Cursor / reload MCP → toggle **appium-mcp**.

Walkthrough steps: **`testscript-generator`** and **`discover-mobile-locators`**.
Screenshots → `target/mcp-screenshots/` when `NO_UI=true`.

### Figma MCP

Design copy only — confirm locators via live dump. See **`get-context`**.

---

## Adding a feature (code order)

Use **`testscript-generator`** for the full workflow, including file order:

1. `src/page_objects/cofee/<screen>_po.py`
2. `src/page_actions/cofee/<screen>_actions.py`
3. `src/steps/cofee/<feature>_steps.py`
4. `tests/dataprovider/dp_<feature>.py`
5. `tests/test/cofee/<feature>/test_<feature>.py`
