# Context: Dues search (`cofee-dues-search`)

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
| Feature slug | dues-search |
| Platforms | android (Flutter) |
| Account type | Individual (logged in) |

## Screens in scope

| Screen | Purpose |
|--------|---------|
| Home | Dues section View All |
| All payments — Pending | List pending dues |
| Search | Filter by member query |

## Happy path

1. Ensure logged-in home  
2. Home → Dues **View All**  
3. Pending dues listed  
4. Search icon → type member query → assert matching card  

## Business rules

- Requires **pre-seeded** pending due for the searched member on the shared Individual account  
- Current automated query assumes member display tied to search `user1` → `User1` (env-coupled; improve with API seed later)  

## Edge cases / unknowns

- Empty search / no matches — not automated  
- Parallel workers may collide on shared seeded data  

## Test data needs (no secrets)

| Need | How supplied |
|------|----------------|
| Logged-in user | `authenticated` + `.env` |
| Seeded member due | Shared account state (fragile) — document in flow index |

## Known product quirks

- Relies on backend state; env reset breaks the case  

## Existing automation

| Layer | Path |
|-------|------|
| Tests | `tests/test/cofee/payments/test_dues_search.py` |
| Steps | `src/steps/cofee/payment_steps.py` |
| Dataprovider | `tests/dataprovider/dp_dues_search.py` |

## Open questions

- Replace seeded `user1` with API-created due for isolation  

## Handoff

Testcases: `docs/context/cofee-dues-search-testcases.md`
