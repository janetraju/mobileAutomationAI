# Mobile Appium Python

Implement and maintain the mobile automation framework by authoring Page Objects, Actions, Steps, Data Providers, and Tests.

Repository conventions (layer boundaries, locators, waits, markers, and code quality) are defined in `AGENTS.md`. This skill focuses only on the implementation workflow.

## When to Use

Use this skill when:

- Creating or updating automation for a feature
- Writing or modifying Page Objects, Actions, Steps, Data Providers, or Tests
- Fixing flaky automation or locator issues
- Updating automation after UI changes

> For complete feature automation (context → test cases → locator discovery → implementation), start with `automate-a-flow`.

## Prerequisites

Before implementation, ensure the following are available:

- `AGENTS.md`
- `.env` (`APP_SLUG`, `PLATFORM`)
- `docs/<app_slug>-flow.md`
- Approved `docs/context/<app_slug>-<feature>-testcases.md` *(if available)*
- Live-confirmed locators from `discover-mobile-locators`

Never author Page Objects from product source, APK analysis, or Figma alone.

---

## Workflow

### Step 1 — Review the Feature

Understand:

- Feature flow
- Approved test cases
- Confirmed UI locators
- Existing automation

Reuse existing implementation where appropriate.

---

### Step 2 — Implement the Layers

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

Layer boundaries and import rules are defined in `AGENTS.md`.

---

### Step 3 — Validate on Device

When implementation is based on product documentation:

1. Confirm the feature flow.
2. Confirm approved test cases.
3. Confirm live UI locators.
4. Implement all framework layers.
5. Execute on a real device or emulator.
6. Resolve failures using screenshots and page source.

---

### Step 4 — Verify

Run:

```bash
invoke lint
```

```bash
invoke test --markers "<feature markers>"
```

When a P0 scenario is automated, update the automation status in:

```
docs/<app_slug>-flow.md
```

---

### Step 5 — Resolve Common Issues

| Issue | Recommended Action |
|--------|--------------------|
| Stale element | Re-query the element after navigation |
| Element not found | Re-capture UI dump and verify locator priority |
| Loading spinner | Wait in the Actions layer |
| Keyboard overlap | Hide the keyboard before continuing |
| WebView | Switch context appropriately |
| Parallel execution | Use the appropriate `xdist_group` marker |

Framework fixtures (`driver`, `settings`, `mobile`, `otp`) are provided by `tests/conftest.py`.

---

## Output

Depending on the requested work, create or update:

- `src/page_objects/...`
- `src/page_actions/...`
- `src/steps/...`
- `tests/dataprovider/...`
- `tests/test/...`

---

## Rules

- Follow all framework conventions defined in `AGENTS.md`.
- Never access `driver.find_element()` outside Page Objects.
- Tests should interact only with Steps.
- Steps should interact only with Actions.
- Actions should interact only with Page Objects.
- Never use `time.sleep()`; use the project's wait utilities.

## Next Steps

Depending on the workflow:

- Run the automated tests
- Update the flow documentation
- Generate a PR using `author-pr-description`

## Related Skills

- `automate-a-flow`
- `discover-mobile-locators`
- `setup-mobile-test-data`
- `read-test-reports`
- `pr-review-changes`