# Setup Mobile Test Data

Configure OTP, API credentials, and fixtures so login and downstream E2E tests can run.

Secrets and dataprovider rules live in **AGENTS.md** — this skill covers only the setup workflow.

## When to Use

Use this skill when:

- Preparing login or onboarding E2E tests
- The user provides test phone, OTP strategy, or API credentials
- Tests need pre-seeded org, account, or feature flags
- Backend state must be verified alongside UI

## Workflow

### Step 1 — Review Configuration

Read:

**Required**

- `AGENTS.md` (Secrets & config)
- `.env` / `.env.<env>`
- `src/core/api_client.py`
- `data/<app_slug>/`

Key variables: `API_BASE_URL`, `API_AUTH_TOKEN`, `TEST_MOBILE`, `OTP_GENERATE_PATH`, `OTP_VALIDATE_PATH`, `FEATURE_ORG_ID`, `FEATURE_ACCOUNT_ID`.

### Step 2 — Choose OTP Strategy

Document the active strategy in `docs/<app_slug>-flow.md` → Test data / Known blockers.

| Strategy | Implementation |
| -------- | -------------- |
| Fixed OTP (dev) | `TEST_OTP` in `.env.dev` — never commit |
| API inject | `generate_otp()` + test mail/SMS hook or debug endpoint |
| Manual | `@pytest.mark.manual_otp` — avoid in CI |
| Bypass | Deep link / `auth_profile` + `no_reset` session reuse |

```python
from src.core.api_client import generate_otp, validate_otp, ApiClient

generate_otp("+919876543210")  # paths from settings
```

### Step 3 — Layout Fixtures

```
data/<app_slug>/
  users.example.json      # structure only, committed
  users.json              # gitignored if real data
  org_setup.example.json
```

Dataproviders reference env vars or `data/<app_slug>/` — never hardcode passwords.

Optional: DB checks via `psycopg` — keep SQL in `data/<app_slug>/` scripts, not in page layers.

### Step 4 — Verify Readiness

Confirm:

- `TEST_MOBILE` is set when login tests will be collected
- Whitelisted phone on dev API (if OTP flow requires it)
- Strategy documented in flow doc

### Step 5 — Hand Off

```text
setup-mobile-test-data → automate-a-flow → mobile-appium-python
```

## Rules

- No secrets in dataproviders, POs, steps, or committed JSON.
- Dev/stg/uat credentials only — never production.
- Fail fast if `TEST_MOBILE` is missing when login tests are collected.
- Time-relative values computed in tests, not at collection.

## Related Skills

- `get-context`
- `automate-a-flow`
- `mobile-appium-python`
