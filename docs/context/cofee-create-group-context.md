# Context: Create group (`cofee-create-group`)

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
| Feature slug | create-group |
| Platforms | android (Flutter) |
| Account type | Individual (logged in) |

## Screens in scope

| Screen | Purpose |
|--------|---------|
| Home | Start Add New |
| Add member manually | Create member |
| Group name + fee amount | Core group fields |
| Fee collection schedule | Monthly last day or Weekly Monday |
| Share later / group detail | Confirm creation |

## Happy path

1. Ensure logged-in home (`authenticated`)  
2. Add New → Manually → add member  
3. Set group name + amount  
4. Choose fee collection schedule  
5. Save (left-biased tap to avoid debug FAB) → I'll share later  
6. Assert group detail  

## Business rules

| Variant | Schedule |
|---------|----------|
| Monthly | Last day of the month |
| Weekly | Weekly → Mon (`Weekly: Monday`) |

- Member mobile/name must be unique per run for parallel safety  

## Edge cases / unknowns

- Contacts picker / installments / multi-member → Not started (see flow index)  

## Test data needs (no secrets)

| Need | How supplied |
|------|----------------|
| Logged-in user | `TEST_MOBILE` / `TEST_OTP` via `authenticated` fixture |
| Member / group names | Runtime unique suffix in dataprovider |

## Known product quirks

- Save CTA: prefer **left-biased** tap (debug FAB overlap)  
- Some Flutter controls may need coordinate / adb taps  

## Existing automation

| Layer | Path |
|-------|------|
| Tests | `tests/test/cofee/groups/test_create_group.py` |
| Steps | `src/steps/cofee/group_steps.py` |
| Dataprovider | `tests/dataprovider/dp_create_group.py` |

## Open questions

- P1 contacts / installments / 2 members still open  

## Handoff

Testcases: `docs/context/cofee-create-group-testcases.md`
