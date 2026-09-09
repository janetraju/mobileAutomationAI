---
name: mobile-test-automation
description: >-
  Implements an approved test scenario end-to-end across the four-layer POM
  (Page Objects, Actions, Steps, Data Providers, Tests) and runs it, once
  discover-mobile-locators has confirmed locators live on a running app. Also
  the skill for editing a single layer file or fixing a flaky test caused by
  a wait or layer/import issue. Use when automating a feature or flow with
  confirmed locators, or fixing a layer issue.
---

# Mobile Test Automation

Implement an approved test scenario end-to-end across the four-layer POM,
once locators are confirmed live via `discover-mobile-locators`, and run it.

Locator **priority, naming, dumps, and the live UI-dump/MCP workflow** are
owned by `discover-mobile-locators` — this skill consumes its confirmed
handoff, it does not rediscover locators itself. Everything else (layer
boundaries, waits, assertions, markers, credential rules) is defined in
`AGENTS.md` — this skill implements that contract, it does not redefine it.

## When to Use

Use this skill when:

- Automating a feature or flow with an approved test case
- Creating a new `*_po.py` file or starting a new E2E scenario
- Editing a single layer file (Page Object, Actions, Steps, Data Provider, Test)
- A layer file needs updating once `discover-mobile-locators` has refreshed a stale locator
- Fixing a flaky test caused by a wait or layer/import violation

## Prerequisites

Before starting, confirm:

- `create-mobile-framework-structure` has run — app registered, folders exist
- `docs/context/<app_slug>-<feature>-context.md` from `get-mobile-context` *(if available)*
- Credential strategy set by `get-mobile-auth` for every login method the
  scenario depends on
- Approved `docs/context/<app_slug>-<feature>-testcases.md` from `mobile-test-design`
- `docs/<app_slug>-flow.md`
- `.env` (`APP_SLUG`, `PLATFORM`)
- Locators for this scenario's screens confirmed live via `discover-mobile-locators`

Never author Page Objects from product source, APK analysis, or Figma alone —
every locator must come from a `discover-mobile-locators` handoff (Step 3).

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

Mandatory for every new scenario — do not begin implementation without it.

Run **`discover-mobile-locators`** for the screens this scenario touches. It
owns the UI-dump/Appium MCP walkthrough, the locator priority order, and PO
naming — see that skill for the full workflow; it is not restated here.

Take from its handoff into Step 4:

- Screens visited, in order
- Confirmed UI text
- Verified locator strategy per screen
- Navigation flow, quirks, or overlays
- Differences from the documented flow

Do not begin implementation until `discover-mobile-locators` has handed off
confirmed locators.

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
| Element not found | Re-run `discover-mobile-locators` for that screen — do not guess a fix here |
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

Depending on the scenario: PO / actions / steps / dataprovider / tests built
on locators `discover-mobile-locators` confirmed; flow doc update per Step 7;
skill or quirk notes per Step 8.

---

## Rules

- Never author a locator here — every one comes from a `discover-mobile-locators` handoff.
- Never automate a new scenario before `discover-mobile-locators` has completed its live walkthrough.
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
discover-mobile-locators
      ↓
mobile-test-automation
      ↓
mobile-test-report → teardown
```

Runs any time before merging: `mobile-coverage-audit`. Repo contract: `AGENTS.md`.
