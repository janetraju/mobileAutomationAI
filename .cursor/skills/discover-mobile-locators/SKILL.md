---
name: discover-mobile-locators
description: >-
  Discover real mobile UI locators by installing the app on a device or emulator
  and capturing accessibility trees. Use before writing page objects, when
  onboarding a new app, after UI changes, or when APK analysis is insufficient
  for Flutter, React Native, or hybrid apps.
---

# Discover Mobile Locators

## When to use

- Before creating any `*_po.py` file
- After `onboard-mobile-app` or `author-mobile-flow-docs`
- After analyzing a **product/source repo** (code labels/keys are hints only)
- User asks for selectors, Inspector output, or uiautomator dump
- Flutter / RN / hybrid apps (APK or source analysis alone is never enough)

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
# writes docs/locators/<screen_name>.xml locally (gitignored — do not commit dumps)
```

Repeat per screen (e.g. `splash`, `login_phone`, `login_otp`, `home`).

### 4. Parse dump — locator priority

| Priority | Android (UiAutomator2) | iOS (XCUITest) |
|----------|------------------------|----------------|
| 1 | `content-desc` → `ACCESSIBILITY_ID` | `accessibility id` |
| 2 | `resource-id` | `name` / predicate |
| 3 | `text` | `label` / predicate |
| 4 | `class` + index | class chain |
| 5 | XPath | XPath (last resort) |

### 5. App-type notes

| `APP_TYPE` | Guidance |
|------------|----------|
| `flutter` | Prefer `content-desc` / semantic labels; text like `"Enter mobile number"` often works; avoid brittle XPath into `android.view.View` |
| `rn` | Look for `content-desc` matching `testID` / `accessibilityLabel` |
| `hybrid` | Dump in native context; switch WebView for H5 screens (`switch_to_webview` in actions) |
| `native` | `resource-id` usually stable |

### 6. Produce locator sheet

For each interactive element, document in `docs/<app_slug>-flow.md` or `docs/locators/<screen>.md`:

| PO name | Element | Strategy | Locator value | Confirmed |
|---------|---------|----------|---------------|-----------|
| `input_mobile` | Phone field | accessibility id | `...` | yes |

### 7. Hand off to `mobile-appium-python`

Only after locator sheet exists for the screen.

## Rules

- Never guess locators from APK decompilation or product source alone
- Product repo / widget keys are **candidates** — confirm in the live dump
- Re-dump after animations, keyboard open, or navigation
- Name PO fields with prefixes: `btn_`, `input_`, `txt_`, `msg_`
- Store dumps under `docs/locators/` for the session; **do not commit** `*.xml` dumps (see `.gitignore`)

## iOS alternative

Use Xcode Accessibility Inspector or Appium Inspector; save snapshot locally as `docs/locators/<screen>_ios.xml` (local only).
