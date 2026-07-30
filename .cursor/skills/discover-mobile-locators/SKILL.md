# Capture UI Locators

Capture and verify UI locators from a **running application** using `ui:dump` and Appium MCP.

This skill is responsible only for capturing and validating locators. Locator priority, naming conventions, and Page Object patterns are defined in `AGENTS.md`.

## When to Use

Use this skill when:

- Creating a new `*_po.py` file
- Adding a new test scenario (MCP walkthrough required)
- UI changes have invalidated existing locators
- Refreshing stale UI dumps
- Working with Flutter, React Native, or hybrid applications

> Product source, APK analysis, and Figma can provide candidate locators, but **every locator must be verified on a live application**.

## Workflow

### Step 1 — Prepare the Environment

Run:

```bash
invoke appium:doctor
invoke emulator:start        # or connect a physical device
invoke app:install           # uses APP_PATH from .env
```

Verify the following values in `.env`:

- `APP_SLUG`
- `APP_TYPE`
- `PLATFORM`
- `APP_PACKAGE`
- `APP_ACTIVITY`

Ensure `environment/appium-mcp.capabilities.json` matches the `.env` configuration.

---

### Step 2 — Capture Static UI Dumps

Launch the application:

```bash
adb shell am start -n <APP_PACKAGE>/<APP_ACTIVITY>
```

Capture the current screen:

```bash
invoke ui:dump --screen=<screen_name>
```

This creates:

```
docs/locators/<screen_name>.xml
```

Repeat for each screen in the flow.

Do **not** commit `docs/locators/*.xml`.

---

### Step 3 — Walk the Flow with Appium MCP

This step is **mandatory** for every new test scenario.

Create a session:

- `select_device`
- `appium_session_management (action=create)`

Walk through the application using:

- `appium_gesture`
- `appium_set_value`
- `appium_find_element`

For each screen:

1. Capture a screenshot.
2. Retrieve the page source.
3. Save the XML dump to `docs/locators/<screen>.xml`.
4. Run `generate_locators`.
5. Verify every generated locator against both:
   - Page source
   - Visible UI text

### Common Preconditions

| Scenario | Action |
|----------|--------|
| Fresh login | Clear app data and relaunch |
| Logged-in session | Reuse the existing session |
| Downstream flow | Complete login before continuing |

When `NO_UI=true`, screenshots should be stored in:

```
target/mcp-screenshots/
```

---

### Step 4 — Build the Locator Sheet

Apply the locator priority and naming conventions defined in `AGENTS.md`.

Optionally document the results in:

```
docs/locators/<screen>.md
```

Recommended format:

| Page Object | Element | Strategy | Locator | Confirmed |
|-------------|---------|----------|---------|-----------|

### Locator Preference by App Type

| APP_TYPE | Preferred Locator |
|----------|-------------------|
| `flutter` | `content-desc` / Semantics |
| `rn` | `testID` / `accessibilityLabel` |
| `hybrid` | Native hierarchy (switch to WebView only when required) |
| `native` | `resource-id` |

Re-capture dumps whenever:

- animations complete
- the keyboard changes the layout
- navigation changes the UI

---

### Step 5 — Summarize Findings

Before handing off, provide:

- Screens visited (in order)
- Confirmed UI text
- Verified locator strategy for each screen
- UI quirks or overlays
- Gaps between the implemented UI and the expected flow

---

### Step 6 — Hand Off

Once the locator sheet is complete, hand off to:

- `mobile-appium-python`, or
- `automate-a-flow`

## Rules

- Never author Page Object files in this skill.
- Never rely solely on APK analysis, product source, or Figma.
- Every locator must be confirmed in a live session.
- Save iOS dumps as `docs/locators/<screen>_ios.xml`.
- Never commit generated XML dumps.

## Related Skills

- `automate-a-flow`
- `get-context`
- `mobile-appium-python`