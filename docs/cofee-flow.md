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

UI dump XMLs are local/temporary — do not commit them. Locators live in page objects.

## Known blockers

| Blocker | Mitigation |
|---------|------------|
| Dev debug FAB (purple cloud) overlaps Save/Next | Tap left-center of CTAs via gesture |
| Promo modal after Save | Dismiss with **I'll share later** |
| Duplicate group name | Use runtime-unique name in test data |
| Login required | Reuse `user_ensures_logged_in_home` after P0-01 in same session |
| `Fee Collection Start Date` pre-filled | Leave default unless test requires change |
| Post-OTP screen can briefly linger | Accept only `home`/`org` as success — don't treat a lingering OTP screen as a pass |
| Org → home transition | Continue button is left-biased (debug FAB overlaps right side); "home" means CoFee's own nav (`Groups`/`Payments`), not the Android launcher |
| Onboarding carousel reappears after `pm clear` | Prefer seeding `hasIntroScreenShown` directly rather than tapping through the carousel each time |
| Create group tile locator | Use `ACCESSIBILITY_ID` / `descriptionMatches` for **Add New** / **Create group** — plain text match is unreliable |
| Member fee assertion | Indian currency formatting + embedded newlines in the accessibility label — match with one `descriptionMatches("(?s).*…*")`, not a plain equality check |

## Test data

| Item | Source |
|------|--------|
| Login phone / OTP | `TEST_MOBILE`, `TEST_OTP` in `.env` |
| Member name | Runtime unique, e.g. `AutoMember{timestamp}` |
| Member phone | `TEST_MEMBER_MOBILE` or generated 10-digit |
| Group name | Runtime unique, e.g. `AutoGroup{timestamp}` |
| Group amount | Parametrize, default `5000` |

## Locator notes (Flutter)

- Prefer `content-desc` / visible text
- Bottom sheet: **Select members**, **Manually**
- Save is full-width green button — not the purple FAB
