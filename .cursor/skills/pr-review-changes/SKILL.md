---
name: pr-review-changes
description: >-
  Reviews automation diffs for compliance with AGENTS.md—layer boundaries,
  locator policy, waits, markers, and code quality. Use when reviewing pull
  requests, local branch changes, or validating page objects, actions, steps,
  dataproviders, or tests before merge.
---
# Review Changes

Review automation diffs for compliance with the repo contract in **AGENTS.md**.

This skill checks whether changes follow layer boundaries, locator policy, waits, tests, and code quality. It does not redefine those rules — cite **AGENTS.md** sections when flagging issues.

## When to Use

Use this skill when:

- Reviewing a pull request or local branch changes
- Validating new page objects, actions, steps, dataproviders, or tests
- Checking automation work before merge

For PR description drafting, use **`add-pr-description`** instead.

## Workflow

### Step 1 — Understand the Change

Review:

**Required**

- `AGENTS.md`

**If modified on this branch**

- `src/page_objects/`, `src/page_actions/`, `src/steps/`
- `tests/dataprovider/`, `tests/test/`
- `docs/context/*.md`, `docs/<app_slug>-flow.md`

Map each changed file to its layer (PO, actions, steps, dataprovider, test, docs).

### Step 2 — Check Repo Contract

Walk **AGENTS.md** section by section:

| Section | Verify |
| ------- | ------ |
| Architecture & layer boundaries | Import direction; no driver in tests/steps; locators only in POs |
| Locator strategy | Live-confirmed selectors; naming; no duplicate XPath |
| Wait & stability | Re-query after navigation; no `time.sleep()` |
| Assertions | Observable UI outcomes; no assert_helper in actions |
| Tests, markers & Allure | `@pytest.mark.e2e` + priority; Allure labels |
| Code quality | Lint clean; no bare `except:`; no secrets |

### Step 3 — Traceability

Confirm:

- Tests map to approved `docs/context/*-testcases.md` or flow doc P0 matrix
- New locators have a dump or MCP walkthrough note
- Flow/context docs updated if behavior or blockers changed

### Step 4 — Run Verification

```bash
invoke lint --no-fix
invoke test --markers "<relevant markers>"
```

### Step 5 — Report Findings

Group by severity:

- **Blocker** — must fix before merge
- **Should fix** — contract violation or missing traceability
- **Nit** — style or optional improvement

Reference the **AGENTS.md** section for each finding.

## Rules

- Do not restate repo rules — point to **AGENTS.md**.
- Flag import-direction and layer violations as blockers.
- Require live-confirmed locators for new PO fields.
- Do not approve tests that skip upstream prerequisite checks when the flow depends on login.

## Related Skills

- `add-pr-description`
- `testscript-generator`
