---
name: discover-mobile-locators
description: >-
  Captures and verifies UI locators from a running app via ui:dump and Appium
  MCP; defines locator priority, PO naming, and dump paths. Use when creating
  page objects, adding test scenarios, fixing stale locators, refreshing UI
  dumps, or when the user mentions locators, selectors, or UI inspection.
---
# Capture UI Locators

Capture and verify UI locators from a **running application** using `ui:dump`
and Appium MCP.

**Owns:** locator priority, PO naming, dump paths, and the dump/MCP workflow.  
**Repo contract (layers, waits, markers):** [AGENTS.md](../../../AGENTS.md).

## When to Use

Use this skill when:

- Creating a new `*_po.py` file
- Adding a new test scenario (MCP walkthrough required)
- UI changes have invalidated existing locators
- Refreshing stale UI dumps
- Working with Flutter, React Native, or hybrid applications

> Product source, APK analysis, and Figma can provide candidate locators, but
> **every locator must be verified on a live application**.

---

## Locator strategy (source of truth)

### Priority (highest first)

1. `AppiumBy.ACCESSIBILITY_ID` / content-desc  
2. Android `ANDROID_UIAUTOMATOR` / resource-id  
3. iOS `IOS_PREDICATE` / `IOS_CLASS_CHAIN`  
4. Text / label  
5. XPath — last resort; justify in a comment  

### Naming (PO fields)

| Prefix | Kind | Example |
|--------|------|---------|
| `btn_` | Button / CTA | `btn_continue` |
| `input_` | Text field | `input_mobile` |
| `txt_` | Static label | `txt_title` |
| `msg_` | Error / toast | `msg_whitelist_error` |
| `chk_` | Checkbox / switch | `chk_terms` |
| `ddl_` | Dropdown | `ddl_org` |
| `lnk_` | Link | `lnk_view_payments` |
| `icn_` | Icon-only | `icn_kebab_menu` |
| `tab_` | Tab | `tab_groups` |
| `card_` | Card / list row | `card_member` |

Private attrs: `self._<prefix><name>_<strategy>` (`_acc`, `_uia`, `_ios`, `_text`, `_xpath`).  
Public API: `find_<prefix><name>()` → element; `loc_<prefix><name>()` → `(by, value)` for waits.  
Do **not** put strategy suffixes on `find_*` / `loc_*`.

### Dumps

`docs/locators/<screen>.xml` — **local only** (gitignored); do not commit.  
iOS: `docs/locators/<screen>_ios.xml`.

### Preference by app type

| APP_TYPE | Preferred locator |
|----------|-------------------|
| `flutter` | `content-desc` / Semantics |
| `rn` | `testID` / `accessibilityLabel` |
| `hybrid` | Native hierarchy (WebView only when required) |
| `native` | `resource-id` |

---

## Workflow

### Step 1 — Prepare the Environment

```bash
invoke appium:doctor
invoke emulator:start        # or connect a physical device
invoke app:install           # uses APP_PATH from .env
```

Verify in `.env`: `APP_SLUG`, `APP_TYPE`, `PLATFORM`, `APP_PACKAGE`, `APP_ACTIVITY`.  
Keep `environment/appium-mcp.capabilities.json` aligned with `.env`.

### Step 2 — Capture Static UI Dumps

```bash
adb shell am start -n <APP_PACKAGE>/<APP_ACTIVITY>
invoke ui:dump --screen=<screen_name>   # → docs/locators/<screen_name>.xml
```

Repeat per screen. Do **not** commit the XML files.

### Step 3 — Walk the Flow with Appium MCP

**Mandatory** for every new test scenario.

1. `select_device` → `appium_session_management` (`action=create`)  
2. Navigate with `appium_gesture` / `appium_set_value` / `appium_find_element`  
3. Per screen: screenshot → page source → save XML → `generate_locators`  
4. Confirm every generated locator against page source and visible UI  

| Scenario | Action |
|----------|--------|
| Fresh login | Clear app data and relaunch |
| Logged-in session | Reuse the existing session |
| Downstream flow | Complete login before continuing |

Screenshots when `NO_UI=true`: `target/mcp-screenshots/`.

Re-dump after animations, keyboard, or navigation.

### Step 4 — Build the Locator Sheet

Apply **Locator strategy** above. Optional sheet:

```text
docs/locators/<screen>.md
```

| Page Object | Element | Strategy | Locator | Confirmed |
|-------------|---------|----------|---------|-----------|

PO name = method stem (`input_mobile` → `find_input_mobile` / `loc_input_mobile`).

### Step 5 — Summarize Findings

- Screens visited (order)  
- Confirmed UI text  
- Verified strategy per screen  
- Quirks / overlays  
- Gaps vs expected flow  

### Step 6 — Hand Off

→ `testscript-generator` (do **not** author `*_po.py` in this skill).

## Rules

- Never invent locators from APK / product source / Figma alone  
- Never write Page Object files here  
- Never commit generated XML dumps  

## Related Skills

`testscript-generator` · `get-context` · [AGENTS.md](../../../AGENTS.md)
