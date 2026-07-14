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

| ID | Flow | Priority | Automation status | Notes |
|----|------|----------|-------------------|-------|
| P0-03 | Create group with manual member | P0 | **Done** | `tests/test/cofee/groups/test_create_group.py` |
| P1-01 | Create group from contacts | P1 | Not started | Requires contacts permission |
| P1-02 | Create group with installments toggle | P1 | Not started | |

## Screen map

| Screen | Entry | Page object | Locator dump |
|--------|-------|-------------|--------------|
| Home | After login | `home_po.py` | `docs/locators/home_logged_in.xml` |
| Select members | Add New | `create_group_po.py` | `docs/locators/select_members.xml` |
| Add member | Manually | `create_group_po.py` | `docs/locators/add_member.xml` |
| Create group | After Add member | `create_group_po.py` | `docs/locators/create_group.xml` |
| Schedule payment | Fee Collection Day | `create_group_po.py` | `docs/locators/schedule_payment.xml` |
| Promo share | After Save | `create_group_po.py` | `docs/locators/share_promo.xml` |
| Group detail | After I'll share later | `group_detail_po.py` | `docs/locators/group_detail.xml` |

## Known blockers

| Blocker | Mitigation |
|---------|------------|
| Dev debug FAB (purple cloud) overlaps Save/Next | Tap left-center of CTAs via gesture |
| Promo modal after Save | Dismiss with **I'll share later** |
| Duplicate group name | Use runtime-unique name in test data |
| Login required | Reuse `user_ensures_logged_in_home` after P0-01 in same session |
| `Fee Collection Start Date` pre-filled | Leave default unless test requires change |

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
