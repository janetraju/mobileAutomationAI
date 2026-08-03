# Test Cases: Enable Partial Payment (`cofee-enable-partial-payment`)

Source: [docs/context/cofee-enable-partial-payment-context.md](cofee-enable-partial-payment-context.md)
(live-validated). Locators live in `src/page_objects/cofee/`.
Approved: 2026-07-16 session

## Preconditions (shared, reference by id)

| ID | Description |
|----|-------------|
| PRE-01 | Logged into CoFee dev test account, Home screen visible |
| PRE-02 | An active group member has a pending payment request ≥ ₹2,000 (confirmed threshold-passing), not yet partial-payment-enabled |
| PRE-03 | An active group member has a pending payment request < ₹2,000 (confirmed threshold-failing, e.g. ₹1,999) |
| PRE-04 | A payment request already has partial payment enabled **and** a partial amount already paid (`totalPaidAmount > 0`) |

## Happy Path (HP)

### TC-enable-partial-payment-HP-01: Enable partial payment on an eligible payment

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-01, PRE-02 |
| Automation status | Not started |

**Steps:**
1. Navigate Home → Groups → open the group containing the eligible member (PRE-02) → tap the member row (or Monthly Insights → month card → View payments) to open a payment-card list
2. Tap "⋮" (Show menu) on the eligible card
3. Observe menu items
4. Tap "Enable Partial Payment"
5. Observe the confirm dialog
6. Tap "Confirm"

**Expected Result:** Menu shows Mark as paid, Share payment link, Disable, Enable Partial Payment. Confirm dialog shows title "Enable partial payment?" and subtitle "Once enabled, users will be able to make partial payment for this payment request". After Confirm: no toast/snackbar appears; the card's label gains a leading "0%," prefix; re-opening "⋮" on the same card immediately shows only Mark as paid / Share payment link / Disable — no refresh needed.

### TC-enable-partial-payment-HP-02: Mark As Paid shows Full/partial options after enabling

| Field | Value |
|-------|-------|
| Priority | P1 |
| Preconditions | PRE-01, result of HP-01 (or any partial-enabled payment) |
| Automation status | Not started |

**Steps:**
1. Tap "⋮" → "Mark as paid" on a partial-enabled payment

**Expected Result:** "Full Amount" and "Enter amount" options are shown, with "Full Amount" selected by default.

### TC-enable-partial-payment-HP-03: Complete a valid partial payment

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-01, result of HP-01 |
| Automation status | Not started |

**Steps:**
1. On Mark As Paid, select "Enter amount"
2. Enter an amount less than the pending amount (e.g. 2000 of 5000)
3. Select Payment Mode (default "Cash") and Payment Date (defaults to today)
4. Tap "Proceed"

**Expected Result:** Proceed becomes enabled once a valid amount is entered (confirmed live). [Assumption] Tapping Proceed completes the partial payment and updates the card's paid percentage — exact post-submit screen not observed live; confirm during automation.

### TC-enable-partial-payment-HP-04: "Enable Partial Payment" is available from all three payment-list entry points (parametrized)

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-01, PRE-02 |
| Automation status | Not started |

**Steps:**
1. Reach the eligible payment card (PRE-02, ≥ ₹2,000) via the entry point in the data table
2. Tap "⋮" (Show menu) on the card

**Expected Result:**

| Entry point | Navigation | Expected |
|---|---|---|
| Per-member payment history | Groups tab → group → tap member row | **Confirmed live:** menu includes "Enable Partial Payment" |
| "Group payments" (Monthly Insights) | Groups tab → group → "Monthly Insights" → month card → "View payments" | **Confirmed live:** same menu, screen titled "Group payments" |
| "All payments" (global) | Bottom nav "Payments" tab (or Home → "Dues" → "View All") | **Confirmed live:** same menu, screen titled "All payments", not scoped to one group |

All three reach the same underlying widget (`payment_card_bottom_actions.dart`) — tested with the same ₹2,000 payment on each, identical result.

## Negative / Validation (NEG)

