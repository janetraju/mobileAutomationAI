---
name: automate-a-flow
description: >-
  Orchestrate turning an approved test case or scenario into working E2E
  automation: validate prereqs, walk the flow on device via Appium MCP, then
  hand off layer coding to mobile-appium-python. Use when the user says
  "automate this", "implement this flow", or gives a TC to automate — not for
  editing a single PO/step file (use mobile-appium-python for that).
disable-model-invocation: true
---

# Automate a Flow

**Orchestrator** for a full scenario.  
**Repo contract:** [AGENTS.md](../../../AGENTS.md) (layers, locators, waits, markers).  
Layer file patterns: **`mobile-appium-python`**. This skill decides *when* /
*in what order*; that skill decides *how* each file looks.

Use when the user gives a **test scenario**, **approved test case**, or
**"automate this flow"** request.

## Goal

Turn a business scenario into layered automation using **real** locators from
dumps / Appium MCP (per AGENTS.md — never invent selectors).

## Read first

1. **`AGENTS.md` Repo contract**
2. **`docs/context/<app_slug>-<feature>-testcases.md`** (if approved) or flow doc P0 row
3. **`docs/<app_slug>-flow.md`**
4. Existing POs, actions, steps under `src/` and `tests/test/<app_slug>/`

## Step 0 — Validate prerequisites (before writing code)

**Never author a downstream flow test (e.g. groups, payments) until upstream
prerequisites pass on a real device/emulator.**

| Precondition | Verify with |
|---|---|
| Emulator + Appium | `invoke appium:doctor` · `AVD_NAME` in `.env` (or single-AVD auto-detect) |
| Android boot complete | `scripts/wait-for-device.sh` waits for `sys.boot_completed` + `settings` service |
| App installed | `invoke app:install` · `APP_PATH` in `.env` |
| Login P0 | Login tests pass on clean emulator |
| Logged-in home (if required) | `invoke ui:dump --screen=home_logged_in` · confirm target tile locators |
| Test credentials | `TEST_MOBILE` whitelisted on dev API · `TEST_OTP` in `.env` |

If the new flow depends on login, run login first — do not assume
`user_ensures_logged_in_home` masks infra or locator gaps.

## Step 1 — Parse the scenario

| Item | Example |
|---|---|
| Feature area | `login`, `groups`, `payments` |
| Priority | `p0`, `p1`, `p2` |
| Steps | From approved testcases or `docs/<app_slug>-flow.md` |
| Assertions | Success criteria in test case / flow doc |
| Test data | `.env` or `tests/dataprovider/dp_<feature>.py` |
| Platform | `android` / `ios` |
| Pre-conditions | Logged in? account type? |

Search before creating:

```text
src/page_objects/<app_slug>/   src/page_actions/<app_slug>/   src/steps/<app_slug>/
tests/dataprovider/            tests/test/<app_slug>/         docs/locators/
docs/context/
```

**App source** (when flow doc is stale): read `reference/<app_slug>-app-source/`
— routes, `en_us.dart`, onboarding modules. Repo informs **what**; device dump
locks **how**.

Reuse existing steps (e.g. `user_ensures_logged_in_home` before group flows).

## Step 2 — Gather context (strict order)

### 2a. Context file + flow doc + repo (always first)

1. Read approved test cases or flow doc P0 matrix.
2. Grep for existing POs, actions, steps, tests for the feature.
3. Note gaps: missing locators, navigation, assertions.

### 2b. Figma / Jira (when available from `get-context`)

Use MCP only for artifacts collected in intake — for **expected copy**, not
locator source of truth.

### 2c. Locator dump (`invoke ui:dump`)

Follow **`discover-mobile-locators`** for static snapshots:

```bash
invoke appium:doctor
invoke emulator:start
invoke app:install
invoke ui:dump --screen=<name>    # → docs/locators/<name>.xml (local only)
```

Use for quick single-screen dumps. For new test cases, Step 2d is still required.

### 2d. Verify flow on device via Appium MCP (mandatory before new TC)

**Do not add a new test scenario or implementation until the flow is walked on a
real device/emulator through Appium MCP.**

This step confirms navigation, copy, overlays, and locators before any
`*_po.py`, steps, or `test_*.py` changes.

