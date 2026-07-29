---
name: discover-mobile-locators
description: >-
  Discover real mobile UI locators by installing the app on a device or emulator
  and capturing accessibility trees. Use before writing page objects, when
  onboarding a new app, after UI changes, or when APK/source analysis is
  insufficient. Locator priority and naming live in AGENTS.md — this skill is
  the dump/MCP workflow only.
disable-model-invocation: true
---

# Discover Mobile Locators

**Task:** capture and confirm locators on a running app.  
**Repo contract:** [AGENTS.md](../../../AGENTS.md) — locator priority, naming
prefixes/suffixes, `find_*` / `loc_*`, no invented selectors.

## When to use

- Before creating any `*_po.py` file
- After `onboard-mobile-app`, `get-context`, or `author-mobile-flow-docs`
- After analyzing a product/source repo (code labels/keys are **hypotheses only**)
- User asks for selectors, Inspector output, or uiautomator dump

## Prerequisites

```bash
invoke appium:doctor
invoke emulator:start          # Android; or connect physical device
invoke app:install             # uses APP_PATH from .env
```

## Workflow

### 1. Confirm config

From `.env`: `APP_SLUG`, `APP_TYPE`, `PLATFORM`, `APP_PACKAGE`, `APP_ACTIVITY`.

### 2. Launch app to target screen

```bash
adb shell am start -n <APP_PACKAGE>/<APP_ACTIVITY>
# Navigate manually or via deep link to the screen under test
```

### 3. Dump UI tree

```bash
invoke ui:dump --screen=<screen_name>
# writes docs/locators/<screen_name>.xml locally (gitignored)
```

Repeat per screen (e.g. `splash`, `login_phone`, `login_otp`, `home`).

### 3b. Appium MCP (live tree — mandatory for new TCs)

**Required before any new test scenario** — see **`automate-a-flow`**.

1. Emulator/device up; `.env` matches `environment/appium-mcp.capabilities.json`
2. `select_device` → `appium_session_management` (`action=create`)
3. Walk the scenario — `appium_gesture` / `appium_set_value`
4. Per screen: `appium_get_page_source` → `docs/locators/<screen>.xml`
5. `generate_locators` — **confirm every selector** against page source before `*_po.py`

Screenshots → `target/mcp-screenshots/` when `NO_UI=true`.

### 4. Parse dump

Apply **AGENTS.md Locator strategy** (priority + naming) to each interactive
element. Re-dump after animations, keyboard, or navigation.

### 5. App-type notes (while parsing)

| `APP_TYPE` | Guidance |
|------------|----------|
| `flutter` | Prefer `content-desc` / semantic labels; avoid brittle XPath into `android.view.View` |
| `rn` | Prefer `content-desc` matching `testID` / `accessibilityLabel` |
| `hybrid` | Dump native; switch WebView in actions for H5 |
| `native` | `resource-id` usually stable |

### 6. Produce locator sheet

Document in `docs/<app_slug>-flow.md` or `docs/locators/<screen>.md`:

| PO name | Element | Strategy | Locator value | Confirmed |
|---------|---------|----------|---------------|-----------|
| `input_mobile` | Phone field | accessibility id | `...` | yes |

PO name = method stem (`input_mobile` → `find_input_mobile` / `loc_input_mobile`).

Dump file names: `docs/locators/<screen>.xml` (snake_case screen names).  
iOS: `docs/locators/<screen>_ios.xml`.

### 7. Hand off

Only after the locator sheet exists → **`mobile-appium-python`** / **`automate-a-flow`**.

## Skill-specific rules

- Never guess from APK or product source alone — confirm live
- Product repo / widget keys are candidates only
- Do not commit `docs/locators/*.xml` (see `.gitignore`)

## Related skills

`automate-a-flow` · `mobile-appium-python` · [AGENTS.md](../../../AGENTS.md)
