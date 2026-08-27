---
name: mobile-test-automation
description: >-
  Confirms locators live on a running app via ui:dump and Appium MCP, then
  implements the approved test scenario end-to-end across the four-layer POM
  (Page Objects, Actions, Steps, Data Providers, Tests) and runs it. Also the
  skill for editing a single layer file, refreshing a stale locator, or
  fixing a flaky test. Owns locator priority, PO naming, and dump paths per
  AGENTS.md. Use when automating a feature or flow, starting a new E2E
  scenario with an approved test case, or fixing a locator/layer issue.
---

# Mobile Test Automation

Confirm every locator live on a running application, then implement an
approved test scenario end-to-end across the four-layer POM, and run it.

AGENTS.md delegates locator **priority, naming, dumps, and the live
UI-dump/MCP workflow** to this skill — that detail is owned here, not
restated in AGENTS.md. Everything else (layer boundaries, waits, assertions,
markers, credential rules) is defined in `AGENTS.md` — this skill implements
that contract, it does not redefine it.

## When to Use

Use this skill when:

- Automating a feature or flow with an approved test case
- Creating a new `*_po.py` file or starting a new E2E scenario
- Editing a single layer file (Page Object, Actions, Steps, Data Provider, Test)
- UI changes have invalidated existing locators — refreshing a stale dump
- Fixing a flaky test caused by a locator, wait, or layer/import violation

## Prerequisites

Before starting, confirm:

- `create-mobile-framework-structure` has run — app registered, folders exist
- `docs/context/<app_slug>-<feature>-context.md` from `get-mobile-context` *(if available)*
- Credential strategy set by `get-mobile-auth` for every login method the
  scenario depends on
- Approved `docs/context/<app_slug>-<feature>-testcases.md` from `mobile-test-design`
- `docs/<app_slug>-flow.md`
- `.env` (`APP_SLUG`, `PLATFORM`)

Never author Page Objects from product source, APK analysis, or Figma alone —
every locator is confirmed live in Step 3.

Review existing automation before creating new files:

```text
src/page_objects/<app_slug>/
src/page_actions/<app_slug>/
src/steps/<app_slug>/
tests/dataprovider/
tests/test/<app_slug>/
docs/context/
target/ui-dumps/   # local dumps from invoke ui:dump
```

Reuse existing implementation whenever possible.

---

## Locator strategy (source of truth)

### Priority (highest first)

1. `AppiumBy.ACCESSIBILITY_ID` / content-desc
2. Android `ANDROID_UIAUTOMATOR` / resource-id
3. iOS `IOS_PREDICATE` / `IOS_CLASS_CHAIN`
4. Text / label
5. XPath — last resort; justify in a comment

### Naming (PO fields)

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

### Dumps

`target/ui-dumps/<screen>.xml` — **local only** (under `target/`); do not
commit. iOS: `target/ui-dumps/<screen>_ios.xml`.

### Preference by app type

| APP_TYPE | Preferred locator |
|----------|-------------------|
| `flutter` | `content-desc` / Semantics |
| `rn` | `testID` / `accessibilityLabel` |
| `hybrid` | Native hierarchy (WebView only when required) |
| `native` | `resource-id` |

---

## Workflow

### Step 1 — Validate the Environment

```bash
invoke appium:doctor
invoke app:install
```

Confirm:

- Emulator or physical device is available
- Application is installed
- Login automation passes
- Test credentials are configured — strategy per method comes from
  `get-mobile-auth`, recorded in `docs/<app_slug>-flow.md` → Known blockers / Test data

Run login automation first whenever the feature depends on an authenticated
session.

---

### Step 2 — Understand the Scenario

Review the approved test case from `mobile-test-design` and identify:

- Feature
- Priority
- Preconditions
- Test data
- Expected behaviour
- Observable assertions

---

### Step 3 — Confirm Locators Live on Device

Every new scenario must be validated on a running application. This step is
mandatory — do not begin implementation without it.

1. **Capture static UI dumps**

   ```bash
   adb shell am start -n <APP_PACKAGE>/<APP_ACTIVITY>
   invoke ui:dump --screen=<screen_name>   # → target/ui-dumps/<screen_name>.xml
   ```

   Repeat per screen.

2. **Walk the flow with Appium MCP**

   - `select_device` → `appium_session_management` (`action=create`)
   - Navigate with `appium_gesture` / `appium_set_value` / `appium_find_element`
   - Per screen: screenshot → page source → save XML → `generate_locators`
   - Confirm every generated locator against page source and visible UI

   | Scenario | Action |
   |----------|--------|
   | Fresh login | Clear app data and relaunch |
   | Logged-in session | Reuse the existing session |
   | Downstream flow | Complete login before continuing |

   Screenshots when `NO_UI=true`: `target/mcp-screenshots/`. Re-dump after
   animations, keyboard, or navigation.

