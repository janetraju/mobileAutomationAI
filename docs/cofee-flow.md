# CoFee — Flow Documentation

**App:** CoFee dev (`cofee.life.app.dev`) · **Type:** Flutter · **Platform:** Android  
**API:** `https://api.dev.cofee.life`

## Login happy path (automated)

1. Fresh install → notification Allow (if shown)
2. Onboarding carousel → phone entry
3. Enter mobile → OTP → account picker → Continue → Home

| ID | Flow | Priority | Automation status | Notes |
|----|------|----------|-------------------|-------|
| P0-01 | Phone + OTP login | P0 | **Done** | `tests/test/cofee/login/test_login.py` |
| P0-02 | Post-login home visible | P0 | **Done** | Covered in P0-01 |

## Create group happy path (from screenshots — confirmed)

**Precondition:** Logged in as **Individual** account (`test individual`).

| Step | Screen | Action |
|------|--------|--------|
| 1 | Home | Tap **Add New** (+) in Groups section |
| 2 | Select members (bottom sheet) | Tap **Manually** |
| 3 | Add member | Enter **Name**, **Mobile Number**, tap **Add** |
| 4 | Create group | Form with 1 member pre-added |
| 5 | Create group | Enter **Group name** and **Amount** (fee) |
| 6 | Create group | Tap **Fee Collection Day** → opens schedule modal |
| 7 | Schedule payment collection | Select **Last day of the month** → **Apply** |
| 8 | Create group | Tap **Save** (green bar — avoid dev FAB on right) |
| 9 | Promo modal | Tap **I'll share later** |
| 10 | Group detail | Verify group name, member count, fee amount |

**Success criteria (step 10):**

- Header shows group name (e.g. `Test group1`)
- Subtitle: `1 Active Member` (or member count badge)
- Member row shows name and **Fee amount** matching entered amount
- Overview cards visible (Amount Collected / Amount Due)

## Create group — weekly fee collection (from product repo)

**Source:** `builds/cofee-app-develop` — `WeeklyFrequencySelector`, `group_settings.dart` frequencySelectors  
**Precondition:** Same as above (logged-in Individual).

| Step | Screen | Action |
|------|--------|--------|
| 1–6 | Same as P0-03 | Through opening schedule modal |
| 7 | Schedule payment | Open **Frequency** dropdown (default Monthly) → **Weekly** |
| 8 | Schedule payment | Tap weekday chip **Mon** → **Apply** |
| 9 | Create group | Field shows **`Weekly: Monday`** → **Save** |
| 10–11 | Promo → Group detail | Same success criteria as P0-03 |

| ID | Flow | Priority | Automation status | Context | Notes |
|----|------|----------|-------------------|---------|-------|
| P0-03 | Create group with manual member (monthly last day) | P0 | **Done** | screenshots | `test_create_group_with_manual_member` |
| P0-04 | Create group with weekly Monday fee | P0 | **Done** | product repo | `test_create_group_with_weekly_fee_collection` |
| P1-01 | Create group from contacts | P1 | Not started | product repo | Requires contacts permission |
| P1-02 | Create group with installments toggle | P1 | Not started | product repo | Amount ≥ org `splitRequiredAmountMin` |
| P1-03 | Create group with two manual members | P1 | Not started | product repo | Members `+` on create form |

## Enable Partial Payment (from live discovery — confirmed)

Full context: [docs/context/cofee-enable-partial-payment-context.md](context/cofee-enable-partial-payment-context.md)
· locators: [docs/locators/enable_partial_payment.md](locators/enable_partial_payment.md)
· test cases: [docs/context/cofee-enable-partial-payment-testcases.md](context/cofee-enable-partial-payment-testcases.md)

**Precondition:** A pending payment request ≥ **₹2,000** (confirmed exact
threshold — `splitRequiredAmountMin`), reachable from any of three screens
that share the same card/kebab widget:

| Entry point | Navigation |
|---|---|
| Per-member payment history | Groups → group → tap member row |
| "Group payments" (matches Figma) | Groups → group → Monthly Insights → month card → View payments |
| "All payments" (global) | Bottom nav Payments tab, or Home → Dues → View All |

| Step | Screen | Action |
|------|--------|--------|
| 1 | Payment card | Tap "⋮" (Show menu) |
| 2 | Kebab menu | Tap **Enable Partial Payment** (only shown when amount ≥ ₹2,000) |
| 3 | Confirm dialog | Tap **Confirm** — no success toast; card gains a "0%," prefix, option disappears immediately |
| 4 | Mark As Paid | Select **Enter amount** (not "Partial Amount") for a partial payment |

| ID | Flow | Priority | Automation status | Notes |
|----|------|----------|-------------------|-------|
| P0-04 | Enable partial payment on eligible request | P0 | **Done** | `tests/test/cofee/payments/test_enable_partial_payment.py` |
| P0-05 | Threshold visibility (₹1,999 vs ₹2,000) | P0 | **Done** | Same file, parametrized |
| P0-06 | Option present from all 3 entry points | P0 | **Done** | Same file, parametrized |
| P1-03 | Mark As Paid — Full/partial toggle + amount validation | P1/P0 | Not started | Needs `mark_as_paid_po.py` |

