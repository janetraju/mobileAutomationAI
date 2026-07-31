---
name: read-test-reports
description: >-
  Generates Allure HTML from pytest results and triages failures using
  screenshots, page source, and logcat. Use when debugging failed E2E runs,
  generating or opening Allure reports (invoke report), or investigating test
  failures after automation verification.
---
# Read Test Reports

Generate Allure HTML from pytest results and triage failure artifacts (screenshot, page source, logcat).

Reports reflect **only the latest pytest run**. Use this skill after a test failure to find the root cause — not to patch with `time.sleep()`.

## When to Use

Use this skill when:

- Generating or opening an Allure report (`invoke report`)
- Debugging a failed E2E run from attachments
- Triage after `testscript-generator` verification fails

## Workflow

### Step 1 — Confirm Results Exist

Reports require a completed pytest run:

```bash
invoke test --markers "e2e and p0"
# or: pytest -m "e2e and p0"
```

Raw results: `target/allure-results/` (configured in `pytest.ini` with `--clean-alluredir`).

Prerequisite: Allure CLI + Java (`allure --version`).

### Step 2 — Generate the Report

```bash
invoke report
invoke report --port=5051

# Manual equivalent
allure generate target/allure-results -o target/allure-report --clean
allure open target/allure-report -h 127.0.0.1 -p 5050
```

Tell the user the report URL (default `http://127.0.0.1:5050`).

Do not commit `target/allure-results/` or `target/allure-report/`.

### Step 3 — Triage a Failure

```text
Test fails
  → pytest stdout / -ra summary
  → invoke report → screenshot, page_source, logcat attachments
  → identify failed @allure.step
  → invoke ui:dump --screen=<name> on failing screen
```

Attachments come from `conftest.py` on failure — no per-test screenshot code needed.

### Step 4 — Map Failure to Owner

| Failure involves | Update |
| ---------------- | ------ |
| Report / attachment gaps | This skill |
| Locator timeout | `discover-mobile-locators` |
| Login / session / emulator | `testscript-generator` |
| Layer import violation | `pr-review-changes`, `testscript-generator` |

See **`testscript-generator`** Step 8 for the full update-skills policy.

### Step 5 — Record Learnings

When the failure teaches something reusable, append under **Known pitfalls** in the owning skill:

```markdown
### Known pitfalls (updated YYYY-MM-DD)
- **Symptom:** …
  **Cause:** …
  **Fix:** …
```

Skip only for one-off environment issues (e.g. device unplugged).

## Rules

- Always run tests before `invoke report` — empty results exit with an error.
- Do not change `pytest.ini` reporters unless the user asks.
- Flaky fixes follow **AGENTS.md** wait strategy — never add `time.sleep()`.
- Map the failed step back to the owning PO, step, or skill.

## Related Skills

- `testscript-generator`
- `discover-mobile-locators`
- `pr-review-changes`
