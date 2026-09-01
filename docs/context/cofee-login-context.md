# Context: Login (`cofee-login`)

## Freshness

| Field | Value |
|-------|-------|
| Last updated | 2026-08-12 |
| Env checked | dev |
| Confirmed on device | yes |
| Owner | mobile-automation |

## Source links (optional — fill when available)

| Source | Link / key | Status |
|--------|------------|--------|
| Jira | | Not available |
| PRD | | Not available |
| Figma | | Not available |
| App source / walkthrough | Live device + existing automation | Available |

## Feature

| Field | Value |
|-------|-------|
| App slug | cofee |
| Feature slug | login |
| Platforms | android (Flutter) |
| Account type | Individual (dev OTP) |

## Screens in scope

| Screen | Purpose |
|--------|---------|
| Onboarding / permissions | Notification permission dismiss |
| Phone entry | Enter mobile, request OTP |
| OTP entry | Enter OTP |
| Account picker | Select account when shown |
| Home | Logged-in dashboard |

## Happy path

1. Fresh install (`pm clear`) and launch app  
2. Dismiss notification permission if shown  
3. Reach phone entry → enter `TEST_MOBILE` → Next  
4. Enter `TEST_OTP` → complete account picker if shown  
5. Land on Home  

## Business rules

- Dev uses fixed OTP from `.env` (`TEST_OTP`) — never commit the value  
- Login automation uses `@pytest.mark.fresh` (owns clean app)  
- Feature tests use `@pytest.mark.authenticated` (fixture ensures home)  

## Edge cases / unknowns

- Account picker may or may not appear depending on account state  
- Flutter digit fields may need adb text input (product quirk)  

## Test data needs (no secrets)

| Need | How supplied |
|------|----------------|
| Phone | `TEST_MOBILE` in `.env` |
| OTP | `TEST_OTP` in `.env` |

## Known product quirks

- After `pm clear`, relaunch with `am start` / `activate_app`  
- Debug overlay may need dismiss on some builds  

## Existing automation

| Layer | Path |
|-------|------|
| Tests | `tests/test/cofee/login/test_login.py` |
| Steps | `src/steps/cofee/login_steps.py` |
| Actions / POs | `src/page_actions/cofee/login_actions.py`, `src/page_objects/cofee/login_po.py` |

## Open questions

- iOS login path not automated yet  

## Handoff

Testcases: `docs/context/cofee-login-testcases.md`
