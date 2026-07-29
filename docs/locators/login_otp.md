# Locator sheet — login_otp (CoFee, Android, Flutter)

Source dump: `login_otp.xml`. App: `cofee.life.app.dev` / `cofee.life.app.MainActivity`. Captured 2026-07-27.

## Elements

| PO name | Element | Strategy | Locator value | Confirmed |
|---------|---------|----------|----------------|-----------|
| `txt_otp_title` | "We've sent a 6-digit code to..." title | `-android uiautomator` | `descriptionContains("6-digit code")` | yes (existing `loc_otp_title`) |
| `input_otp` | OTP code field (single merged EditText spanning all 6 boxes) | `class name` | `android.widget.EditText` | yes (existing `loc_otp_input`, reuses same class locator as phone screen) |
| `btn_next` | Submit CTA | `accessibility id` | `Next` | yes — present as its own node even while visually disabled (differs from login_phone, where it's only separated after valid input) |
| `lnk_resend_otp` | "Resend OTP." link | *(not currently in `login_po.py`)* | `content-desc` region `[279,691][470,733]`, text `" Resend OTP."` | not wired up — candidate for future negative/resend test cases |

## Notes

- Same debug-FAB overlap hazard as `login_phone` (`btn_next` bounds `[58,2193][1022,2319]` vs. FAB `[854,2135][1001,2282]`) — `_tap_primary_cta(x_ratio=0.35)` handles it correctly here too.
- The phone number entered is echoed back at the top (`content-desc="+91 63210 20200"`) — useful for an assertion if a test wants to confirm the correct number was carried over from the previous screen.
- No Google-services autofill sheet observed on this screen (the phone-hint sheet only triggers on the phone-number field).
