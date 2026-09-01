# Context: Home explore (`cofee-home-explore`)

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
| Feature slug | home-explore |
| Platforms | android (Flutter) |
| Account type | Individual (logged in) |

## Screens in scope

| Screen | Purpose |
|--------|---------|
| Home | Groups section with View All |
| My active groups | List of active groups |

## Happy path

1. Ensure logged-in home  
2. Tap Groups section **View All**  
3. Assert **My active groups** list visible  

## Business rules

- Smoke / exploratory navigation from home dashboard  

## Edge cases / unknowns

- Empty groups list behavior — Unknown / not automated  

## Test data needs (no secrets)

| Need | How supplied |
|------|----------------|
| Logged-in user | `authenticated` + `.env` |

## Known product quirks

- None beyond general Flutter idle/wait behavior  

## Existing automation

| Layer | Path |
|-------|------|
| Tests | `tests/test/cofee/home/test_home_explore.py` |
| Steps | `src/steps/cofee/home_steps.py` |

## Open questions

- Broader home widgets still exploratory  

## Handoff

Testcases: `docs/context/cofee-home-explore-testcases.md`
