# Automate a Flow

Orchestrate an approved test scenario into end-to-end mobile automation.

This skill coordinates the automation workflow. It validates prerequisites, ensures the feature is verified on a running device, and hands implementation to `mobile-appium-python`.

Repository conventions (architecture, locators, waits, coding standards, etc.) are defined in `AGENTS.md`.

## When to Use

Use this skill when:

- A user asks to automate a feature or flow
- An approved test case exists
- Starting a new end-to-end automation scenario

> For changes limited to Page Objects, Actions, Steps, or Tests, use `mobile-appium-python`.

## Prerequisites

Before starting, ensure:

- `AGENTS.md`
- Approved `docs/context/<app_slug>-<feature>-testcases.md`
- `docs/<app_slug>-flow.md`

Review existing automation before creating new files.

Search:

```text
src/page_objects/<app_slug>/
src/page_actions/<app_slug>/
src/steps/<app_slug>/
tests/dataprovider/
tests/test/<app_slug>/
docs/context/
docs/locators/
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

### Step 4 — Implement the Automation

Hand off implementation to:

```text
mobile-appium-python
```

Standard implementation order:

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

Reuse existing framework components whenever possible.

---

### Step 5 — Verify

Run:

```bash
invoke test --markers "login and p0"
```

```bash
invoke test --markers "<feature>"
```

```bash
invoke test --markers "e2e and p0"
```

Review the results using `read-test-reports`.

If failures are caused by UI changes, refresh the UI dump rather than introducing additional waits.

---

### Step 6 — Capture Reusable Learnings

If implementation uncovers reusable framework or process improvements:

- Update the appropriate skill documentation.
- Record application-specific issues in:

```
docs/<app_slug>-flow.md
```

---

## Output

Depending on the scenario:

- Updated Page Objects
- Updated Actions
- Updated Steps
- Updated Data Providers
- Updated Tests
- Updated flow documentation (when applicable)

---

## Rules

- Never automate a new scenario without a live device walkthrough.
- Never automate downstream flows before prerequisite flows pass.
- Reuse existing framework components whenever possible.
- Do not redefine repository conventions from `AGENTS.md`.
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
automate-a-flow
      ↓
mobile-appium-python
      ↓
read-test-reports
      ↓
author-pr-description
```

---

## Related Skills

- `get-context`
- `testcase-generator`
- `discover-mobile-locators`
- `mobile-appium-python`
- `read-test-reports`
- `author-pr-description`
- `pr-review-changes`
- `AGENTS.md`