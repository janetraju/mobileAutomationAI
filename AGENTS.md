# Mobile Automation Framework — Agent Guide

Agent entry point for an **app-agnostic** Pytest + Appium + Allure mobile UI
automation framework. This file is written to be copied into **any** mobile
automation project — replace `<app_slug>` / `<APP_NAME>` with the project's
own values via `create-mobile-framework-structure`; nothing else here is
project-specific.

## Who this is for

The whole point of the skillset below is that **you do not need to write
code** to automate a mobile app. Every layer of automation (folder
structure, credentials, test cases, locators, Page Objects, reports, cleanup)
is produced or reviewed by a skill — your job is to answer each skill's
questions and approve what it proposes.

If you're a QA or anyone without a coding background: work through the
**Getting started** pipeline below, in order, one skill at a time. If you're
an engineer maintaining the framework itself: the **Repo contract** section
is the always-on rulebook every skill must follow when it generates code.

---

## Getting started (no coding required)

Run these skills **in order**. Skip a step only if its output already
exists (e.g. the app is already registered, or a credential strategy is
already documented).

| Step | Skill | What you do | What you get |
|------|-------|--------------|----------------|
| 1 | `mobile-env-doctor` | Nothing — run it and read the result | Confirmation the host/device/Appium stack can actually run automation right now |
| 2 | `create-mobile-framework-structure` | Provide the APK/IPA once per new app | App registered + folder skeleton — **one-time per app** |
| 3 | `get-mobile-context` | Answer questions / share a PRD, Figma, or walkthrough for the feature | A written feature context doc |
| 4 | `get-mobile-auth` | Pick how login/OTP should work in tests (fixed code, manual, or bypass) | Credentials wired up, nothing hardcoded |
| 5 | `mobile-test-data` | Decide where a feature's test data lives (once, if it needs backend records beyond login) | A documented data strategy — no silent accumulation |
| 6 | `mobile-test-design` | Review and approve the generated test cases (plain language, P0/P1/P2) | An approved test case list |
| 7 | `mobile-test-automation` | Confirm the flow on a live device when asked | Working, runnable automation — written for you |
| 8 | `mobile-test-report` | Nothing — just open the report | Pass/fail results with screenshots and logs |
| 9 | `mobile-coverage-audit` | Nothing — run any time | A coverage-gap report (missing categories, business rules, flow-index drift) |
| 10 | `pr-review-changes` | Nothing — run before merging | A code-compliance review against the Repo contract (blockers / should-fix / nits) |
| 11 | `add-pr-description` | Approve the drafted PR description before it's opened/updated | A PR opened or updated via `gh pr create` / `gh pr edit` |
| 12 | `teardown` | Nothing | Device/session reset, ready for the next run |
| — | `mobile-ci-pipeline` | Nothing — run once per app, whenever local execution stops being enough | A CI workflow running this suite instead of a shared dev machine |

Steps 1–5 happen once per app (or once per feature, for context/auth/data
changes) — though re-run `mobile-env-doctor` (step 1) any time a run feels
flaky for no code reason, not just once at the start. Steps 6–12 repeat for
every new feature or test run. `mobile-ci-pipeline` is a one-time setup
step, run whenever it makes sense for the project rather than at a fixed
point in the sequence.

You never need to open a code editor, write a locator, or touch Python to
complete this pipeline — that's what `mobile-test-automation` is for.

---

## How this repo is governed

| Document | Owns |
|----------|------|
| **`AGENTS.md`** (this file) | Always-on **repo contract** — architecture, layers, waits, assertions, stability, markers; locator *policy* (never invent; confirm live) |
| **`mobile-test-automation`** | Locator **priority, naming, dumps**, live UI-dump/MCP workflow, and layered code generation |
| **Other `.cursor/skills/*/SKILL.md`** | Task workflows only — do not restate repo contract |

Skills must **not** restate layer rules, wait policy, or markers — they
implement the contract below, they don't redefine it.

---

## Skills (execution helpers)

Canonical copies: `.cursor/skills/`. `.claude/skills/` are **symlinks** to the
same folders.

Each skill describes **only its own workflow**. Shared behavior lives in the
**Repo contract** below.

### Pipeline

