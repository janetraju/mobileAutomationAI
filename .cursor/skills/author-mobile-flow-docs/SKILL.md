---
name: author-mobile-flow-docs
description: >-
  Fallback flow documentation when get-context was not run: turn screenshots,
  walkthroughs, Figma, or a product/source repo into docs/<app_slug>-flow.md.
  Prefer get-context for full intake + context file. Use before
  extract-p0-test-cases when adding a feature without get-context.
disable-model-invocation: true
---

# Author Mobile Flow Docs

**Fallback** for flow docs. Prefer **`get-context`** when available — it writes
`docs/context/<app_slug>-<feature>-context.md` with intake. Use this skill when
the user only has screenshots / a walkthrough / product repo and did not run
`get-context`.

## When to use

- User shares screenshots, screen recording, or step-by-step flow **and**
  `get-context` was not run
- User shares a **product / feature source repo** without running `get-context`
- Updating `docs/<app_slug>-flow.md` after product changes (light edit)

## Read first

1. **`AGENTS.md`**
2. Existing **`docs/<app_slug>-flow.md`**
3. User-provided context:
   - Screenshots / assets in `docs/assets/` when supplied, **and/or**
   - Product repo paths the user points to (screens, routes, widgets, copy)

## Accepted inputs

| Input | Use for |
|-------|---------|
| Screenshots / walkthrough | Visual happy path, CTA labels, order of screens |
| Product/source repo | Screen names, navigation, fields, validation, a11y labels in code |
| Figma / docs in git | Same as walkthrough when structured |

**Repo is the flow spec — not the locator source of truth.** After documenting flows, hand off to **`discover-mobile-locators`** on a running build.

## Workflow

### 1. Capture the happy path

From screenshots **or** code (routes / screen widgets / navigation):

```
1. Home → tap Add New
2. Select members → Manually
...
```

Mark anything only inferred from code (not seen on device) as **Unconfirmed**.

### 2. Update `docs/<app_slug>-flow.md`

Add or extend:

| Section | Content |
|---------|---------|
| Happy path | Numbered steps with screen names |
| Priority matrix | P0/P1 rows with automation status |
| Screen map | Screen → PO file → how to dump (`invoke ui:dump --screen=…`) |
| Known blockers | Permissions, promos, dev FAB, network |
| Test data | Required fields, unique naming, cleanup |
| Context source | Screenshots / product repo path / both |

### 3. Optional assets

- Copy screenshots to `docs/assets/<feature>/` when provided
- Do **not** commit product source into this automation repo; reference the path/repo the user shared for this session

### 4. Hand off

Use this skill only when **`get-context` was not run** this session.

```text
author-mobile-flow-docs
  → extract-p0-test-cases
  → discover-mobile-locators
  → setup-mobile-test-data
  → automate-a-flow
  → mobile-appium-python
```

## Rules

- Do not invent steps not in user docs, screenshots, **or** clearly identifiable product code
- Mark unconfirmed steps as **Unconfirmed**
- Note mandatory fields and success criteria explicitly
- Document dismissible modals (promos, permissions) in blockers
- For CoFee: read `docs/cofee-flow.md`
- Never skip device locator discovery for Flutter/RN because “the repo has widget keys”

## QA checklist (include in flow doc)

- Preconditions (logged in? which account type?)
- Unique test data strategy (runtime group name)
- Assertions on final screen (not just navigation)
- Dev-build quirks (debug FAB, network logs overlay)
