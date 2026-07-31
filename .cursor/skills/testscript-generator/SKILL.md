---
name: testscript-generator
description: >-
  Authors and maintains Page Objects, Actions, Steps, Data Providers, and Tests
  following the four-layer POM. Use when writing or editing automation layers,
  fixing flaky tests or locators, or updating automation after UI changes. For
  full feature automation from scratch, prefer automate-a-flow.
---
# Testscript Generator

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

**Test data & OTP in dataproviders** — strategy table and security rules
live in `AGENTS.md` → Test data & credentials; don't restate them here.
Usage in a dataprovider/fixture:

```python
from src.core.api_client import generate_otp, validate_otp, ApiClient
generate_otp("+919876543210")
```

Non-secret structured fixtures go under `data/<app_slug>/`:

```
data/<app_slug>/
  users.example.json      # structure only, committed
  users.json               # gitignored if it contains real data
  org_setup.example.json
```

Encrypt at rest if secrets must live in the repo; decrypt via an env key
(document in README). Never hardcode a phone/OTP/token in the dataprovider
itself — pull from env or `data/<app_slug>/`.

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

When a P0 scenario is automated, update status in `docs/<app_slug>-flow.md` — see **`automate-a-flow`** Step 6 (that skill owns the gate).

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

## Next Steps

Depending on the workflow: run tests → `read-test-reports` for failures → update flow doc via `automate-a-flow` Step 6 → `add-pr-description` / `pr-review-changes`.

Related: `automate-a-flow`, `discover-mobile-locators`.