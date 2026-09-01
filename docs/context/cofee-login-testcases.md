# Test Cases: Login (`cofee-login`)

Source: `docs/context/cofee-login-context.md`  
Approved: **yes** — 2026-08-12 (backfill from existing automation)

## Freshness

| Field | Value |
|-------|-------|
| Last updated | 2026-08-12 |
| Env checked | dev |
| Confirmed on device | yes |
| Owner | mobile-automation |

## Preconditions (shared)

| ID | Description |
|----|-------------|
| PRE-01 | Fresh install, no active session (`@pytest.mark.fresh`) |
| PRE-02 | Logged in on home (`@pytest.mark.authenticated`) |

## Happy Path (HP)

### TC-login-HP-01: Phone + OTP login success

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-01 |
| Automation status | Done |
| Test path | `tests/test/cofee/login/test_login.py::TestLogin::test_phone_otp_login_success` |
| Flow ID | P0-01/02 |

**Steps:**
1. Clear app data and relaunch  
2. Reach phone login screen  
3. Enter phone from `TEST_MOBILE` and request OTP  
4. Enter OTP from `TEST_OTP` and complete account picker if shown  

**Expected Result:** Home dashboard is visible  

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-login-HP-01 | Happy Path | P0 | Done |

## Parametrization candidates

- Phone/OTP from `dataprovider/dp_login.py` (env-backed)

## Locator map (live-confirmed only)

Confirm via `discover-mobile-locators` / existing `login_po.py` — do not invent.

## Open questions

- Negative OTP / wrong phone cases not yet automated  

## Handoff

Stable for regression; extend NEG cases via `testcase-generator` when product prioritizes.
