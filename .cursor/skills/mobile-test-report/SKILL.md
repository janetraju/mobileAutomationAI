---
name: mobile-test-report
description: >-
  Generates Allure HTML from a completed pytest run and triages failures
  using screenshots, page source, and logcat. Use after mobile-test-automation
  runs a test, to view pass/fail results or investigate why something
  failed. Non-coders: nothing to do here except open the report.
---

# Mobile Test Report

Generate Allure HTML from pytest results and triage failure artifacts
(screenshot, page source, logcat). Reports reflect **only the latest pytest
run** — this skill does not re-run tests itself.

Repository conventions (wait strategy, layer boundaries, markers) are
defined in `AGENTS.md`. This skill only reports and triages; it does not
fix a flaky test, rewrite a locator, or edit any layer file — those hand
off to `mobile-test-automation`.

## When to Use

Use this skill when:

- A run just finished in `mobile-test-automation` and you want pass/fail
  results
- Debugging why a test failed
- Opening or regenerating the Allure report (`invoke report`)

## Output

- Allure HTML report (local, opened in a browser)
- Triage notes: which step failed, the likely owning skill, and — if the
  failure teaches something reusable — a **Known pitfalls** entry appended
  to the owning skill

Do not commit `target/allure-results/` or `target/allure-report/`.

---

# Workflow

## Step 1 — Confirm Results Exist

Reports require a completed pytest run:

```bash
invoke test --markers "e2e and p0"
# or: pytest -m "e2e and p0"
```

Raw results land in `target/allure-results/` (`pytest.ini`,
`--clean-alluredir`). If nothing ran yet, stop and hand back to
`mobile-test-automation` — this skill has nothing to report on.

Prerequisite: Allure CLI + Java (`allure --version`).

## Step 2 — Generate the Report

```bash
invoke report
invoke report --port=5051
```

```bash
# Manual equivalent
allure generate target/allure-results -o target/allure-report --clean
allure open target/allure-report -h 127.0.0.1 -p 5050
```

Tell the user the report URL (default `http://127.0.0.1:5050`) — for a
non-coder, this is the entire step: open the link, look at pass/fail.

## Step 3 — Triage a Failure

```text
Test fails
  → pytest stdout / -ra summary
  → invoke report → screenshot, page_source, logcat attachments
  → identify the failed @allure.step
  → invoke ui:dump --screen=<name> on the failing screen, if a locator is suspect
```

Attachments come from `conftest.py` on failure automatically — no
per-test screenshot code needed.

## Step 4 — Map Failure to Owner

| Failure involves | Hand off to |
|---|---|
| Report/attachment gap itself | This skill |
| Locator timeout, flaky wait, layer/import violation | `mobile-test-automation` |
| Login, session, or emulator/device state | `mobile-test-automation` (auth wiring) or `teardown` (stale session/device state from a prior run) |
| Coverage/contract violation caught at review time, not runtime | `mobile-coverage-audit` |

## Step 5 — Record Learnings

When a failure teaches something reusable, append under **Known pitfalls**
in the *owning* skill from Step 4 — not here, unless the gap is in
reporting/triage itself:

```markdown
### Known pitfalls (updated YYYY-MM-DD)
- **Symptom:** …
  **Cause:** …
  **Fix:** …
```

Skip this for one-off environment issues (e.g. device unplugged, Appium
server not started).

## Step 6 — Hand Off

Report read, failures triaged and routed → hand off to `teardown` to reset
device/session/app state before the next run.

---

## Rules

- Always run tests before `invoke report` — empty results exit with an
  error.
- Do not change `pytest.ini` reporters unless the user asks.
- Flaky-test fixes follow `AGENTS.md`'s wait strategy — never patch with
  `time.sleep()`; that fix belongs in `mobile-test-automation`, not here.
- Map the failed step back to the owning layer file or skill — don't leave
  a failure unrouted.

## Related Skills

- `mobile-test-automation`
- `mobile-coverage-audit`
- `teardown`
