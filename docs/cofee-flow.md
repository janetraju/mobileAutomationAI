# CoFee — Flow index

Flutter Android · `cofee.life.app.dev` · API `https://api.dev.cofee.life`

This file is the **coverage dashboard** only. Feature detail and approved cases live
under [`docs/context/`](context/README.md). Do not duplicate long TC text here.

**OTP strategy (dev):** fixed OTP via `TEST_OTP` in `.env` (never commit).

## Coverage status

| ID | Flow | Status | Context | Testcases | Tests |
|----|------|--------|---------|-----------|-------|
| P0-01/02 | Login + home | **Done** | [context](context/cofee-login-context.md) | [testcases](context/cofee-login-testcases.md) | `tests/test/cofee/login/` |
| P0-03 | Create group (monthly last day) | **Done** | [context](context/cofee-create-group-context.md) | [testcases](context/cofee-create-group-testcases.md) | `test_create_group_with_manual_member` |
| P0-04 | Create group (weekly Mon) | **Done** | same | same | `test_create_group_with_weekly_fee_collection` |
| P1-01…03 | Contacts / installments / 2 members | Not started | — | — | — |
| P0-05 | Enable partial payment (HP-01, HP-04, NEG-01) | **Done** | [context](context/cofee-enable-partial-payment-context.md) | [testcases](context/cofee-enable-partial-payment-testcases.md) | `test_enable_partial_payment.py` |
| P0-06 | Dues View All → Pending search | **Done** | [context](context/cofee-dues-search-context.md) | [testcases](context/cofee-dues-search-testcases.md) | `test_dues_search.py` |
| P1-04 | Home Groups View All → My active groups | **Done** | [context](context/cofee-home-explore-context.md) | [testcases](context/cofee-home-explore-testcases.md) | `test_home_explore.py` |

## Known blockers / test data

| Topic | Note |
|-------|------|
| Dues search | Uses pre-seeded member on shared Individual account — fragile across env resets / parallel workers |
| Partial payment | Threshold ₹2000 inclusive; create fresh group/payment per case |
| Secrets | Never store phone/OTP in context docs |

## New feature rule

1. `get-context` → `docs/context/<slug>-context.md`  
2. `testcase-generator` → approve `*-testcases.md`  
3. `discover-mobile-locators` → confirm locators live  
4. `testscript-generator` → implement  
5. Update **this** index row to Done + links  
