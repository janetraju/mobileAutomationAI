---
name: author-mobile-flow-docs
description: >-
  Document mobile app user flows from screenshots, walkthroughs, or Figma into
  docs/<app_slug>-flow.md. Use before extract-p0-test-cases or
  discover-mobile-locators when adding a new feature.
---

# Author Mobile Flow Docs

## When to use

- User shares screenshots, screen recording, or step-by-step flow
- New feature before automation (groups, payments, onboarding, etc.)
- Updating `docs/<app_slug>-flow.md` after product changes

## Read first

1. **`AGENTS.md`**
2. Existing **`docs/<app_slug>-flow.md`**
3. User-provided assets in `docs/assets/` (copy screenshots there when supplied)

## Workflow

### 1. Capture the happy path

Number each screen transition:

```
1. Home → tap Add New
2. Select members → Manually
...
```

### 2. Update `docs/<app_slug>-flow.md`

Add or extend:

| Section | Content |
|---------|---------|
| Happy path | Numbered steps with screen names |
| Priority matrix | P0/P1 rows with automation status |
| Screen map | Screen → PO file → locator dump path |
| Known blockers | Permissions, promos, dev FAB, network |
| Test data | Required fields, unique naming, cleanup |

### 3. Save screenshots

Copy user images to `docs/assets/<feature>/01-home.png`, etc.

### 4. Hand off

```
author-mobile-flow-docs → extract-p0-test-cases → discover-mobile-locators
  → setup-mobile-test-data → mobile-appium-python
```

## Rules

- Do not invent steps not in user docs or screenshots
- Mark unconfirmed steps as **Unconfirmed**
- Note mandatory fields and success criteria explicitly
- Document dismissible modals (promos, permissions) in blockers
- For CoFee: read `docs/cofee-flow.md`

## QA checklist (include in flow doc)

- Preconditions (logged in? which account type?)
- Unique test data strategy (runtime group name)
- Assertions on final screen (not just navigation)
- Dev-build quirks (debug FAB, network logs overlay)
