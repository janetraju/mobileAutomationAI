---
name: mobile-appium-python
description: >-
  Author and maintain four-layer Appium code (page objects, actions, steps,
  dataproviders, tests), markers, fixtures, and flaky-test fixes in this repo.
  Use when writing or editing a specific layer file, or debugging locators/
  markers. For end-to-end "automate this scenario" orchestration (prereqs,
  MCP walkthrough, verify order), use automate-a-flow first.
disable-model-invocation: true
---

# Mobile Appium Python Skill

Layer patterns and coding rules. **Orchestration** (prereqs → MCP walk →
implement → verify) belongs in **`automate-a-flow`** — call that first for a
new scenario, then use this skill for the files.

## Before you write code

1. Read **`AGENTS.md`** (repo root).
2. Confirm **`PLATFORM`** and **`APP_SLUG`** from `.env` / `src/core/settings.py`.
3. Read **`docs/<app_slug>-flow.md`** and approved testcases if present.
4. Confirm locators via **`discover-mobile-locators`** / Appium MCP — never
   guess selectors from product source alone.

## Authoring from a product/source repo

When the feature spec came from an app codebase:

1. Ensure flow doc exists (`author-mobile-flow-docs`) and P0s are agreed (`extract-p0-test-cases`)
2. Navigate the build on emulator/device → **`discover-mobile-locators`**
3. Draft POs from the dump (optionally cross-check labels/keys seen in product code)
4. Implement actions → steps → dataprovider → test
5. Run on device; heal flaky CTAs with evidence (screenshot / page source)

Repo informs **what** to automate; the device dump locks **how** to find elements.

## When working on CoFee

- Read **`docs/cofee-flow.md`** for flows and priorities.
- Add code under `src/page_objects/cofee/`, `src/page_actions/cofee/`, `src/steps/cofee/`.
- Run **`invoke test`** (or `pytest` with markers) after changes.
- Update flow doc automation status when a P0 case is covered.

## Feature add order

```
page_objects → page_actions → steps → dataprovider → test
```

| Step | Path pattern | Rules |
|------|--------------|-------|
| PO | `src/page_objects/<app_slug>/<screen>_po.py` | Locators in `# --- Locators ---`; inherit `BasePage` |
| Actions | `src/page_actions/<app_slug>/<screen>_actions.py` | Verb phrases; gestures here; instantiate PO |
| Steps | `src/steps/<app_slug>/<feature>_steps.py` | `@allure.step`; call actions only |
| Data | `tests/dataprovider/dp_<feature>.py` | `get_*_test_data()` → `list[pytest.param(...)]`; no secrets |
| Test | `tests/test/<app_slug>/<feature>/test_<feature>.py` | Steps + assertions only |

## Locator rules

- Priority: accessibility id → UiAutomator/resource-id → iOS predicate/class chain → text → XPath (last)
- Naming: `btn_login`, `txt_title`, `input_email`, `chk_terms`, `msg_error`
- Dynamic text: `_loc_*()` helpers + format templates in `__init__`
- Platform split: `self._platform` in PO, or `*_android_po.py` / `*_ios_po.py`
- **Never** put `driver.find_element` in tests, steps, or actions

## Test markers (required)

```python
@pytest.mark.e2e
@pytest.mark.p0  # or p1, p2
@pytest.mark.android  # or ios when platform-specific
@allure.epic("CoFee")
```

## Flaky test playbook

| Symptom | Fix |
|---------|-----|
| Stale element | Re-query via PO after navigation |
| Element not found | Wrong locator priority; inspect live tree |
| Timeout on spinner | `wait_for_loading_spinner_to_disappear()` in actions |
| Keyboard covering field | `hide_keyboard()` in actions |
| Wrong context | `switch_to_webview()` / `switch_to_native()` in actions |
| Parallel collision | `pytestmark = pytest.mark.xdist_group(PARALLEL_GROUP_*)` |

## Invoke commands

```bash
invoke install
invoke emulator:start
invoke appium:start
invoke appium:doctor
invoke lint                       # auto-fix ruff + black (default)
invoke lint --no-fix              # check-only
invoke test --markers "e2e and p0"   # clean → lint (auto-fix) → pytest
invoke report
```

## Lint (auto-fix by default)

`invoke lint` and `invoke test` always run **ruff --fix** + **black** write mode.

- Check-only: `invoke lint --no-fix`
- If anything remains unfixed (e.g. unused import needing judgment), fix in code,
  then `invoke lint` again — do not leave formatting for the user to do by hand.

## Sync API only

Use `appium.webdriver.webdriver.WebDriver` (sync). Do not mix async Appium clients.

## Before a new feature test

Follow **`automate-a-flow`** — login P0 on a clean emulator first, walk the
scenario on device (`discover-mobile-locators`), then implement layers here.

## Pytest fixtures (`tests/conftest.py`)

| Fixture | Scope | Source |
|---------|-------|--------|
| `driver` | session | `SessionManager.get_driver(profile=auth_profile)` |
| `settings` | session | `get_settings()` |
| `mobile` / `otp` | session | `TEST_MOBILE` / `TEST_OTP` from env |

CLI overrides: `--env`, `--platform`, `--device`, `--headless-emulator`,
`--record-video`. Tests live under `tests/test/<app_slug>/<feature>/`.

## Related skills

`automate-a-flow` · `discover-mobile-locators` · `setup-mobile-test-data` ·
`read-test-reports` · `review-changes` · [AGENTS.md](../../../AGENTS.md)
