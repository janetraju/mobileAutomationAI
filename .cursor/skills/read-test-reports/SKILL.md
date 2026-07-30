---
name: read-test-reports
description: >-
  Generate and open Allure HTML reports from pytest results, and interpret
  failure artifacts (screenshot, page source, logcat). Use when the user asks
  to generate/open a report, run invoke report, view Allure, or debug a failed
  E2E run from attachments.
disable-model-invocation: true
---

# Test Reports (generate + read)

Covers **report generation** and **failure triage**. Derived from `pytest.ini`,
`tests/conftest.py` `pytest_runtest_makereport`, and `tasks.py` `report`.

---

## Part A — Generate the report

### How results are produced

| Step | What happens | Path |
|------|----------------|------|
| 1. Run tests | `allure-pytest` writes raw results each pytest session | `target/allure-results/` |
| 2. Generate HTML | Allure CLI builds the report from those results | `target/allure-report/` |
| 3. Open | Local Allure server serves the HTML | browser on `127.0.0.1:<port>` |

`pytest.ini` sets `--alluredir=target/allure-results` and `--clean-alluredir`
(previous results wiped at the start of each run).

### Prerequisites

```bash
allure --version    # Allure CLI + Java 8+
# Install if missing: https://docs.qameta.io/allure/ (or brew install allure)
```

`allure-pytest` is already a project dep (`pyproject.toml`).

### Commands

```bash
# 1) Produce raw results (always run tests first)
invoke test --markers "e2e and p0"
# or: pytest -m "e2e and p0"

# 2) Generate HTML + open browser (default port 5050)
invoke report
invoke report --port=5051

# Equivalent manual CLI
allure generate target/allure-results -o target/allure-report --clean
allure open target/allure-report -h 127.0.0.1 -p 5050
```

### What gets into the report

| Source | How it appears |
|--------|----------------|
| `@allure.epic` / `feature` / `story` / `severity` on tests | Suites / labels |
| `allure.dynamic.title(...)` | Parametrized case titles |
| `@allure.step` on steps + `assert_helper` | Timeline steps |
| Failure hook in `conftest.py` | Attachments: screenshot, page_source, logcat (Android) |
| `--record-video` | Optional session video when `RECORD_VIDEO=true` |

No per-test screenshot code needed — conftest attaches on failure.

### Generation rules

- **Always run tests before `invoke report`** — empty `target/allure-results/` → task prints *"No allure-results found"* and exits
- `--clean-alluredir` means the report reflects **only the latest pytest run**, not a historical merge
- Do not commit `target/allure-results/` or `target/allure-report/` (gitignored under `target/`)
- Do not change `pytest.ini` reporters unless the user asks

### Agent instructions (generate)

1. Confirm tests were run and `target/allure-results/` has files.
2. Run `invoke report` (or generate without open if headless CI).
3. Tell the user the report path / URL (`http://127.0.0.1:5050` by default).

---

## Part B — Read / triage the report

### Artifacts

| Artifact | Path / where | When |
|---|---|---|
| Allure results | `target/allure-results/` | Every pytest run |
| Allure report | `target/allure-report/` | After `invoke report` |
| Screenshot | Allure attachment | Failure |
| Page source | Allure attachment | Failure |
| Logcat (Android) | Allure attachment (last 200 lines) | Failure |

### Failure investigation

```text
Test fails
  → pytest stdout / -ra summary
  → invoke report (Part A) → open screenshot, page_source, logcat
  → identify failed @allure.step
  → invoke ui:dump --screen=<name> on failing screen
```

Do not add `time.sleep()` to fix flaky runs.

### On failure — update skills (mandatory)

After triaging a failed run, **update the relevant skill** — not only application
code. See **`automate-a-flow` Step 5**.

| If failure involves… | Update |
|---|---|
| Screenshot / page source / logcat / report gaps | This skill |
| Locator timeout | `discover-mobile-locators` Known pitfalls |
| Login / session / emulator | `mobile-appium-python`, `automate-a-flow` |
| Layer import violation | `pr-review-changes`, `mobile-appium-python` |

Append dated bullets under **Known pitfalls** so the next agent does not repeat
the mistake.

### Agent instructions (read)

1. Open the generated report (or inspect attachments in `target/allure-results/`).
2. Point to conftest auto-attachments — no per-test screenshot code needed.
3. Map the failed step back to the owning skill / PO.

---

## Related skills

`automate-a-flow` · `mobile-appium-python` · `discover-mobile-locators` ·
[AGENTS.md](../../../AGENTS.md)
