---
name: author-mobile-flow-docs
description: >-
  Fallback flow documentation when get-context was not run: turn screenshots,
  walkthroughs, Figma, or a product/source repo into docs/<app_slug>-flow.md.
  Prefer get-context for full intake. Repo contract lives in AGENTS.md.
disable-model-invocation: true
---

# Author Mobile Flow Docs

**Task:** write/update `docs/<app_slug>-flow.md` from user assets or product code.  
**Repo contract:** [AGENTS.md](../../../AGENTS.md) (feature context vs locators).  
Prefer **`get-context`** when available.

## When to use

- Screenshots / walkthrough / product repo **and** `get-context` was not run
- Light update to an existing flow doc after product changes

## Read first

1. **`AGENTS.md`**
2. Existing **`docs/<app_slug>-flow.md`**
3. User assets (`docs/assets/`) and/or product repo paths shared this session

## Accepted inputs

| Input | Use for |
|-------|---------|
| Screenshots / walkthrough | Visual happy path, CTA labels, screen order |
| Product/source repo | Screens, navigation, fields, validation, a11y labels in code |
| Figma / docs in git | Same as walkthrough when structured |

Product/source code informs the **flow spec** only. Locators are confirmed later
via **`discover-mobile-locators`** (see AGENTS.md).

## Workflow

### 1. Capture the happy path

```text
1. Home → tap Add New
2. Select members → Manually
...
```

Mark steps only inferred from code (not seen on device) as **Unconfirmed**.

### 2. Update `docs/<app_slug>-flow.md`

| Section | Content |
|---------|---------|
| Happy path | Numbered steps with screen names |
| Priority matrix | P0/P1 rows with automation status |
| Screen map | Screen → PO file → `invoke ui:dump --screen=…` |
| Known blockers | Permissions, promos, dev FAB, network |
| Test data | Required fields, unique naming, cleanup |
| Context source | Screenshots / product repo / both |

### 3. Optional assets

- Copy screenshots to `docs/assets/<feature>/` when provided
- Do **not** commit product source into this repo

### 4. Hand off

```text
author-mobile-flow-docs
  → extract-p0-test-cases
  → discover-mobile-locators
  → setup-mobile-test-data
  → automate-a-flow
  → mobile-appium-python
```

## Skill-specific rules

- Do not invent steps not in user docs, screenshots, or clearly identifiable product code
- Note mandatory fields and success criteria explicitly
- Document dismissible modals in blockers
- For CoFee: extend `docs/cofee-flow.md`

## QA checklist (include in flow doc)

- Preconditions (logged in? account type?)
- Unique test data strategy
- Assertions on final screen (not just navigation)
- Dev-build quirks (debug FAB, overlays)

## Related skills

`get-context` · `extract-p0-test-cases` · `discover-mobile-locators` ·
[AGENTS.md](../../../AGENTS.md)
