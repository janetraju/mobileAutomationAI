# CoFee Mobile Automation

Agent entry point for the **app-agnostic** Pytest + Appium + Allure mobile UI
framework configured for **CoFee** (`APP_SLUG=cofee`).

## How this repo is governed

| Document | Owns |
|----------|------|
| **`AGENTS.md` (this file)** | Always-on **repo contract** — architecture, layers, locators, waits, assertions, stability, markers |
| **`.cursor/skills/*/SKILL.md`** | **Task workflows only** — how to perform one action (intake, dump, automate, review) |
| **`.cursor/rules/mobile-appium-python.mdc`** | Short always-apply pointer to this contract |

Skills must **not** restate layer rules, locator priority, wait policy, or markers.
They should say: *follow `AGENTS.md` Repo contract*, then describe their own steps.

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
docs/locators/             # UI dumps per screen (local; gitignored *.xml)
docs/context/              # Feature context + approved testcases
environment/               # Per-env .properties overrides
scripts/                   # Emulator / Appium / install / dump helpers
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

**Priority (highest first):**

1. `AppiumBy.ACCESSIBILITY_ID` / content-desc
2. Android `ANDROID_UIAUTOMATOR` / resource-id
3. iOS `IOS_PREDICATE` / `IOS_CLASS_CHAIN`
4. Text / label
5. XPath — last resort; justify in a comment

**Never invent locators.** Screenshots, Figma, and product/source code are
**flow/spec** only. Confirm every selector on a running app (`invoke ui:dump`
and/or Appium MCP) before treating a PO as final.

**Naming (PO fields):**

| Prefix | Kind | Example |
|--------|------|---------|
| `btn_` | Button / CTA | `btn_continue` |
| `input_` | Text field | `input_mobile` |
| `txt_` | Static label | `txt_title` |
| `msg_` | Error / toast | `msg_whitelist_error` |
| `chk_` | Checkbox / switch | `chk_terms` |
| `ddl_` | Dropdown | `ddl_org` |
| `lnk_` | Link | `lnk_view_payments` |
| `icn_` | Icon-only | `icn_kebab_menu` |
| `tab_` | Tab | `tab_groups` |
| `card_` | Card / list row | `card_member` |

Private attrs: `self._<prefix><name>_<strategy>` (`_acc`, `_uia`, `_ios`, `_text`, `_xpath`).  
Public API: `find_<prefix><name>()` → element; `loc_<prefix><name>()` → `(by, value)` for waits.  
Do **not** put strategy suffixes on `find_*` / `loc_*`.

UI dumps: `docs/locators/<screen>.xml` — **local only** (gitignored); do not commit.

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
`API_BASE_URL`, `TEST_MOBILE`, `OTP_GENERATE_PATH`, `OTP_VALIDATE_PATH`,
`NO_RESET`, `EXPLICIT_WAIT_TIMEOUT`

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
| `author-mobile-flow-docs` | Fallback intake → flow doc | `docs/<app_slug>-flow.md` |
| `extract-p0-test-cases` | Generate P0/P1/P2 cases (approval gated) | `docs/context/<app_slug>-<feature>-testcases.md` |
| `discover-mobile-locators` | Live UI dump / Appium MCP | `docs/locators/<screen>.xml` + locator sheet |
| `setup-mobile-test-data` | OTP, API seeding, credentials via `.env` | Test data ready |
| `automate-a-flow` | Orchestrate one approved scenario | Working E2E for one flow |
| `mobile-appium-python` | Write/edit layer files; flaky fixes | Layered automation files |

`automate-a-flow` = orchestration. `mobile-appium-python` = layer authoring.
Prefer `automate-a-flow` for “automate this”; use `mobile-appium-python` when
editing an existing layer or debugging locators/markers.

### Supporting (any time)

| Skill | When to use |
|-------|-------------|
| `read-test-reports` | Generate Allure HTML and triage failures |
| `review-changes` | Review against this **Repo contract** before merge |
| `author-pr-description` | Draft PR body from real branch diff |

### Pipeline

```text
# Preferred (app already configured, e.g. CoFee)
get-context
  → extract-p0-test-cases
  → discover-mobile-locators
  → setup-mobile-test-data
  → automate-a-flow
  → mobile-appium-python

# Fallback (no get-context this session)
author-mobile-flow-docs → extract-p0-test-cases → (same from discover onward)

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

Walkthrough steps: **`automate-a-flow`** and **`discover-mobile-locators`**.
Screenshots → `target/mcp-screenshots/` when `NO_UI=true`.

### Figma MCP

Design copy only — confirm locators via live dump. See **`get-context`**.

---

## Adding a feature (code order)

Use **`automate-a-flow`** for the full workflow. File order (patterns in
`mobile-appium-python`):

1. `src/page_objects/cofee/<screen>_po.py`
2. `src/page_actions/cofee/<screen>_actions.py`
3. `src/steps/cofee/<feature>_steps.py`
4. `tests/dataprovider/dp_<feature>.py`
5. `tests/test/cofee/<feature>/test_<feature>.py`