```text
# Any time — before a big run, or the moment something feels flaky
mobile-env-doctor

# New app (once)
create-mobile-framework-structure

# Per feature
  → get-mobile-context
  → get-mobile-auth        (only if credentials/OTP strategy isn't set yet)
  → mobile-test-data       (only if the feature needs backend data beyond login)
  → mobile-test-design
  → mobile-test-automation
  → mobile-test-report
  → teardown

# Any time (standalone coverage snapshot — does not gate merging)
mobile-coverage-audit

# Once per app, whenever local execution stops being enough
mobile-ci-pipeline

# Before merging
pr-review-changes
  → add-pr-description
```

### Skill roles

| Skill | Role | Output / handoff |
|-------|------|-------------------|
| `mobile-env-doctor` | Diagnoses whether the host, device/simulator, and Appium stack are actually fit to run automation right now — resource pressure, a real input/render round-trip (not just "device is online"), driver/dependency version conflicts, platform-host readiness | Healthy / Degraded / Broken status per check, with a specific next action |
| `create-mobile-framework-structure` | Bootstraps a new app: APK/IPA analysis, `APP_REGISTRY`, `.env`, four-layer folder skeleton | Registered app + folder skeleton + `docs/<app_slug>-flow.md` stub |
| `get-mobile-context` | Feature intake from PRD, Figma, Jira, product source, or a walkthrough | `docs/context/<app_slug>-<feature>-context.md` |
| `get-mobile-auth` | Chooses & documents the OTP/credential strategy for the app; wires `.env` | `.env` vars + flow-doc *Known blockers / Test data* section |
| `mobile-test-data` | Decides how a feature's backend test data is created and cleaned up — isolated vs. shared fixtures, seeding, growth ceiling or reset | Documented **Test Data** section in `docs/<app_slug>-flow.md`, optional seed scripts under `data/<app_slug>/` |
| `mobile-test-design` | Generates P0/P1/P2 test cases for approval | `docs/context/<app_slug>-<feature>-testcases.md` |
| `mobile-test-automation` | Live UI dump/locator discovery **and** implements the approved scenario end-to-end; also the skill for editing a single layer file or fixing a flaky test/locator | Working E2E automation (layered files) |
| `mobile-test-report` | Generates Allure HTML and triages failures (screenshots, page source, logcat) | Allure report + triage notes |
| `mobile-coverage-audit` | Read-only report of test-design coverage gaps (missing categories, screens, business rules, flow-index drift) — does not review code against the Repo contract | `docs/context/<app_slug>-coverage-audit-report.md` |
| `mobile-ci-pipeline` | Packages the suite for CI (hardware-accelerated emulator/simulator, `mobile-env-doctor` checks, Allure artifact upload) instead of a shared dev machine | `.github/workflows/mobile-tests.yml` (or equivalent) |
| `pr-review-changes` | Reviews automation diffs for Repo-contract compliance (layer boundaries, locator policy, waits, markers, code quality) — does not check test-design coverage | Review notes (blocker / should-fix / nit), reported in conversation |
| `add-pr-description` | Drafts a reviewer-friendly PR description from the actual commits/diff, then opens/updates the PR after approval | PR created or updated via `gh pr create` / `gh pr edit` |
| `teardown` | Resets device/session/app state after a run so the next run starts clean | Clean environment for the next automation run |

---

## Stack

**Appium 2.x + Pytest + Python + Allure. Four-layer POM.**

- Sync `appium.webdriver.webdriver.WebDriver` API only — no async drivers
- Config: `python-dotenv` + Pydantic (`src/core/settings.py`)
- Task runner: `invoke` (`tasks.py`)
- App type is per-project: native / Flutter / React Native / hybrid — set via `APP_TYPE`

**Platform coverage status:** the Android path (UiAutomator2, `aapt`,
emulator/device workflow) has been exercised end-to-end against a real app
and is proven. The iOS path (XCUITest, IPA/`Info.plist` analysis, simulator
workflow) is implemented per Appium/Apple tooling conventions throughout
these skills but has **not** been run end-to-end on a real macOS host —
treat it as a well-reasoned starting point, not a verified capability, and
run `mobile-env-doctor` Step 4 before assuming an iOS bootstrap will just
work. iOS requires an actual macOS host with Xcode's command-line tools;
there is no simulator fallback on Linux/Windows.

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