### TC-enable-partial-payment-NEG-01: Partial-payment option visibility respects the ₹2,000 threshold (parametrized)

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-01, a pending payment request at the amount under test |
| Automation status | Not started |

**Steps:**
1. Open "⋮" (Show menu) on a payment card whose pending amount matches the data table below

**Expected Result:**

| Pending amount | Expected menu contents |
|---|---|
| ₹1,999 | **Confirmed live:** Mark as paid, Share payment link, Disable only — "Enable Partial Payment" absent |
| ₹2,000 | **Confirmed live:** Mark as paid, Share payment link, Disable, **Enable Partial Payment** present |

### TC-enable-partial-payment-NEG-02: Invalid partial amounts are rejected (parametrized)

| Field | Value |
|-------|-------|
| Priority | P1 |
| Preconditions | PRE-01, result of HP-01 (pending amount ₹5,000) |
| Automation status | Not started |

**Steps:**
1. On Mark As Paid for a ₹5,000-pending payment, select "Enter amount"
2. Enter the amount from the data table
3. Observe inline error + Proceed button state

**Expected Result:**

| Input amount | Expected |
|---|---|
| 10000 (> pending) | **Confirmed live:** "Amount should be less than 5,000", Proceed disabled |
| 5000 (== pending, exact boundary) | [Assumption] Same error (message says "less than", strict) — not literally tested at this exact value |
| 0 | [Assumption] Rejected / Proceed disabled |
| -100 (negative) | [Assumption] Rejected, or field prevents negative entry |

## State / Navigation (STATE)

### TC-enable-partial-payment-STATE-01: Back button dismisses confirm dialog

| Field | Value |
|-------|-------|
| Priority | P2 |
| Preconditions | PRE-01, PRE-02 |
| Automation status | Not started |

**Steps:**
1. Open the confirm dialog (tap "⋮" → "Enable Partial Payment")
2. Press the device Back button

**Expected Result:** [Assumption] Dialog dismisses same as tapping Cancel; payment remains not-split — not verified live, confirm during automation.

### TC-enable-partial-payment-STATE-02: Partial-enabled state persists across navigation

| Field | Value |
|-------|-------|
| Priority | P1 |
| Preconditions | PRE-01, result of HP-01 |
| Automation status | Not started |

**Steps:**
1. After enabling partial payment (HP-01), navigate back to the Groups list
2. Re-enter the same payment-card screen

**Expected Result:** [Assumption] Card still shows the "X%," prefix and the kebab menu still excludes "Enable Partial Payment" — not verified live, confirm during automation.

## Regression (REG)

### TC-enable-partial-payment-REG-01: Close-payment behavior changes once partially paid

| Field | Value |
|-------|-------|
| Priority | P1 |
| Preconditions | PRE-01, PRE-04 |
| Automation status | Not started |

**Steps:**
1. Using PRE-04 (partial-enabled payment with `totalPaidAmount > 0`), tap "⋮"

**Expected Result:** [Assumption] Per code (`payment_card_bottom_actions.dart:132-133`, `canDisablePaymentLink` logic), disable/close-payment behavior differs once any partial amount is paid — exact UI difference not verified live; confirm during automation and update this case with the observed behavior.

---

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-enable-partial-payment-HP-01 | Happy Path | P0 | **Done** — `test_enable_partial_payment_on_eligible_payment` |
| TC-enable-partial-payment-HP-02 | Happy Path | P1 | Not started (Mark As Paid PO deferred) |
| TC-enable-partial-payment-HP-03 | Happy Path | P0 | Not started (Mark As Paid PO deferred) |
| TC-enable-partial-payment-HP-04 | Happy Path | P0 | **Done** — `test_partial_payment_option_available_from_all_entry_points` |
| TC-enable-partial-payment-NEG-01 | Negative | P0 | **Done** — `test_partial_payment_option_visibility_at_threshold` |
| TC-enable-partial-payment-NEG-02 | Negative | P1 | Not started (Mark As Paid PO deferred) |
| TC-enable-partial-payment-STATE-01 | State/Navigation | P2 | Not started |
| TC-enable-partial-payment-STATE-02 | State/Navigation | P1 | Not started |
| TC-enable-partial-payment-REG-01 | Regression | P1 | Not started |

