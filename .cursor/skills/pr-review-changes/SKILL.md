---
name: pr-review-changes
description: >-
  Code review against AGENTS.md Repo contract for Appium mobile automation.
  Use when reviewing PRs or local changes. Does not redefine repo rules —
  checks compliance with AGENTS.md.
disable-model-invocation: true
---

# Review Changes

**Task:** review diffs for compliance.  
**Source of truth:** [AGENTS.md](../../../AGENTS.md) **Repo contract**.  
For PR body drafting, use **`author-pr-description`**.

## How to review

1. Read the diff.
2. Check each changed file against **AGENTS.md** sections:
   - Architecture & layer boundaries
   - Locator strategy
   - Wait & stability
   - Assertions
   - Tests, markers & Allure
   - Code quality
3. Flag violations with the **AGENTS.md section name** in the comment.

## Quick checklist (pointers only)

| Severity | Check (details in AGENTS.md) |
|----------|------------------------------|
| Critical | Layer imports; no `driver.find_element` outside POs; no locators in tests/steps; no `time.sleep()`; no secrets |
| High | `# --- Locators ---`; `find_*` / `loc_*`; `e2e` + priority markers; live-confirmed locators; Allure labels |
| Medium | `EXPLICIT_WAIT_TIMEOUT`; re-query after nav; `pytest.param` ids; `PARALLEL_GROUP_*` when needed; `invoke lint` clean |

## Layer smoke check

| Layer | Pass if |
|-------|---------|
| PO | Locators only; `BasePage` |
| Actions | `PageActions` + PO; no assert_helper |
| Steps | Actions only; `@allure.step` |
| Tests | Steps + assert_helper only |
| Dataprovider | `get_*_test_data()`; no secrets |

## Traceability

New/changed tests should map to approved `docs/context/*-testcases.md` or the
flow doc priority matrix.

## Related skills

`author-pr-description` · `mobile-appium-python` · `automate-a-flow` ·
[AGENTS.md](../../../AGENTS.md)
