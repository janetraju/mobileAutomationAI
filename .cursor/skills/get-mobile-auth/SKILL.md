---
name: get-mobile-auth
description: >-
  Selects and documents the mobile test credential/OTP strategy for an
  app — fixed OTP, manual, or bypass — and wires TEST_MOBILE, TEST_OTP,
  and auth_profile/session-reuse settings into .env per AGENTS.md's
  credential policy. Use when configuring login/OTP test data for a new
  app or feature, before dataproviders or login automation are written.
---

# Get Mobile Auth

Decide and record how login/OTP will be handled in tests, and wire the
resulting settings into `.env`. This skill produces **configuration and
documentation only** — it does not author the login Page Object, Actions, or
Steps files; that belongs to `mobile-test-automation`.

Repository conventions (credential storage rules, `.env` policy, fail-fast
behavior) are defined in `AGENTS.md` → *Test data & credentials*. This skill
implements that policy for one app; it does not redefine it.

## When to Use

Use this skill when:

- Onboarding a new app (after `create-mobile-framework-structure`) that has a
  login/OTP gate
- A feature requires authenticated test data and no strategy is set yet
- The existing OTP strategy for an app needs to change (e.g. dev bypass →
  fixed OTP for a new environment)

## Output

- One OTP strategy chosen and recorded per app:

  | Strategy | Implementation |
  |----------|-----------------|
  | Fixed OTP in dev | `TEST_OTP` set in `.env` / `.env.dev` |
  | Manual | Tests marked `@pytest.mark.manual_otp` (avoid in CI) |
  | Bypass | Deep link or `auth_profile` + `NO_RESET` session reuse |

- `.env` / `.env.<env>` updated with `TEST_MOBILE`, `TEST_OTP`,
  `DEFAULT_USERNAME`, `DEFAULT_PASSWORD` as applicable — **never committed**
- `docs/<app_slug>-flow.md` → *Known blockers / Test data* section updated
  with the chosen strategy and rationale
- No production credentials — dev/stg/uat only

Commit the flow-doc update; never commit `.env` or any file containing actual
secrets.

---

# Workflow

## Step 1 — Confirm Prerequisites

Confirm the app is already registered (`create-mobile-framework-structure`
has run). If not, stop and hand off there first.

## Step 2 — Choose the OTP Strategy

Ask the user which strategy applies for this app/environment:

- Fixed OTP in dev
- Manual
- Bypass (deep link / `auth_profile` + `NO_RESET`)

Only one strategy per app per environment — don't mix without documenting why
in the flow doc.

## Step 3 — Wire `.env`

Set the variables required by the chosen strategy (see Output table) in
`.env` / `.env.<env>`. Confirm:

- No secrets are hardcoded anywhere outside `.env`
- No production credentials are used
- `TEST_MOBILE` is present whenever login tests will be collected — tests
  must fail fast if it's missing, per `AGENTS.md`

## Step 4 — Document the Choice

Update `docs/<app_slug>-flow.md` → *Known blockers / Test data* with:

- The strategy chosen and why
- Any manual steps required in CI or locally
- Which environments (dev/stg/uat) it applies to

## Step 5 — Hand Off

Once the strategy is documented and `.env` is wired, hand off to
`mobile-test-automation` to author the actual login Page Object, Actions, and
Steps files that consume these settings.
