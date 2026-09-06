---
name: pr-review-changes
description: >-
  Reviews automation diffs for compliance with AGENTS.md's Repo contract —
  layer boundaries, locator policy, waits, markers, and code quality. Use
  when reviewing a pull request or local branch changes, or validating new
  page objects, actions, steps, dataproviders, or tests before merge. This
  is a code-compliance review only — it does not check whether test-design
  coverage is complete (that's mobile-coverage-audit's job).
---
# Review Changes

Review automation diffs for compliance with the Repo contract in
**AGENTS.md**. This skill checks whether *code* follows layer boundaries,
locator policy, waits, markers, and code quality — it does not redefine
those rules; cite the relevant **AGENTS.md** section when flagging an issue.

**This is a code-quality gate, not a coverage report.** Whether enough test
cases exist for a feature (missing categories, screens, business rules, or
a `docs/<app_slug>-flow.md` row whose claimed Status doesn't match reality)
is **`mobile-coverage-audit`**'s job, not this skill's. Run both before a
merge if you want both checks — they read overlapping files but answer
different questions and never duplicate each other's findings.

## When to Use

Use this skill when:

- Reviewing a pull request or local branch changes
- Validating new page objects, actions, steps, dataproviders, or tests
- Checking automation work before merge

## Workflow

### Step 1 — Understand the Change

Review:

**Required**

- `AGENTS.md`

**If modified on this branch**

- `src/page_objects/<app_slug>/`, `src/page_actions/<app_slug>/`, `src/steps/<app_slug>/`
- `tests/dataprovider/`, `tests/test/<app_slug>/`
- `docs/context/*.md`, `docs/<app_slug>-flow.md`

Map each changed file to its layer (PO, actions, steps, dataprovider, test, docs).

### Step 2 — Check Repo Contract

Walk **AGENTS.md**'s Repo contract section by section:

| Section | Verify |
| ------- | ------ |
| Architecture & layer boundaries | Import direction (tests → steps → page_actions → page_objects → core); no `driver.find_element` in tests/steps/actions; locators only in `*_po.py` under `# --- Locators ---`; platform branching only in page objects |
| Locator strategy | Selectors live-confirmed on a running app (never invented from APK/product source/Figma alone); PO naming conventions (`btn_`, `input_`, `find_*`/`loc_*`) |
| Wait & stability | No `time.sleep()`; explicit waits via `PageActions`/`BasePage`; elements re-queried after navigation/animation, not cached stale |
| Assertions | Assertions live in tests (via `assert_helper`) or thin step wrappers, never in page actions/objects; assert observable UI outcomes (screen, copy, counts, amounts), not just "navigation happened" |
| Tests, markers & Allure | `@pytest.mark.e2e` + priority (`p0`/`p1`/`p2`) + platform marker; Allure `epic`/`feature`/`story`/`severity`; `PARALLEL_GROUP_*` used when sharing a device/session |
| Code quality | Lint clean (`invoke lint --no-fix`); no bare `except:`; no hardcoded credentials or app names (`.env` / `get_settings()` / `APP_NAME` only); imports at module top |
| Test data & credentials | Credentials only in `.env`/`.env.<env>`, never in a committed context/flow doc, dataprovider, PO, or step; no production credentials or real personal SSO accounts; backend/SQL assertions stay in `data/<app_slug>/` scripts, never in page layers |

### Step 3 — Traceability

Confirm:

- Tests map to an existing `docs/context/<app_slug>-<feature>-testcases.md` (from `mobile-test-design`) or a row in `docs/<app_slug>-flow.md`'s Status table
- New locators have a `ui:dump` or Appium MCP walkthrough note (`mobile-test-automation`'s job)
- `docs/<app_slug>-flow.md` and/or the feature's context doc were updated if behavior or blockers changed
- Login/credential strategy used by any new test matches what `get-mobile-auth` recorded for that method — don't approve a test that invents its own auth handling

### Step 4 — Run Verification

```bash
invoke lint --no-fix
invoke test --markers "<relevant markers>"
```

### Step 5 — Report Findings

Group by severity:

- **Blocker** — must fix before merge (layer/import-direction violation, invented/unconfirmed locator, hardcoded secret, missing traceability to an approved testcase)
- **Should fix** — Repo-contract deviation that isn't a hard blocker (e.g. a missing marker, a weak assertion)
- **Nit** — style or optional improvement

Reference the **AGENTS.md** Repo-contract section for each finding. This
skill reports in conversation only — it does not write a file.

## Rules

- Do not restate Repo-contract rules — point to **AGENTS.md**.
- Flag import-direction and layer violations as blockers.
- Require live-confirmed locators for new PO fields — never approve one
  sourced only from APK analysis, product source, or Figma.
- Do not approve a test that skips an upstream prerequisite (e.g. a
  downstream flow that assumes login without going through it or reusing
  an authenticated session per the recorded strategy).
- Do not flag missing test cases, missing categories, or coverage gaps —
  redirect those findings to `mobile-coverage-audit` instead of reporting
  them here.

## Related Skills

- `mobile-test-automation` — implements the code this skill reviews
- `mobile-coverage-audit` — the companion coverage-gap report (test-design completeness, not code compliance)
- `get-mobile-context` / `mobile-test-design` — the context/testcases docs this skill checks traceability against