## Screen map

| Screen | Entry | Page object | Locator discovery |
|--------|-------|-------------|-------------------|
| Home | After login | `home_po.py` | `invoke ui:dump --screen=home_logged_in` |
| Select members | Add New | `create_group_po.py` | `invoke ui:dump --screen=select_members` |
| Add member | Manually | `create_group_po.py` | `invoke ui:dump --screen=add_member` |
| Create group | After Add member | `create_group_po.py` | `invoke ui:dump --screen=create_group` |
| Schedule payment | Fee Collection Day | `create_group_po.py` | `invoke ui:dump --screen=schedule_payment` |
| Promo share | After Save | `create_group_po.py` | `invoke ui:dump --screen=share_promo` |
| Group detail | After I'll share later | `group_detail_po.py` | `invoke ui:dump --screen=group_detail` |
| Quick Collect (member/amount/note) | Group detail → Quick Collect | `quick_collect_po.py` | `invoke ui:dump --screen=quick_collect` |
| Payment card / kebab menu (3 screens) | See Enable Partial Payment table above | `payment_card_po.py` | `invoke ui:dump --screen=payment_card_kebab` — see [enable_partial_payment.md](locators/enable_partial_payment.md) for the confirmed locator table |

UI dump XMLs are local/temporary — do not commit them (`docs/locators/*.xml`
is gitignored). Locators live in page objects; the markdown locator
*sheets* under `docs/locators/*.md` (e.g. `enable_partial_payment.md`) are
committed reference documentation, not raw dumps.

## Known blockers

| Blocker | Mitigation |
|---------|------------|
| Dev debug FAB (purple cloud) overlaps Save/Next | Tap left-center of CTAs via gesture |
| Promo modal after Save | Dismiss with **I'll share later** |
| Duplicate group name | Use runtime-unique name in test data |
| Login required | Reuse `user_ensures_logged_in_home` after P0-01 in same session |
| `Fee Collection Start Date` pre-filled | Leave default unless test requires change |
| Group detail has no bottom nav (full-screen stacked view) | Call `HomeActions.return_to_home_dashboard()` before tapping any bottom-nav tab |
| Quick Collect's confirm button text is dynamic ("Add 1 member") | Match via `descriptionContains`, not exact "Add members" |
| Kebab-menu "Show menu" is a descendant of the card's container, not a sibling | Use XPath descendant axis (`//*[contains(@content-desc,"X")]//*[@content-desc="Show menu"]`), not UiAutomator `fromParent()` |
| Emulator occasionally crashes/degrades under sustained runs (software rendering, no GPU accel in this sandbox) | Re-run failed cases individually; not a code defect — see `enable-partial-payment-testcases.md` automation notes |
| `TEST_MOBILE` must be the **10-digit local number only, no `+91` prefix** | The login screen's country-code chip (🇮🇳 +91) is a separate fixed element; `enter_phone_number()` types the value char-by-char straight into the local-number field — a `+91` prefix corrupts the digits |

## Test data

| Item | Source |
|------|--------|
| Login phone / OTP | `TEST_MOBILE`, `TEST_OTP` in `.env.dev` (gitignored — **fixed OTP strategy**, verified live end-to-end 2026-07-16: logout → phone entry → OTP → account picker → Home) |
| Member name | Runtime unique, e.g. `AutoMember{timestamp}` |
| Member phone | `TEST_MEMBER_MOBILE` or generated 10-digit |
| Group name | Runtime unique, e.g. `AutoGroup{timestamp}` |
| Group amount | Parametrize, default `5000` |
| Quick Collect payment amount (enable-partial-payment feature) | Parametrize via `dp_enable_partial_payment.py` — `1999` (below threshold), `2000` (at threshold), `5000`/`10000` (validation cases) |

### OTP strategy detail

**Fixed OTP in dev**, per `setup-mobile-test-data` skill. `TEST_MOBILE` /
`TEST_OTP` live in `.env.dev` (gitignored, never committed) — copy
`.env.dev.example` and fill in locally. `dp_login.py` fails fast if either
is unset. No API-based OTP generation/debug endpoint is wired up; this is
the only strategy currently supported for this account.

### Quick Collect API (discovered, not yet used for seeding)

`POST {API_BASE_URL}/v1/organisation/{orgId}/branch/{branchId}/payment-order/instant-link`
(`lib/app/data/api/api_endpoints.dart:35`, `quick_collect_repository.dart`)
creates a payment request server-side. Not wired into `api_client.py` yet
— requires a captured session bearer token plus org/branch IDs, neither of
which this framework extracts today. Current test data for this feature is
seeded **via UI** (Quick Collect flow), not via direct API call. Revisit if
UI-based seeding becomes a speed bottleneck.

## Locator notes (Flutter)

- Prefer `content-desc` / visible text
- Bottom sheet: **Select members**, **Manually**
- Save is full-width green button — not the purple FAB
