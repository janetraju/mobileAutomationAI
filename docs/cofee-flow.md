# CoFee — Flow doc

Flutter Android · `cofee.life.app.dev` · API `https://api.dev.cofee.life`  
Detail TCs: `docs/context/` when present.

## Status

| ID | Flow | Status |
|----|------|--------|
| P0-01/02 | Login + home | **Done** — `tests/test/cofee/login/` |
| P0-03 | Create group (monthly last day) | **Done** — `test_create_group_with_manual_member` |
| P0-04 | Create group (weekly Mon) | **Done** — `test_create_group_with_weekly_fee_collection` |
| P1-01…03 | Contacts / installments / 2 members | Not started |
| P0-05 | Enable partial payment (HP-01, HP-04, NEG-01) | **Done** — `tests/test/cofee/payments/test_enable_partial_payment.py` |

## Flows

**Login:** fresh install → phone → OTP → account picker → Home  

**Create group** (logged-in Individual): Add New → Manually → add member → name + amount → Fee Collection Day → schedule → Save (left tap) → I'll share later → assert group detail  

| Variant | Schedule |
|---------|----------|
| P0-03 | Last day of the month |
| P0-04 | Weekly → Mon (`Weekly: Monday`) |

**Enable partial payment** (logged in; pending payment ≥ ₹2,000): open payment card (member history / Group payments / All payments) → ⋮ → **Enable Partial Payment** → **Confirm** → card shows `0%,` prefix; menu no longer offers Enable Partial Payment  

| Case | What |
|------|------|
| HP-01 | Enable on eligible card |
| HP-04 | Option available from all three entry points |
| NEG-01 | Option hidden when amount &lt; ₹2,000 |

Detail TCs: `docs/context/cofee-enable-partial-payment-testcases.md`
