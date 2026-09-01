# Test Cases: Create group (`cofee-create-group`)

Source: `docs/context/cofee-create-group-context.md`  
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

### TC-create-group-HP-01: Create group with manual member (monthly last day)

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-02 |
| Automation status | Done |
| Test path | `tests/test/cofee/groups/test_create_group.py::TestCreateGroup::test_create_group_with_manual_member` |
| Flow ID | P0-03 |

**Steps:**
1. From home, create group with one manual member  
2. Set monthly last-day fee schedule  
3. Save and dismiss share  

**Expected Result:** Group detail shows expected name / fee  

### TC-create-group-HP-02: Create group with weekly Monday fee

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-02 |
| Automation status | Done |
| Test path | `tests/test/cofee/groups/test_create_group.py::TestCreateGroup::test_create_group_with_weekly_fee_collection` |
| Flow ID | P0-04 |

**Steps:**
1. Same as HP-01 with Weekly → Monday schedule  

**Expected Result:** Group detail shows weekly Monday fee schedule  

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-create-group-HP-01 | Happy Path | P0 | Done |
| TC-create-group-HP-02 | Happy Path | P0 | Done |

## Parametrization candidates

- Member/group/amount from `dp_create_group.py`  

## Open questions

- P1-01…03 (contacts / installments / 2 members) not started  

## Handoff

Extend via `testcase-generator` when P1 flows are prioritized.