Non-coders: this section is handled for you by `create-mobile-framework-structure`
and `mobile-test-automation` — you don't need to run these commands yourself
unless you're setting up a fresh machine.

## Invoke commands

| Task | Description |
|------|-------------|
| `invoke install` | Install Python deps (`pip install -e .`) |
| `invoke install-precommit` | Install git pre-commit hooks |
| `invoke emulator:start` | Start Android emulator + wait for device |
| `invoke app:analyze --apk=...` | Extract package/activity/type from an APK |
| `invoke app:analyze --ipa=...` | Extract bundle ID/executable from an IPA *(not yet proven against a real IPA)* |
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

## Directory tree (created by `create-mobile-framework-structure`)

```
src/
  core/                       # Framework base — no app imports upward
  page_objects/<app_slug>/    # Layer 1: locators only (*_po.py)
  page_actions/<app_slug>/    # Layer 2: interactions (*_actions.py)
  steps/<app_slug>/           # Layer 3: @allure.step orchestration
  constants/<app_slug>/       # Static strings (no secrets)
tests/
  conftest.py
  parallel_groups.py
  dataprovider/               # dp_<feature>.py
  test/<app_slug>/            # Layer 4: test_*.py
data/<app_slug>/               # Structured fixtures
docs/<app_slug>-flow.md        # Product flows — read before authoring tests
docs/context/                  # Feature context + approved testcases
target/ui-dumps/               # UI dumps from invoke ui:dump (local; under target/)
environment/                   # Per-env .properties overrides
tasks.py                       # invoke tasks (emulator, install, dump, test, report)
```

This tree is identical across every project using this framework — only the
`<app_slug>` folders and their contents differ per app.

---

## Repo contract (always-on)

Shared behavioral rules for every agent, skill, and contributor, on every
project using this framework. Skills implement *workflows*; they do not
redefine these rules. `mobile-test-automation` applies this section
automatically as it generates code; `pr-review-changes` reviews a diff
against it before merge — non-coders don't need to apply it by hand either
way. `mobile-coverage-audit` is a separate, read-only coverage-gap report
(test-design completeness) — it does not review code against this section.

### Architecture & layer boundaries

Import direction: **tests → steps → page_actions → page_objects → core**

| Layer | May call | Must not call |
|-------|----------|----------------|
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

Full priority order, PO naming (`btn_` / `find_*` / `loc_*`), and dump paths
are handled by **`mobile-test-automation`**.

### Wait & stability

- No `time.sleep()` — use explicit waits from `PageActions` / `BasePage`
- Use `EXPLICIT_WAIT_TIMEOUT` from settings — no magic timeouts
- Re-query elements after navigation / animation — no stale `WebElement` caching across screens
- Prefer left-biased taps when a known overlay (e.g. debug FAB) covers CTAs — document quirks in the flow doc

### Flakiness & reruns

`pytest-rerunfailures` may only mask **confirmed environment-level**
flakiness — run `mobile-env-doctor` first; if it reports Healthy, a rerun
hides a real bug instead of working around a real environment problem.

- A rerun is legitimate only after `mobile-env-doctor` has diagnosed the
  specific transient cause (host resource pressure, a known dependency
  conflict) — never applied by default "just in case"
- A test that needs a rerun on more than one run in a row is not flaky —
  it has a real, reproducible bug. Route it to `mobile-test-automation`
  instead of increasing `--reruns`
- Never silently increase the rerun count to make a red build green —
  that's the same failure mode as ignoring `mobile-env-doctor`'s Broken
  result and hoping the next run gets lucky

### Assertions

- Assertions belong in **tests** (via `assert_helper`) or thin step wrappers — not in page objects
- No `assert_helper` in page actions
- Assert **observable UI outcomes** (screen, copy, counts, amounts) — not just "navigation happened"
- On failure, Allure attachments (screenshot / page source) are handled in `conftest` — do not skip triage

### Tests, markers & Allure

Every UI test:

