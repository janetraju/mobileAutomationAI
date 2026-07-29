# Locator sheet — login_phone (CoFee, Android, Flutter)

Source dumps: `login_phone.xml` (Google phone-hint sheet visible, unfilled), `login_phone_filled.xml` (after valid number entered).
App: `cofee.life.app.dev` / `cofee.life.app.MainActivity`. Captured via `invoke ui:dump` + manual adb walk, 2026-07-27.

## Elements

| PO name | Element | Strategy | Locator value | Confirmed |
|---------|---------|----------|----------------|-----------|
| `txt_phone_title` | "What's your phone number?" title | `-android uiautomator` | `descriptionContains("phone number")` | yes (existing `loc_phone_title`) |
| `input_phone` | Phone number field | `class name` | `android.widget.EditText` (only EditText on screen) | yes (existing `loc_phone_input`) |
| `btn_next` | Submit / continue CTA | `accessibility id` | `Next` | yes, **conditionally** — see Notes |
| `btn_permission_allow` | System notification-permission "Allow" | `-android uiautomator` | `text("Allow")` | yes (existing `loc_permission_allow`) |

## Notes / hazards (not yet all handled in code)

1. **`btn_next` is only its own accessibility node once the phone field holds a value that passes validation.** Before typing, "Next" text is merged into an unrelated ad-card widget's giant `content-desc` (`"...make payment securely.\nNext"`) and is *not* independently locatable — confirmed via full-tree dump (`login_phone.xml`, no node has `content-desc=="Next"` exactly). After a valid 10-digit number is entered, a distinct `android.view.View` node with `content-desc="Next"` appears at its own bounds. `login_actions.py` already calls `enter_phone_number()` before `submit_phone_number()`, so this ordering is currently correct — the locator itself is not the bug.
2. **Google Play Services "Choose a phone number" bottom sheet (`com.google.android.gms`) appears automatically** the moment the phone `EditText` gains focus — no explicit tap needed. It is a **separate system window**, not part of the app, and fully covers the lower half of the screen including wherever "Next" would render. `login_actions.py` / `login_steps.py` have **no logic to detect or dismiss this dialog** today. Its dismiss control:
   - `content-desc="Cancel"`, `resource-id="com.google.android.gms:id/cancel"`, package `com.google.android.gms`.
   - This is very likely the actual cause of the login test's `submit_phone_number()` timeout (`loc_btn_next` never visible) — the sheet was still covering the screen.
3. **A debug FAB (purple circle, dev-build only) overlaps the right ~15% of the "Next" button's bounds** (`btn_next` bounds `[58,2193][1022,2319]` vs. FAB `[854,2135][1001,2282]`). `_tap_primary_cta()` in `login_actions.py` already works around this by tapping at `x_ratio=0.35` (left side) — confirmed correct, keep as-is.
4. The debug FAB itself is also a plain `android.widget.Button`, `NAF="true"`, no resource-id/content-desc — not independently locatable; avoid via coordinate offset only (as current code does).

## Recommended fix (not applied — flag for follow-up)

Add a dismiss step for the Google phone-number-hint sheet (by `accessibility id: Cancel`, scoped so it doesn't accidentally match an in-app "Cancel") right after tapping/focusing the phone input and before `submit_phone_number()`, mirroring how `dismiss_notification_permission_if_visible()` already handles the OS permission dialog.
