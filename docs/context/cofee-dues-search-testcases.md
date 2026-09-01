# Test Cases: Dues search (`cofee-dues-search`)

Source: `docs/context/cofee-dues-search-context.md`  
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
| PRE-02 | Logged in on home (`@pytest.mark.authenticated`) |
| PRE-04 | Pending due exists for seeded member on account |

## Happy Path (HP)

### TC-dues-search-HP-01: Search pending due from Dues View All

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-02, PRE-04 |
| Automation status | Done |
| Test path | `tests/test/cofee/payments/test_dues_search.py::TestDuesSearch::test_search_pending_due_from_dues_view_all` |
| Flow ID | P0-06 |

**Steps:**
1. Open Pending via home Dues View All  
2. Search for configured member query  
3. Assert expected card name listed  

**Expected Result:** Matching pending due card visible  

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-dues-search-HP-01 | Happy Path | P0 | Done |

## Parametrization candidates

- `dp_dues_search.py` query / expected name  

## Open questions

- Seed via API instead of shared `user1`  

## Handoff

Keep P0 green; prioritize data isolation in a later iteration.