```python
@pytest.mark.e2e
@pytest.mark.p0  # or p1, p2
@pytest.mark.android  # or ios when platform-specific
@allure.epic("<APP_NAME>")
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

This section covers **login credentials** only. For a feature's other
backend data needs — a group, record, or account the flow interacts with —
see `mobile-test-data`; don't let a test invent its own ad hoc fixture
strategy just because it needs data unrelated to login.

An app may support **more than one** login method — mobile number + OTP,
email + password, Google/Gmail sign-in, or other SSO. `get-mobile-auth` sets
and documents a strategy for **each** one the app actually has, in
`docs/<app_slug>-flow.md` → Known blockers / Test data:

| Method | Strategy | Implementation |
|--------|----------|-----------------|
| Mobile + OTP | Fixed OTP in dev | Set `TEST_OTP` in `.env` / `.env.dev` (never commit) |
| Mobile + OTP | Manual | Mark test `@pytest.mark.manual_otp` or pause — avoid in CI |
| Mobile + OTP | Bypass | Deep link / `auth_profile` + `NO_RESET` session reuse |
| Email + password | Dedicated test account | `DEFAULT_USERNAME` / `DEFAULT_PASSWORD` in `.env` |
| Google/Gmail, other SSO | Pre-authorized device account (preferred) | Test account already signed in on the device/emulator/CI image — never store the real provider password in `.env` |
| Google/Gmail, other SSO | Bypass | Deep link / `auth_profile` + `NO_RESET` session reuse |
| Google/Gmail, other SSO | Manual (last resort) | Avoid in CI; automating a provider's real consent UI is fragile and may violate its ToS |

- Credentials live in `.env`/`.env.<env>` only — never in a committed context/flow doc, dataprovider, PO, or step
- No production credentials, and no real personal SSO accounts — dev/stg/uat test accounts only
- Fail fast if `TEST_MOBILE` is missing when OTP login tests are collected
- Backend/SQL assertions: keep queries in `data/<app_slug>/` scripts — never in page layers

### Feature context vs automation

| Input | Role |
|-------|------|
| Screenshots / walkthrough / Figma / product repo / PRD | **Flow spec** (what to automate) |
| Live device dump / Appium MCP | **Locator source of truth** (how to find elements) |

Read `docs/<app_slug>-flow.md` (and `docs/context/` when present) before
writing tests. Do not invent flows or selectors not documented **or**
inspected on device.

---

## Key `.env` variables

`APP_NAME`, `APP_SLUG`, `APP_TYPE`, `APP_ENV`, `PLATFORM`, `APPIUM_HOST`,
`APPIUM_PORT`, `DEVICE_NAME`, `APP_PATH`, `APP_PACKAGE`, `APP_ACTIVITY`,
`API_BASE_URL`, `TEST_MOBILE`, `TEST_OTP`, `DEFAULT_USERNAME`,
`DEFAULT_PASSWORD`, `FEATURE_ORG_ID`, `FEATURE_ACCOUNT_ID`, `NO_RESET`,
`EXPLICIT_WAIT_TIMEOUT`

All of the above are set for you by `create-mobile-framework-structure` and
`get-mobile-auth` — this list is a reference, not a manual setup checklist.

---

## MCP Tools

### Appium MCP (project-local)

| File | Purpose |
|------|---------|
| `.mcp.json` | MCP server config (`npx appium-mcp@…`) |
| `environment/appium-mcp.capabilities.json` | Caps — keep aligned with `.env` |

**Prerequisites:** `ANDROID_HOME`, device/emulator up, `invoke appium:install-drivers`.
**Enable:** restart the editor / reload MCP → toggle **appium-mcp**.

Walkthrough steps live in **`mobile-test-automation`**. Screenshots →
`target/mcp-screenshots/` when `NO_UI=true`.

### Figma MCP

Design copy only — confirm locators via live dump. See **`get-mobile-context`**.

---

## Adding a feature (code order)

`mobile-test-automation` follows this file order automatically:

1. `src/page_objects/<app_slug>/<screen>_po.py`
2. `src/page_actions/<app_slug>/<screen>_actions.py`
3. `src/steps/<app_slug>/<feature>_steps.py`
4. `tests/dataprovider/dp_<feature>.py`
5. `tests/test/<app_slug>/<feature>/test_<feature>.py`
