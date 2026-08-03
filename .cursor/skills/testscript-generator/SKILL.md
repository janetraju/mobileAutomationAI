---
name: testscript-generator
description: >-
  Orchestrates an approved mobile test scenario into end-to-end Pytest+Appium
  automation—validates prerequisites, verifies the flow on a live device,
  then authors Page Objects, Actions, Steps, Data Providers, and Tests
  following the four-layer POM, verifies the run, and updates the flow doc.
  Use when the user asks to automate a feature or flow, starts a new E2E
  scenario with approved test cases, or needs to write/edit a single
  automation layer, fix a flaky test, or fix a locator.
---
# Testscript Generator

Orchestrate an approved test scenario into end-to-end mobile automation —
from environment validation through a live device walkthrough, layer
implementation, verification, and the flow-doc update.

Repository conventions (architecture, locators, waits, coding standards, etc.) are defined in `AGENTS.md`.

## When to Use

Use this skill when:

- A user asks to automate a feature or flow
- An approved test case exists
- Starting a new end-to-end automation scenario
- Writing or modifying Page Objects, Actions, Steps, Data Providers, or Tests
- Fixing flaky automation or locator issues
- Updating automation after UI changes

## Prerequisites

Before starting, ensure:

- `AGENTS.md`
- Approved `docs/context/<app_slug>-<feature>-testcases.md` *(if available)*
- `docs/<app_slug>-flow.md`
- `.env` (`APP_SLUG`, `PLATFORM`)

Never author Page Objects from product source, APK analysis, or Figma alone —
locators get confirmed live in Step 3.

Review existing automation before creating new files.

Search:

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

## Workflow

### Step 1 — Validate the Environment

Verify the automation environment.

```bash
invoke appium:doctor
```

```bash
invoke app:install
```

Confirm:

- Emulator or physical device is available
- Application is installed
- Login automation passes
- Test credentials are configured — see `AGENTS.md` → Test data & credentials
  for OTP strategy; availability was recorded in `get-context`'s intake

Run login automation first whenever the feature depends on an authenticated session.

---

### Step 2 — Understand the Scenario

Review the approved test case and identify:

- Feature
- Priority
- Preconditions
- Test data
- Expected behaviour
- Observable assertions

---

### Step 3 — Verify the Flow on Device

Every new scenario must be validated on a running application.

Run `discover-mobile-locators`.

Capture:

- Screens visited
- Confirmed UI text
- Verified locator strategy
- Navigation flow
- UI quirks or overlays
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

**Test data & OTP in dataproviders** — strategy table and security rules
live in `AGENTS.md` → Test data & credentials; don't restate them here.
Pull credentials from `.env` / settings (e.g. `TEST_MOBILE`, `TEST_OTP`) —
never hardcode a phone/OTP/token in the dataprovider.

Non-secret structured fixtures go under `data/<app_slug>/` when needed.

Framework fixtures (`driver`, `settings`, `mobile`, `otp`) are provided by `tests/conftest.py`.

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

Review the results using `generate-test-reports`.

If failures are caused by UI changes, refresh the UI dump rather than introducing additional waits.

---

### Step 6 — Resolve Common Issues

| Issue | Recommended Action |
|--------|--------------------|
| Stale element | Re-query the element after navigation |
| Element not found | Re-capture UI dump and verify locator priority |
| Loading spinner | Wait in the Actions layer |
| Keyboard overlap | Hide the keyboard before continuing |
| WebView | Switch context appropriately |
| Parallel execution | Use the appropriate `xdist_group` marker |

---

### Step 7 — Update flow doc (mandatory when tests pass)

After the new scenario **passes**, update `docs/<app_slug>-flow.md` (for CoFee:
`docs/cofee-flow.md`) so the board matches reality.

**Status table** — every automated scenario needs a complete row:

| Column | Requirement |
|--------|-------------|
| **ID** | Stable id — never blank or `—`. Reuse the approved TC/flow id if one exists; otherwise assign the next free id (`P0-06`, `P1-04`, …) |
| **Flow** | Short name matching what was automated (include TC ids if useful, e.g. HP-01) |
| **Status** | `**Done** — \`path/to/test_*.py\`` (or test function name if clearer) |

Also:

1. If the feature is **new**, add a short **Flows** blurb (happy path + variants), same style as Login / Create group / Enable partial payment.
2. Keep Not started / deferred cases visible (do not delete P1 rows just because a P0 shipped).
3. This skill owns the gate — do this even after a passing run.

**Checklist before finishing:**

```text
- [ ] Status row has a real ID (not empty)
- [ ] Status says Done + test path
- [ ] Flows section mentions the feature (if new or substantially changed)
```

---

### Step 8 — Capture reusable learnings

If implementation uncovers reusable framework or process improvements:

- Update the appropriate skill documentation.
- Record new **application-specific quirks** only if they are not already
  covered elsewhere (skills / POs); prefer a short note over duplicating
  long blocker tables.

---

## Output

Depending on the scenario: updated PO / actions / steps / dataprovider / tests; flow doc per Step 7; skill or quirk notes per Step 8.

---

## Rules

- Never automate a new scenario without a live device walkthrough.
- Never automate downstream flows before prerequisite flows pass.
- Reuse existing framework components whenever possible.
- Follow all framework conventions defined in `AGENTS.md` — do not redefine them here.
- Avoid introducing unnecessary waits to fix unstable tests.

---

## Known Pitfalls

Common process issues:

- `pm clear` invalidates the active UiAutomator2 session. Create a new Appium session after clearing app data.
- Emulator cold boots may take several minutes. Do not assume short startup times.
- Android autofill dialogs may intercept phone number fields and should be dismissed before interaction.

Application-specific issues belong in:

```
docs/<app_slug>-flow.md
```

---

## Next Steps

```text
testscript-generator
      ↓
generate-test-reports
      ↓
add-pr-description
      ↓
pr-review-changes
```

Prerequisites: `get-context`, `testcase-generator`, `discover-mobile-locators`. Repo contract: `AGENTS.md`.