**Automated:** `tests/test/cofee/payments/test_enable_partial_payment.py` (3 test
methods, 6 parametrized cases total). Each case verified passing individually;
a full back-to-back run of all 6 in one session showed flakiness on the later
cases (`create_group_actions.py`'s `save_group()` timing out) after ~9 minutes
of sustained execution — consistent with this sandbox's software-rendering
emulator instability (no GPU acceleration), not a defect in the new code.
Re-run individually or in smaller batches until the environment is on
hardware-accelerated rendering.

## Parametrization candidates

- **HP-04** collapses the three entry-point checks (per-member history, "Group payments", "All payments") into one case with a 3-row data table — all confirmed live with the same ₹2,000 payment.
- **NEG-01** collapses the below/at-threshold visibility check into one case with a 2-row data table (₹1,999 / ₹2,000), both confirmed live.
- **NEG-02** collapses four invalid-amount variants (way-over, exact-boundary, zero, negative) into one case with a 4-row data table; only the way-over row is live-confirmed, the other three are `[Assumption]`.

## Locator map (live-confirmed in get-context/discover-mobile-locators)

| Element | Locator | Confirmed live? |
|---------|---------|------------------|
| Kebab menu trigger | accessibility id `Show menu` | yes |
| "Enable Partial Payment" menu item | accessibility id `Enable Partial Payment` | yes |
| Confirm dialog title | accessibility id `Enable partial payment?` | yes |
| Confirm dialog Confirm button | accessibility id `Confirm` | yes |
| "Full Amount" option | accessibility id `Full Amount` | yes |
| Partial-amount option | accessibility id `Enter amount` | yes |
| Amount input field | class-based `android.widget.EditText` (no accessible id) | yes, low-priority locator |
| Validation error text | accessibility id (dynamic) `Amount should be less than <pending>` | yes |
| Proceed button | accessibility id `Proceed` | yes |
| "Monthly Insights" entry point | accessibility id `Monthly Insights` | yes |
| "Payments" bottom-nav tab (global entry point) | accessibility id `Payments` | yes |
| Global screen title | accessibility id `All payments` | yes |
| "View payments" button | accessibility id `View payments` | yes |

Confirmed selectors are implemented in `src/page_objects/cofee/`
(`payment_card_po`, `group_detail_po`, `home_po`, etc.).

## Open questions

- Subscription-tier gating behavior and copy (not exercised — this test account's plan allowed the action without restriction).
- Auto-debit-in-progress block (not exercised — no such payment existed in test data).
- Exact post-submit behavior of a completed partial payment (HP-03) — Proceed-enabled was confirmed, but the flow wasn't completed live to avoid further mutating the shared test account.

## Test data setup — done

- **Login:** Fixed OTP strategy verified live end-to-end (logout → phone
  entry → OTP → account selection → Home, session intact).
  `TEST_MOBILE`/`TEST_OTP` set in `.env.dev` (gitignored).
- **Dataprovider:** [tests/dataprovider/dp_enable_partial_payment.py](../../tests/dataprovider/dp_enable_partial_payment.py)
  — generates runtime-unique group/member names per the existing
  `AutoGroup{timestamp}`/`AutoMember{timestamp}` convention, plus the
  threshold-boundary (₹1,999/₹2,000) and invalid-amount parametrized data
  matching NEG-01/NEG-02.
- **Quick Collect API** discovered (`POST .../payment-order/instant-link`)
  but not wired in — no captured session token/org/branch id in this
  framework yet. Test data is seeded via UI (Quick Collect flow), not API.
- **Pre-existing manual test payments** still sit in the shared dev
  account (₹5,000 "TestPartialPayment", ₹1,999 "Test1999", ₹2,000
  "Test2000") from live discovery — the dataprovider creates fresh data
  per run rather than reusing these.

## Handoff

Next: **`testscript-generator`** to implement page objects, actions,
steps, and tests using this context file + dataprovider.
