---
name: setup-mobile-test-data
description: >-
  Set up mobile test data via API, OTP helpers, and encrypted fixtures.
  Use when tests need login credentials, OTP injection, backend seeding,
  org/account setup, or API assertions before or during UI flows.
disable-model-invocation: true
---

# Setup Mobile Test Data

## When to use

- Before login / onboarding E2E tests
- User provides test phone, OTP strategy, or API credentials
- Tests need pre-seeded org, account, or feature flags
- Backend state must be verified alongside UI

## Read first

1. **`AGENTS.md`**
2. **`.env` / `.env.<env>`** — credentials live here only
3. **`src/core/api_client.py`**
4. **`data/<app_slug>/`** — structured non-secret fixtures

## Config variables

| Variable | Purpose |
|----------|---------|
| `API_BASE_URL` | From `APP_REGISTRY` or explicit override |
| `API_AUTH_TOKEN` | Bearer token for admin/test APIs (`.env` only) |
| `TEST_MOBILE` | Default phone for login tests |
| `DEFAULT_USERNAME` / `DEFAULT_PASSWORD` | Non-phone auth if applicable |
| `OTP_GENERATE_PATH` | Default `/auth/generate-otp` |
| `OTP_VALIDATE_PATH` | Default `/auth/validate-otp` |
| `FEATURE_ORG_ID` / `FEATURE_ACCOUNT_ID` | Shared suite setup |

## OTP strategies

Document the active strategy in `docs/<app_slug>-flow.md` → Known blockers / Test data.

| Strategy | Implementation |
|----------|----------------|
| **Fixed OTP in dev** | Set `TEST_OTP` in `.env.dev` (never commit) |
| **API inject** | `generate_otp()` then read from test mail/SMS hook or debug endpoint |
| **Manual** | Mark test `@pytest.mark.manual_otp` or pause — avoid in CI |
| **Bypass** | Deep link / `auth_profile` + `no_reset` session reuse |

```python
from src.core.api_client import generate_otp, validate_otp, ApiClient

# Example — paths from settings
generate_otp("+919876543210")
```

## Data layout

```
data/<app_slug>/
  users.example.json      # structure only, committed
  users.json              # gitignored if contains real data
  org_setup.example.json
```

Encrypt at rest if secrets must live in repo; decrypt via env key (document in README).

## Dataprovider rules

- `tests/dataprovider/dp_*.py` returns `list[pytest.param(..., id="...")]`
- Reference **env vars** or `data/<app_slug>/` — never hardcode passwords
- Time-relative values computed in tests, not at collection

## DB checks (optional)

If `DB_HOST` is set, use `psycopg` in test setup/teardown — keep SQL in `data/<app_slug>/` scripts, not in page layers.

## Hand off

After data strategy is documented and `.env.<env>` is configured →
**`automate-a-flow`** (orchestration) → **`mobile-appium-python`** (layer code).

## Rules

- No secrets in dataproviders, POs, steps, or committed JSON
- No production credentials — dev/stg/uat only
- Fail fast if `TEST_MOBILE` missing when login tests are collected
