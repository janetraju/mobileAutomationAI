# Context: Enable partial payment (`cofee-enable-partial-payment`)

## Freshness

| Field | Value |
|-------|-------|
| Last updated | 2026-08-12 |
| Env checked | dev |
| Confirmed on device | yes (threshold confirmed live 2026-07-16) |
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
| Feature slug | enable-partial-payment |
| Platforms | android (Flutter) |
| Account type | Individual (logged in) |

## Screens in scope

| Screen | Purpose |
|--------|---------|
| Group / payment setup | Create group + payment request for isolation |
| Member payment history | Entry: per-member card kebab |
| Group payments (Monthly Insights) | Entry: group payments list |
| All payments | Entry: global payments tab |
| Enable Partial Payment confirm | Confirm action |

## Happy path

1. Ensure logged-in home  
2. Create fresh group + pending payment request (eligible amount)  
3. Open payment card via entry point → ⋮ → **Enable Partial Payment** → Confirm  
4. Card shows partial state (`0%,` prefix); Enable option gone from menu  

## Business rules

- **Threshold:** `splitRequiredAmountMin = 2000` (₹), inclusive (`>=`)  
  - Amount **&lt; 2000** → option **hidden**  
  - Amount **≥ 2000** → option **shown**  
- Entry points for same eligible payment: member history, Group payments, All payments  

## Edge cases / unknowns

- Mark As Paid flows (HP-02/HP-03) — not yet automated  
- STATE/REG cases — see testcases open items  

## Test data needs (no secrets)

| Need | How supplied |
|------|----------------|
| Logged-in user | `authenticated` + `.env` |
| Fresh group/member/note | Runtime unique suffix in dataprovider |
| Amounts | Relative to threshold 2000 |

## Known product quirks

- Prefer creating fresh payment data per case (parallel-safe)  
- Flutter amount fields may need careful typing  

## Existing automation

| Layer | Path |
|-------|------|
| Tests | `tests/test/cofee/payments/test_enable_partial_payment.py` |
| Steps | `src/steps/cofee/payment_steps.py` |
| Dataprovider | `tests/dataprovider/dp_enable_partial_payment.py` |

## Open questions

- HP-02/HP-03 Mark As Paid still open  

## Handoff

Testcases: `docs/context/cofee-enable-partial-payment-testcases.md`
