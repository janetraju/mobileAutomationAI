<!--
Template for docs/context/<app_slug>-<slug>-testcases.md. One block per
test case, grouped by category. Delete this comment in the written file.
-->

# Test Cases: <Feature/Screen Name> (`<app_slug>-<slug>`)

Source: `docs/context/<app_slug>-<slug>-context.md` (or `docs/<app_slug>-flow.md` if no context file existed)
Approved: <date/session note>

## Preconditions (shared, reference by id)

| ID | Description |
|----|-------------|
| PRE-01 | Fresh install, no active session |
| PRE-02 | Logged in, on dashboard |

## Happy Path (HP)

### TC-<slug>-HP-01: <title>

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-01 |
| Automation status | Not started / In progress / Done |

**Steps:**
1. ...
2. ...

**Expected Result:** ...

## Negative / Validation (NEG)

<same block shape per case>

## Edge Cases (EDGE)

<same block shape>

## Permission / OS Dialog (PERM)

<same block shape>

## State / Navigation (STATE)

<same block shape>

## Accessibility (A11Y)

<only if a real issue was flagged in context/flow doc — same block shape>

## Platform Variance (PLAT)

<mark iOS cases "not locally runnable" explicitly>

## Regression (REG)

<tied to a known bug/quirk from context/flow doc>

---

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-<slug>-HP-01 | Happy Path | P0 | Not started |

## Parametrization candidates

List any cases collapsed into one parametrized case per Core rule 9, with
their variant data table.

## Locator map (only if live-confirmed in get-context/discover-mobile-locators)

| Element | Locator | Confirmed live? |
|---------|---------|------------------|

## Open questions

Anything still unresolved that `discover-mobile-locators` or
`testscript-generator` should address.

## Handoff

Next: `discover-mobile-locators` (for any outstanding 🟡 hypotheses), then
**`testscript-generator`** to implement.
