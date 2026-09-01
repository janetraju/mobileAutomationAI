<!--
Copy to: docs/context/<app_slug>-<feature-slug>-testcases.md
Also see: .cursor/skills/testcase-generator/testcase-template.md
Delete this comment block in the written file.
-->

# Test Cases: <Feature name> (`<app_slug>-<feature-slug>`)

Source: `docs/context/<app_slug>-<feature-slug>-context.md`  
Approved: **yes** / **no** — <YYYY-MM-DD / note>

## Freshness

| Field | Value |
|-------|-------|
| Last updated | YYYY-MM-DD |
| Env checked | dev / stg / uat |
| Confirmed on device | yes / no |
| Owner | <name or team> |

## Preconditions (shared)

| ID | Description |
|----|-------------|
| PRE-01 | Fresh install, no active session (`@pytest.mark.fresh`) |
| PRE-02 | Logged in on home (`@pytest.mark.authenticated`) |

## Happy Path (HP)

### TC-<slug>-HP-01: <title>

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-01 / PRE-02 |
| Automation status | Not started / In progress / Done |
| Test path | `tests/test/...` (when Done) |

**Steps:**
1. …

**Expected Result:** …

## Negative / Validation (NEG)

<!-- same block shape -->

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-<slug>-HP-01 | Happy Path | P0 | Not started |

## Parametrization candidates

-

## Locator map (live-confirmed only)

| Element | Locator | Confirmed live? |
|---------|---------|------------------|

## Open questions

-

## Handoff

Next: `discover-mobile-locators` (outstanding hypotheses), then `testscript-generator`.