3. **Capture, for handoff into Step 4**:

   - Screens visited, in order
   - Confirmed UI text
   - Verified locator strategy per screen (per priority order above)
   - Navigation flow, quirks, or overlays
   - Differences from the documented flow

Do not begin implementation until the live walkthrough is complete.

---

### Step 4 — Implement the Layers

Follow the standard implementation order:

```text
Page Objects
      ↓
Actions
      ↓
Steps
      ↓
Data Provider
      ↓
Tests
```

| Layer | Location | Responsibility |
|--------|----------|----------------|
| Page Objects | `src/page_objects/<app_slug>/` | Locators and element access |
| Actions | `src/page_actions/<app_slug>/` | User interactions |
| Steps | `src/steps/<app_slug>/` | Business workflows |
| Data Provider | `tests/dataprovider/` | Test data |
| Tests | `tests/test/<app_slug>/` | Test scenarios and assertions |

Layer boundaries and import rules are defined in `AGENTS.md`. Reuse existing
framework components whenever possible.

**Test data & credentials in dataproviders** — strategy table lives in
`AGENTS.md` → Test data & credentials; don't restate it here. Pull
credentials from `.env` / settings (e.g. `TEST_MOBILE`, `TEST_OTP`,
`DEFAULT_USERNAME`) — never hardcode a phone/OTP/password/token in the
dataprovider.

Non-secret structured fixtures go under `data/<app_slug>/` when needed.

Framework fixtures (`driver`, `settings`, `mobile`, `otp`) are provided by
`tests/conftest.py`.

---

### Step 5 — Verify

Run:

```bash
invoke lint
```

```bash
invoke test --markers "login and p0"
```

```bash
invoke test --markers "<feature>"
```

```bash
invoke test --markers "e2e and p0"
```

Hand off to `mobile-test-report` to review results.

If failures are caused by UI changes, refresh the UI dump (Step 3) rather
than introducing additional waits.

---

### Step 6 — Resolve Common Issues

| Issue | Recommended Action |
|--------|--------------------|
| Stale element | Re-query the element after navigation |
| Element not found | Re-capture UI dump and verify locator priority |
| Loading spinner | Wait in the Actions layer |
| Keyboard overlap | Hide the keyboard before continuing |
| WebView | Switch context appropriately |
| Parallel execution | Use the appropriate `PARALLEL_GROUP_*` marker |

---

### Step 7 — Update Flow Doc (mandatory when tests pass)

After the new scenario **passes**, update `docs/<app_slug>-flow.md` so the
board matches reality.

**Status table** — every automated scenario needs a complete row:

| Column | Requirement |
|--------|-------------|
| **ID** | Stable id — never blank or `—`. Reuse the approved TC/flow id if one exists; otherwise assign the next free id (`P0-06`, `P1-04`, …) |
| **Flow** | Short name matching what was automated (include TC ids if useful) |
| **Status** | `**Done** — \`path/to/test_*.py\`` (or test function name if clearer) |

Also:

1. If the feature is **new**, add a short **Flows** blurb (happy path + variants).
2. Keep Not started / deferred cases visible (do not delete rows just because one shipped).
3. This skill owns the gate — do this even after a passing run.

**Checklist before finishing:**

```text
- [ ] Status row has a real ID (not empty)
- [ ] Status says Done + test path
- [ ] Flows section mentions the feature (if new or substantially changed)
```

---

### Step 8 — Hand Off / Capture Reusable Learnings

Hand off to `mobile-test-report` for pass/fail results, then `teardown` to
reset device state before the next run.

If implementation uncovers reusable framework or process improvements:

- Update the appropriate skill documentation.
- Record new **application-specific quirks** only if not already covered
  elsewhere (skills / POs); prefer a short note over duplicating long
  blocker tables.

---

## Output

Depending on the scenario: locator-confirmed PO / actions / steps /
dataprovider / tests; flow doc update per Step 7; skill or quirk notes per
Step 8.

---

## Rules

- Never invent locators from APK / product source / Figma alone.
- Never automate a new scenario without a live device walkthrough.
- Never automate downstream flows before prerequisite flows pass.
- Never commit generated UI-dump XML files.
- Reuse existing framework components whenever possible.
- Follow all framework conventions defined in `AGENTS.md` — do not redefine them here.
- Avoid introducing unnecessary waits to fix unstable tests.

---

## Known Pitfalls

Common process issues:

- `pm clear` invalidates the active UiAutomator2 session. Create a new Appium session after clearing app data.
- Emulator cold boots may take several minutes. Do not assume short startup times.
- Android autofill dialogs may intercept phone number fields and should be dismissed before interaction.

Application-specific issues belong in `docs/<app_slug>-flow.md`, not here.

---

## Related Skills

```text
create-mobile-framework-structure → get-mobile-context → get-mobile-auth → mobile-test-design
      ↓
mobile-test-automation
      ↓
mobile-test-report → teardown
```

Runs any time before merging: `mobile-coverage-audit`. Repo contract: `AGENTS.md`.