Configured in `.cursor/mcp.json` → [appium/appium-mcp](https://github.com/appium/appium-mcp).
Caps live in `environment/appium-mcp.capabilities.json` (keep aligned with `.env`).

#### Session setup

1. Ensure emulator/device is booted and app is installed (`invoke emulator:start` · `invoke app:install`).
2. Align caps with `.env` — update `environment/appium-mcp.capabilities.json` if
   `DEVICE_NAME`, `APP_PACKAGE`, or `PLATFORM_VERSION` changed.
3. Call MCP tools in order:
   - `select_device` (platform from `.env`)
   - `appium_session_management` with `action=create` (embedded mode — no
     `remoteServerUrl` unless the user provides one)
4. If MCP auth is needed, call `mcp_auth` once, then retry.

**Enable:** Restart Cursor (or reload MCP) after cloning — toggle **appium-mcp**
under Customize → MCP. Requires `ANDROID_HOME` and `invoke appium:install-drivers`.

#### Walk the scenario

For each step in the parsed scenario:

1. Navigate to the screen (tap, type, scroll via `appium_gesture`,
   `appium_set_value`, `appium_find_element`).
2. `appium_screenshot` — saved under `target/mcp-screenshots/` when `NO_UI=true`.
3. `appium_get_page_source` — save to `docs/locators/<screen>.xml` when the
   screen is new or locators may have drifted.
4. `generate_locators` on key screens — **confirm every suggestion** against
   page source and app strings (`en_us.dart` / Semantics) before PO authoring.
5. Note blockers: permission dialogs, Google picker, debug FAB, org picker,
   network errors.

Handle preconditions the same way the test will:

| Precondition | MCP action |
|---|---|
| Fresh login | `appium_app_lifecycle` `action=clear` on `APP_PACKAGE`, then relaunch |
| Logged-in home | Walk login first, or reuse session if already on home |
| Downstream flow (groups, payments) | Confirm login P0 passes before walking |

### Deliverable before coding

Summarize for the user (or in PR notes):

```text
- Screens visited (in order)
- Key UI strings confirmed
- Locator notes per screen (strategy + value)
- Overlays / quirks observed
- Gaps vs flow doc (update docs/<app_slug>-flow.md if needed)
```

Only after this summary → proceed to Step 3.

## Step 3 — Implement layers

Follow **`mobile-appium-python`** feature add order (and **AGENTS.md** contract
for what each layer may contain):

```text
src/page_objects/<app_slug>/<screen>_po.py
src/page_actions/<app_slug>/<screen>_actions.py
src/steps/<app_slug>/<feature>_steps.py
tests/dataprovider/dp_<feature>.py
tests/test/<app_slug>/<feature>/test_<feature>.py
```

**Checklist:**

```text
- [ ] MCP flow walkthrough completed (Step 2d)
- [ ] Context sources noted (testcases / flow doc / MCP dump)
- [ ] Locators live-confirmed (AGENTS.md)
- [ ] Steps before test file
- [ ] Markers / Allure per AGENTS.md
```

## Step 4 — Verify

**Order matters** — run upstream tests before the new feature:

```bash
invoke lint                                   # auto-fix (default)
invoke test --markers "login and p0"          # login P0 must pass first
invoke test --markers "<new_feature_marker>"  # then the new flow
invoke test --markers "e2e and p0"
invoke report
```

`invoke test` always runs **ruff --fix + black** before pytest. Use
`invoke lint --no-fix` only when you need a check-only pass.

Re-dump failing screen. Waits/stability: **AGENTS.md** (no `time.sleep()`).

## Step 5 — On failure: update skills (mandatory)

When an E2E run fails, **do not only patch code** — update the relevant
skill(s) so the same class of failure is prevented next time.

| Failure layer | Update skill | What to record |
|---|---|---|
| Emulator / AVD / boot / Appium | `mobile-appium-python`, `onboard-mobile-app` | AVD name, boot wait, timeout values |
| Locator / Flutter semantics | `discover-mobile-locators` | text vs content-desc, conditional labels, dump path |
| Login / onboarding / OTP | `discover-mobile-locators`, `automate-a-flow` | carousel coords, CTA timing, picker overlays |
| Assertion / step wiring | `review-changes`, `mobile-appium-python` | import violations, step reuse |
| Triage / artifacts | `read-test-reports` | new failure signatures |

**Update format** — append a dated bullet under **Known pitfalls** in the
affected skill:

```markdown
### Known pitfalls (updated YYYY-MM-DD)
- **Symptom:** `Can't find service: settings` on session start
  **Cause:** Appium connected before Android boot finished
  **Fix:** Wait for `sys.boot_completed=1` in `wait-for-device.sh`
```

Also update `docs/<app_slug>-flow.md` blocker table when the failure reveals a
new quirk.

Only skip skill updates when the failure is a one-off env issue (e.g. user
unplugged device) — not framework or locator knowledge.

## Decision matrix

| Situation | Action |
|---|---|
| Steps already exist | Compose in test; extend dataprovider only |
| New screen | Dump → PO → Actions → Steps → test |
| Locator drift | Update one PO field; grep duplicates |
| Multi-screen | One step module; steps call multiple actions |
| iOS + Android | Same steps; platform POs if tree differs |

## Anti-patterns (orchestration-specific)

Repo-wide anti-patterns (sleeps, invented locators, layer violations) → **AGENTS.md**.

- Adding a new TC without MCP flow walkthrough (Step 2d)
- Authoring downstream tests (groups, payments) before login P0 passes
- Fixing code without updating the relevant skill after a failure
- Skipping Step 0 prereq validation

## Known pitfalls (CoFee — updated 2026-07-16)

- **`pm clear` mid-session kills UiAutomator2:** Cold-start login while a session
  is alive often yields `instrumentation process is not running` on the next
  `get_window_size`. Quit session → `adb pm clear` + seed intro + launch →
  recreate driver → login with session reuse helpers.
- **Post-OTP wait must ignore lingering OTP:** Pollers must only accept
  `home`/`org`, not `"otp"` while the OTP screen is still visible.
- **Org switch → home:** Continue can miss under the debug FAB; use left-biased
  taps and retry while org screen remains. Home detection must require CoFee nav
  (`Groups`/`Payments`), not launcher `Home` alone.
- **Onboarding carousel:** Prefer seeding `hasIntroScreenShown` via adb after
  `pm clear` — wrong tap coords skip all intro slides.
- **Home create-group tile:** Flutter semantics → `ACCESSIBILITY_ID` /
  `descriptionMatches` for **Add New** / **Create group**.
- **Phone submit:** wait for clickable **Continue** before tap; dismiss Google
  phone-picker; OTP needs API/network + whitelisted `TEST_MOBILE`.
- **Emulator:** set `AVD_NAME` in `.env`; cold boot can exceed 180s — use 300s
  device wait.
- **Member fee assert:** UI shows Indian-formatted amounts with newlines — use
  one `descriptionMatches("(?s).*…*")`, not chained `descriptionContains`.

## Related skills

`get-context` · `extract-p0-test-cases` · `discover-mobile-locators` ·
`setup-mobile-test-data` · `mobile-appium-python` · `read-test-reports` ·
`review-changes` · [AGENTS.md](../../../AGENTS.md)
