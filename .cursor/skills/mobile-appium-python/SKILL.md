---
name: mobile-appium-python
description: >-
  Write and maintain Appium mobile tests using Pytest, Python, and Allure
  in this repo. Use when authoring page objects, page actions, steps, locators,
  driver fixtures, dataproviders, debugging flaky mobile tests, or Android/iOS
  automation for any app configured in this framework.
---

# Mobile Appium Python Skill

## Before you write code

1. Read **`AGENTS.md`** (repo root).
2. Confirm **`PLATFORM`** and **`APP_SLUG`** from `.env` / `src/core/settings.py`.
3. Inspect the real UI (Appium Inspector, `adb shell uiautomator dump`, iOS Accessibility Inspector) before writing locators — never guess selectors.

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
invoke test --markers "e2e and p0"
invoke lint --fix
invoke report
```

## Sync API only

Use `appium.webdriver.webdriver.WebDriver` (sync). Do not mix async Appium clients.
