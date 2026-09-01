# Test Cases: Home explore (`cofee-home-explore`)

Source: `docs/context/cofee-home-explore-context.md`  
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

## Happy Path (HP)

### TC-home-explore-HP-01: Groups View All opens My active groups

| Field | Value |
|-------|-------|
| Priority | P1 |
| Preconditions | PRE-02 |
| Automation status | Done |
| Test path | `tests/test/cofee/home/test_home_explore.py::TestHomeExplore::test_open_groups_list_via_home_view_all` |
| Flow ID | P1-04 |

**Steps:**
1. From home, tap Groups View All  
2. Assert My active groups list  

**Expected Result:** My active groups screen/list is visible  

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-home-explore-HP-01 | Happy Path | P1 | Done |

## Open questions

- Additional home CTAs  

## Handoff

Stable P1 smoke; expand with `testcase-generator` as needed.
