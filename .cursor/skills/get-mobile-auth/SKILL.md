---
name: get-mobile-auth
description: >-
  Selects and documents the mobile test credential strategy for an app —
  across mobile number + OTP, email + password, Google/Gmail sign-in, and
  other SSO providers — and wires the resulting settings into .env (or
  the device's pre-authorized account, for SSO) per AGENTS.md's
  credential policy. Use when configuring login test data for a new app
  or feature, before dataproviders or login automation are written.
---

# Get Mobile Auth

Decide and record how login will be handled in tests — for **every** login
method the app actually supports — and wire the resulting settings into
`.env` (or a pre-authorized device account, for SSO). This skill produces
**configuration and documentation only** — it does not author the login
Page Object, Actions, or Steps files; that belongs to `mobile-test-automation`.

Repository conventions (credential storage rules, `.env` policy, fail-fast
behavior) are defined in `AGENTS.md` → *Test data & credentials*. This skill
implements that policy for one app; it does not redefine it.

## When to Use

Use this skill when:

- Onboarding a new app (after `create-mobile-framework-structure`) that has
  any login gate
- A feature requires authenticated test data and no strategy is set yet for
  the login method it uses
- The app adds a login method that isn't documented yet (e.g. Google
  sign-in added alongside existing mobile-OTP login)
- An existing strategy needs to change (e.g. dev bypass → fixed OTP for a
  new environment)

## Supported Auth Methods

An app may support more than one of these — set a strategy for **each** one
it actually has, not just the first one found.

| Method | Strategy options | Where it's stored |
|--------|-------------------|---------------------|
| Mobile number + OTP | Fixed OTP in dev / Manual / Bypass | `.env`: `TEST_MOBILE`, `TEST_OTP` |
| Email + password | Dedicated non-prod test account | `.env`: `DEFAULT_USERNAME`, `DEFAULT_PASSWORD` |
| Google / Gmail sign-in | Pre-authorized device account (preferred) / Bypass via deep link or `auth_profile` / Manual (avoid in CI) | Device-level test account (not `.env` — never store a real Google password in the repo) |
| Other SSO (Facebook, Apple, corporate SSO, etc.) | Same preference order as Google — pre-authorized device/session first | Document per provider in the flow doc |

**Why SSO is different:** automating a third-party provider's real
consent/login UI (Google, Facebook, Apple) is fragile, frequently trips
bot/anti-automation detection, and can violate that provider's terms of
service. Default to a device or emulator that already has a test account
signed in (or a `NO_RESET` session profile) rather than driving the
provider's login screen. Only fall back to driving that UI, marked
`@pytest.mark.manual_otp`-style manual/skip-in-CI, when no pre-authorized
option is possible.

## Output

- One strategy chosen and recorded **per supported method** (see table above)
- `.env` / `.env.<env>` updated with the variables for OTP and
  email/password methods, as applicable — **never committed**
- For SSO methods: the device/emulator or CI image note describing which
  pre-authorized test account is used, and by which build/profile
- `docs/<app_slug>-flow.md` → *Known blockers / Test data* section updated
  with, for every method: the strategy chosen, why, and any manual/CI
  caveats
- No production credentials or real personal accounts — dev/stg/uat test
  accounts only

Commit the flow-doc update; never commit `.env`, passwords, or any file
containing actual secrets.

---

# Workflow

## Step 1 — Confirm Prerequisites

Confirm the app is already registered (`create-mobile-framework-structure`
has run). If not, stop and hand off there first.

## Step 2 — Identify Every Login Method the App Has

Ask the user (or confirm via `get-mobile-context` / live device) which of
these the app actually supports — it can be more than one:

- Mobile number + OTP
- Email + password
- Google / Gmail sign-in
- Other SSO (name the provider)

Don't assume a single method — many apps offer OTP login *and* Google
sign-in side by side, and each needs its own strategy.

## Step 3 — Choose a Strategy Per Method

For each method identified in Step 2, pick from the options in Supported
Auth Methods above. Only one strategy per method per environment — don't mix
without documenting why in the flow doc.

## Step 4 — Wire Credentials

- OTP / email-password: set the relevant variables (see Output) in `.env` /
  `.env.<env>`
- SSO: confirm a pre-authorized test account exists on the target
  device/emulator/CI image; do not create `.env` entries containing real
  provider passwords

Confirm across all methods:

- No secrets are hardcoded anywhere outside `.env`
- No production credentials or personal accounts are used
- `TEST_MOBILE` is present whenever OTP login tests will be collected —
  tests must fail fast if it's missing, per `AGENTS.md`

## Step 5 — Document Every Method

Update `docs/<app_slug>-flow.md` → *Known blockers / Test data* with one
entry per supported method:

- The strategy chosen and why
- Any manual steps required in CI or locally
- Which environments (dev/stg/uat) it applies to

## Step 6 — Hand Off

Once every method's strategy is documented and credentials/accounts are
wired, hand off to `mobile-test-automation` to author the actual login Page
Object(s), Actions, and Steps files — one flow per method — that consume
these settings.
