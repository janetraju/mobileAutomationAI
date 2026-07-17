# Locator sheet: Enable Partial Payment (`cofee-enable-partial-payment`)

Live-confirmed on `Pixel_7` emulator (Android), CoFee dev build (`cofee.life.app.dev`, versionCode 109).
Raw UI dump XMLs captured during discovery are local-only (`docs/locators/*.xml`
is gitignored per repo policy — see `docs/cofee-flow.md`'s Screen map note);
re-dump with `invoke ui:dump --screen=<name>` if you need to re-verify. This
file is the committed, durable record of what those dumps showed.

## Three distinct payment-list screens — don't conflate them

There are **three different ways** to reach a list of payment cards with
the kebab menu, and the action is confirmed live on all three:

1. **Per-member payment history** — Groups tab → tap a group → tap the
   member row. Screen title is the **member's name**, no month selector.
   All cards for that member across all time, filterable All/Paid/Pending.
2. **"Group payments"** (matches the Figma frame name exactly) — Groups tab
   → tap a group → tap **"Monthly Insights"** → tap a month card (e.g.
   "Jul '26 · 0/2 Paid · Due ₹3,999") → tap **"View payments"**. Screen
   title is literally **"Group payments"**, with a month selector (e.g.
   "July 2026") and the same All/Paid/Pending tabs — but scoped to **all
   members' cards for that month**, not one member's full history.
3. **"All payments"** (global, org-wide) — bottom nav **"Payments"** tab.
   Screen title is literally **"All payments"**, no group or month scoping
   — aggregates every pending/paid card across every group. Also reachable
   via Home → "Dues" → "View All".

All three screens use the same underlying card/kebab-menu widget
(`payment_card_bottom_actions.dart`) — confirmed live, identical menu
items and behavior on all three (tested with the same ₹2,000 payment on
each). Locators below apply to any of the three unless noted.

All strategies below are `content-desc` (→ `AppiumBy.ACCESSIBILITY_ID`) —
priority 1 per `AGENTS.md`. This app merges multiple text nodes into one
`content-desc` per Flutter semantics merging (e.g. a whole card's name +
group + amount + date in one string) — several locators below are
substring/contains matches on a merged block, not a clean single-purpose
label. Noted per element.

## Group Payments list (both screens share these locators)

Reached via either path above.

| PO name | Element | Strategy | Value | Confirmed |
|---------|---------|----------|-------|-----------|
| `txt_screen_title` | Screen title (screen 2 only) | accessibility id | `Group payments` | yes |
| `btn_monthly_insights` | "Monthly Insights" entry point (group detail) | accessibility id | `Monthly Insights` | yes |
| `card_month_insight` | Month card in the Monthly Insights sheet | accessibility id (contains) | merged block e.g. `Jul ' 26\n0/2\nPaid\nCollected\n₹\n0\nDue\n₹\n3,999` | yes — merged semantics |
| `btn_view_payments` | "View payments" button on a month card | accessibility id | `View payments` | yes |
| `ddl_month_selector` | Month selector on screen 2 | accessibility id | e.g. `July  2026` (double space is real, present live) | yes |
| `tab_all_payments` | "All" filter tab | accessibility id | `All` | yes |
| `tab_paid_payments` | "Paid" filter tab | accessibility id | `Paid` | yes |
| `tab_pending_payments` | "Pending" filter tab | accessibility id | `Pending` | yes |
| `card_payment` | Payment card (merged) | accessibility id (contains) | `<MemberName>\n<Group>-<Note>\n₹ <amount>\nRequested on <date>` — merged block, match via `contains("Requested on")` or the note text, not exact string | yes — **merged semantics**, see note below |
| `card_payment_partial_indicator` | "X%," prefix once partial payment is enabled | accessibility id (contains) | `0%,` prepended to the merged card block above | yes — only appears after enabling |
| `btn_send_reminder` | "Send reminder" button on card | accessibility id | `Send reminder` | yes |
| `btn_show_menu` | "⋮" kebab menu trigger on card | accessibility id | `Show menu` | yes |

**Merged semantics caveat:** `card_payment`'s content-desc is one merged
string (member name + group-note + amount + date). There is no separate
locator for "the amount" or "the date" alone — asserting on a specific
sub-value means asserting the whole merged string contains that substring.
This matches the Flutter merged-semantics pattern called out in the
taqwright reference skill.

## Kebab menu (before Enable Partial Payment)

| PO name | Element | Strategy | Value | Confirmed |
|---------|---------|----------|-------|-----------|
| `btn_mark_as_paid` | "Mark as paid" | accessibility id | `Mark as paid` | yes |
| `btn_share_payment_link` | "Share payment link" | accessibility id | `Share payment link` | yes — **not in original context file**, discovered live |
| `btn_disable_payment` | "Disable" | accessibility id | `Disable` | yes |
| `btn_enable_partial_payment` | "Enable Partial Payment" | accessibility id | `Enable Partial Payment` | yes — **visibility threshold pinpointed exactly: ₹1,999 does NOT show it, ₹2,000 DOES — `splitRequiredAmountMin = 2000`, inclusive (`>=`)** |
| `menu_dismiss_scrim` | Tap-outside-to-dismiss overlay | accessibility id | `Dismiss menu` | yes |

## Kebab menu (after Enable Partial Payment)

`btn_enable_partial_payment` **no longer renders** — confirmed by
re-opening the menu immediately after confirming; only `Mark as paid`,
`Share payment link`, `Disable` remain. No page refresh needed.

## Confirm dialog

| PO name | Element | Strategy | Value | Confirmed |
|---------|---------|----------|-------|-----------|
| `txt_confirm_title` | Dialog title | accessibility id | `Enable partial payment?` — **no space before `?`, unlike the Figma mockup's "Enable partial payment ?"** | yes |
| `txt_confirm_subtitle` | Dialog subtitle | accessibility id | `Once enabled, users will be able to make partial payment for this payment request ` (trailing space is real, present live) | yes |
| `btn_confirm_cancel` | "Cancel" | accessibility id | `Cancel` | yes |
| `btn_confirm_enable` | "Confirm" | accessibility id | `Confirm` | yes |

No success toast/snackbar appears after tapping Confirm — the only visible
change is the kebab menu losing the option and the card gaining a "0%,"
prefix (see above). Confirmed absence of any toast in this dump — don't
assert on one.

## Mark As Paid screen

Reached via `btn_mark_as_paid` on any payment card (partial-enabled or not).

| PO name | Element | Strategy | Value | Confirmed |
|---------|---------|----------|-------|-----------|
| `radio_full_amount` | "Full Amount" option | accessibility id | `Full Amount` | yes |
| `radio_enter_amount` | Partial-amount option | accessibility id | `Enter amount` — **live label differs from the code constant name `PARTIAL_AMOUNT`; there is no literal "Partial Amount" text on screen** | yes |
| `input_amount_paid` | Amount input field | class + index (EditText) | no stable accessibility id exposed; XPath/class-based (`android.widget.EditText`, first one under the amount section) — last-resort strategy | yes, but low-priority locator |
| `txt_amount_validation_error` | Inline validation message | accessibility id | `Amount should be less than 5,000` — **exact threshold value is the pending amount itself; message is dynamic, not a fixed string** | yes |
| `ddl_payment_mode` | "Payment Mode" selector | accessibility id | `Cash` (default value shown; the selector itself is `Payment Mode *`) | yes |
| `dt_payment_date` | "Payment Date" field | accessibility id | defaults to today's date, e.g. `15/07/26` | yes |
| `btn_proceed` | "Proceed" button | accessibility id | `Proceed` — **disabled (`enabled="false"`) when amount ≥ pending amount; enabled once a valid lower amount is entered** | yes |
| `btn_cancel_mark_as_paid` | "Cancel" button | accessibility id | `Cancel` | yes |

## Resolved open questions (from context file)

| # | Question | Resolution |
|---|----------|------------|
| 1 | Actual `splitRequiredAmountMin` value | **Pinpointed exactly: ₹2,000**, inclusive. Bisected live: ₹1,999 → no option; ₹2,000 → option present. |
| 2 | Success toast after enabling? | **No.** Confirmed no toast/snackbar; only the menu-item disappearance and the new "X%," card prefix are observable. |
| 4 | Does the menu item disappear immediately? | **Yes**, immediately — no refresh/re-open needed. |
| 5 | Partial-amount validation | **Confirmed:** must be strictly less than the pending amount ("Amount should be less than 5,000"); `Proceed` is disabled otherwise. |
| 6 | Figma vs code copy discrepancy ("? " spacing) | **Code/live wins:** no space before `?`. Figma mockup had a stray space. |
| 7 | Is the 3-item Figma kebab menu exhaustive? | **No** — live menu has 4 items (`Mark as paid`, `Share payment link`, `Disable`, `Enable Partial Payment`); `Share payment link` wasn't in the Figma capture or the original context file's code scan. |

Still open: subscription-tier gating details (not exercised — this test
account already had access).
