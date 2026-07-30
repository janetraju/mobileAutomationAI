---
name: mobile-appium-python
description: >-
  Author and maintain four-layer Appium code (page objects, actions, steps,
  dataproviders, tests), fixtures, and flaky-test fixes in this repo.
  Use when writing or editing a specific layer file, or debugging locators/
  markers. For end-to-end "automate this scenario" orchestration, use
  automate-a-flow first. Repo-wide rules live in AGENTS.md — do not restate them.
disable-model-invocation: true
---

# Mobile Appium Python Skill

**Task:** write or edit layer files. **Repo contract:** [AGENTS.md](../../../AGENTS.md)
(architecture, locators, waits, markers, stability). Do not duplicate those rules here.

**Orchestration** (prereqs → MCP walk → implement → verify) belongs in
**`automate-a-flow`** — call that first for a new scenario.

## Before you write code

1. Read **`AGENTS.md` Repo contract**.
2. Confirm **`PLATFORM`** and **`APP_SLUG`** from `.env` / `src/core/settings.py`.
3. Read **`docs/<app_slug>-flow.md`** and approved testcases if present.
4. Confirm locators via **`discover-mobile-locators`** / Appium MCP.

## Feature add order

```text
page_objects → page_actions → steps → dataprovider → test
```

| Step | Path pattern | This skill's focus |
|------|--------------|--------------------|
| PO | `src/page_objects/<app_slug>/<screen>_po.py` | `# --- Locators ---`; inherit `BasePage`; `find_*` / `loc_*` |
| Actions | `src/page_actions/<app_slug>/<screen>_actions.py` | Verb phrases; gestures; instantiate PO |
| Steps | `src/steps/<app_slug>/<feature>_steps.py` | `@allure.step`; call actions only |
| Data | `tests/dataprovider/dp_<feature>.py` | `get_*_test_data()` → `list[pytest.param(...)]` |
| Test | `tests/test/<app_slug>/<feature>/test_<feature>.py` | Steps + assertions only |

Follow **AGENTS.md** for what each layer may/must not call.

## Authoring from a product/source repo

1. Flow doc / context + agreed P0s exist
2. **`discover-mobile-locators`** on a running build
3. Draft POs from the dump (product keys are hypotheses only)
4. Implement actions → steps → dataprovider → test
5. Run on device; heal with screenshot / page source evidence

## When working on CoFee

- Paths under `src/**/cofee/` and `tests/test/cofee/`
- Update `docs/cofee-flow.md` automation status when a P0 is covered
- Verify with `invoke test` / markers after changes

## Flaky test playbook

| Symptom | Fix |
|---------|-----|
| Stale element | Re-query via PO after navigation |
| Element not found | Re-inspect live tree; check AGENTS locator priority |
| Timeout on spinner | `wait_for_loading_spinner_to_disappear()` in actions |
| Keyboard covering field | `hide_keyboard()` in actions |
| Wrong context | `switch_to_webview()` / `switch_to_native()` in actions |
| Parallel collision | `pytestmark = pytest.mark.xdist_group(PARALLEL_GROUP_*)` |

## Pytest fixtures (`tests/conftest.py`)

| Fixture | Scope | Source |
|---------|-------|--------|
| `driver` | session | `SessionManager.get_driver(profile=auth_profile)` |
| `settings` | session | `get_settings()` |
| `mobile` / `otp` | session | `TEST_MOBILE` / `TEST_OTP` from env |

CLI overrides: `--env`, `--platform`, `--device`, `--headless-emulator`,
`--record-video`.

## Related skills

`automate-a-flow` · `discover-mobile-locators` · `setup-mobile-test-data` ·
`read-test-reports` · `pr-review-changes` · [AGENTS.md](../../../AGENTS.md)
