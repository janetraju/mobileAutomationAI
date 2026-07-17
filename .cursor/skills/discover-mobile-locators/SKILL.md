---
name: discover-mobile-locators
description: >-
  Discover real mobile UI locators by installing the app on a device or emulator
  and capturing accessibility trees. Use before writing page objects, when
  onboarding a new app, after UI changes, or when APK analysis is insufficient
  for Flutter, React Native, or hybrid apps.
disable-model-invocation: true
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

### 3b. Appium MCP (live tree — mandatory for new TCs)

**Required before any new test scenario** — see **`automate-a-flow` Step 2d**.
Also use when `invoke ui:dump` is stale or you need interactive exploration.

Project **Appium MCP** server (`.cursor/mcp.json`):

1. Ensure emulator/device is running and `.env` matches
   `environment/appium-mcp.capabilities.json`
2. `select_device` → `appium_session_management` (`action=create`)
3. Walk the full scenario — navigate each screen via `appium_gesture` /
   `appium_set_value`
4. Per screen: `appium_get_page_source` → save to `docs/locators/<screen>.xml`
5. `generate_locators` on key screens — **confirm every selector** against page
   source and app strings before `*_po.py`

Screenshots land in `target/mcp-screenshots/` when `NO_UI=true`.

### 4. Parse dump — locator priority

| Priority | Android (UiAutomator2) | iOS (XCUITest) |
|----------|------------------------|----------------|
| 1 | `content-desc` → `ACCESSIBILITY_ID` | `accessibility id` |
| 2 | `resource-id` | `name` / predicate |
| 3 | `text` | `label` / predicate |
| 4 | `class` + index | class chain |
| 5 | XPath | XPath (last resort) |

### 5. Naming convention

Use these names on the locator sheet **and** in `*_po.py` so dumps map 1:1 to code.

#### Element-type prefixes (PO field / method stem)

| Prefix | Element kind | Example stem |
|--------|--------------|--------------|
| `btn_` | Button / tappable CTA | `btn_continue`, `btn_quick_collect` |
| `input_` | Text field / EditText | `input_mobile`, `input_otp` |
| `txt_` | Static label / title | `txt_welcome`, `txt_phone_title` |
| `msg_` | Error / snackbar / toast | `msg_whitelist_error` |
| `chk_` | Checkbox / switch | `chk_terms` |
| `ddl_` | Dropdown / picker | `ddl_org` |
| `lnk_` | Link / text button | `lnk_view_payments` |
| `icn_` | Icon-only control | `icn_kebab_menu` |
| `tab_` | Bottom / top tab | `tab_groups` |
| `card_` | List / payment card | `card_member` |

Snake_case only. Stem = role + screen-meaningful name (`btn_enable_partial_payment`, not `btn1`).

#### Strategy suffixes (private locator attrs in `# --- Locators ---`)

| Suffix | Strategy | Example attr |
|--------|----------|--------------|
| `_acc` | `ACCESSIBILITY_ID` / content-desc | `_btn_continue_acc` |
| `_uia` | `ANDROID_UIAUTOMATOR` | `_btn_add_members_uia` |
| `_ios` | `IOS_PREDICATE` / `IOS_CLASS_CHAIN` | `_btn_continue_ios` |
| `_class` | `CLASS_NAME` | `_input_phone_class` |
| `_text` | text-based UiSelector / label | `_btn_allow_text` |
| `_xpath` | XPath — last resort; justify in comment | `_card_member_xpath` |

Pattern: `self._<prefix><name>_<strategy>`

#### Public PO methods

| Method | Returns | Example |
|--------|---------|---------|
| `find_<prefix><name>()` | `WebElement` | `find_btn_continue()` |
| `loc_<prefix><name>()` | `(by, value)` tuple for waits | `loc_btn_continue()` |

Do **not** put the strategy suffix on `find_*` / `loc_*` — only on the private attr.

#### Dump / sheet file names

| Artifact | Pattern | Example |
|----------|---------|---------|
| UI dump | `docs/locators/<screen>.xml` | `login_phone.xml`, `home_logged_in.xml` |
| iOS dump | `docs/locators/<screen>_ios.xml` | `login_otp_ios.xml` |
| Locator sheet | `docs/locators/<screen>.md` (optional) | PO name column = method stem (`input_mobile`) |

Screen names: lowercase snake_case, no spaces (`group_detail`, not `Group Detail`).

### 6. App-type notes

| `APP_TYPE` | Guidance |
|------------|----------|
| `flutter` | Prefer `content-desc` / semantic labels; text like `"Enter mobile number"` often works; avoid brittle XPath into `android.view.View` |
| `rn` | Look for `content-desc` matching `testID` / `accessibilityLabel` |
| `hybrid` | Dump in native context; switch WebView for H5 screens (`switch_to_webview` in actions) |
| `native` | `resource-id` usually stable |

### 7. Produce locator sheet

For each interactive element, document in `docs/<app_slug>-flow.md` or `docs/locators/<screen>.md`:

| PO name | Element | Strategy | Locator value | Confirmed |
|---------|---------|----------|---------------|-----------|
| `input_mobile` | Phone field | accessibility id | `...` | yes |
| `btn_continue` | Submit CTA | accessibility id | `Continue` | yes |

PO name = method stem (`input_mobile` → `find_input_mobile` / `loc_input_mobile`).

### 8. Hand off to `mobile-appium-python`

Only after locator sheet exists for the screen.

## Rules

- Never guess locators from APK decompilation or product source alone
- Product repo / widget keys are **candidates** — confirm in the live dump
- Re-dump after animations, keyboard open, or navigation
- Follow **§5 Naming convention** — prefixes + strategy suffixes + `find_*` / `loc_*`
- Store dumps under `docs/locators/` for the session; **do not commit** `*.xml` dumps (see `.gitignore`)

## iOS alternative

Use Xcode Accessibility Inspector or Appium Inspector; save snapshot locally as `docs/locators/<screen>_ios.xml` (local only).
