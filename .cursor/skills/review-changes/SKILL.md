---
name: review-changes
description: >-
  Code review checklist for Appium mobile automation in this repo. Use when
  reviewing PRs, local changes, or validating new page objects, actions,
  steps, dataproviders, and tests.
disable-model-invocation: true
---

# Review Changes

Use for **code quality review**. For PR body drafting, use **`author-pr-description`**
instead.

## Critical

- No duplicate locators across POs
- No XPath without documented justification
- No `time.sleep()` or arbitrary waits
- No locators in tests or steps
- No business logic in page objects
- No `assert_helper` in page actions
- No `driver.find_element()` outside POs
- No hardcoded credentials — `.env` / `get_settings()`
- No `page_actions` or `page_objects` imports in tests

## High

- Uses `EXPLICIT_WAIT_TIMEOUT` from settings — no magic timeouts
- Every UI test: `@pytest.mark.e2e` + `p0`/`p1`/`p2`
- Platform marker when platform-specific
- `@allure.step` on step functions
- `# --- Locators ---` block in POs
- `find_*` / `loc_*` pattern consistent with existing POs
- Test cases trace to approved `docs/context/*-testcases.md` or flow doc P0 matrix

## Medium

- Import direction: tests → steps → page_actions → page_objects → core
- `pytest.param(..., id="...")` in dataproviders
- `PARALLEL_GROUP_*` when parallel with other features
- Re-query elements after navigation
- Allure epic/feature/story/severity on tests
- `invoke lint` passes (ruff + black auto-fix by default)

## Lint

`invoke lint` and `invoke test` **auto-fix** (ruff `--fix` + black). Check-only:

```bash
invoke lint --no-fix
```

Do not leave formatting for the user to fix by hand.

## Layer checks

| Layer | Verify |
|-------|--------|
| PO | Locators only; inherits `BasePage` |
| Actions | Extends `PageActions`; PO in `__init__` |
| Steps | Instantiates actions; passes `driver` |
| Tests | Calls steps only; receives `driver` fixture |
| Dataprovider | `get_*_test_data()`; no secrets |

## Coding standards

- No bare `except:` — `except Exception:`
- Imports at module top
- No `pytest.skip()` in page actions
- No secrets in dataproviders
- Locators confirmed live (`discover-mobile-locators`) — not repo-code guesses alone

## Related skills

`author-pr-description` · `mobile-appium-python` · `automate-a-flow` ·
[AGENTS.md](../../../AGENTS.md)
