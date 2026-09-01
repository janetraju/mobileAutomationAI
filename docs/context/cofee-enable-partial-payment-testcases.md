# Test Cases: Enable partial payment (`cofee-enable-partial-payment`)

Source: `docs/context/cofee-enable-partial-payment-context.md`  
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
| PRE-03 | Fresh group + pending payment created in-test |

## Happy Path (HP)

### TC-enable-partial-payment-HP-01: Enable on eligible payment

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-02, PRE-03 |
| Automation status | Done |
| Test path | `tests/test/cofee/payments/test_enable_partial_payment.py::TestEnablePartialPayment::test_enable_partial_payment_on_eligible_payment` |
| Flow ID | P0-05 |

**Steps:**
1. Set up group with eligible payment request  
2. Open kebab from member history  
3. Enable Partial Payment and confirm  

**Expected Result:** Partial state visible; Enable option no longer offered  

### TC-enable-partial-payment-HP-04: Option available from all entry points

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-02, PRE-03 |
| Automation status | Done |
| Test path | `…::test_partial_payment_option_available_from_all_entry_points` |
| Flow ID | P0-05 |

**Steps:**
1. Create eligible payment  
2. Open kebab from member history / group payments / all payments  

**Expected Result:** Enable Partial Payment option present at each entry point  

## Negative / Validation (NEG)

### TC-enable-partial-payment-NEG-01: Threshold boundary

| Field | Value |
|-------|-------|
| Priority | P0 |
| Preconditions | PRE-02, PRE-03 |
| Automation status | Done |
| Test path | `…::test_partial_payment_option_visibility_at_threshold` |
| Flow ID | P0-05 |

**Steps:**
1. Create payment with amount 1999 → assert option absent  
2. Create payment with amount 2000 → assert option present  

**Expected Result:** Inclusive threshold at ₹2000  

## Not yet automated

| TC ID | Notes |
|-------|-------|
| HP-02 / HP-03 | Mark As Paid |
| STATE / REG | See prior product notes when revived |

## Coverage matrix

| TC ID | Category | Priority | Automation status |
|-------|----------|----------|--------------------|
| TC-enable-partial-payment-HP-01 | Happy Path | P0 | Done |
| TC-enable-partial-payment-HP-04 | Happy Path | P0 | Done |
| TC-enable-partial-payment-NEG-01 | Negative | P0 | Done |

## Parametrization candidates

- Threshold rows + entry points in `dp_enable_partial_payment.py`  

## Open questions

- Mark As Paid prioritization  

## Handoff

Extend with `testcase-generator` when HP-02/03 are approved for automation.
