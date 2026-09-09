# CoFee — Flow index

Android · Flutter · `cofee.life.app.dev` · `cofee.life.app.MainActivity`

Fixed fee group creation is confirmed live and automated (P0-01 below). Everything else in
the `group-fee-attendance` feature (Attendance based fee, attendance marking, edit group,
member deactivate/delete) remains **unconfirmed** — see Known blockers.

This file is the **coverage dashboard** only. Feature detail and approved cases live under
[`docs/context/`](context/). Do not duplicate long TC text here.

**OTP strategy (dev):** fixed OTP via `TEST_MOBILE` / `TEST_OTP` in `.env.dev` (never commit).

## Flows

**Create group — Fixed fee.** Confirmed live flow differs from the Figma the context doc was
based on: `Add New` → **Select members** (From Contacts / Manually) *first* → `Add member`
(Name + Mobile) → `Create group` form (Fixed fee only — no fee-type picker exists in this
build) → fill Group name / Amount / per-member Amount / Fee Collection Day → `Save` → lands
on the new group's detail screen (occasionally via a "Get paid faster with CoFee!" share
interstitial first, backend-latency dependent, not deterministic).

## Coverage status

| ID | Flow | Status | Context | Testcases | Tests |
|----|------|--------|---------|-----------|-------|
| P0-01 | Create group — Fixed fee, happy path | **Done** — `tests/test/cofee/create_group/test_create_group.py::test_create_fixed_fee_group` | [context](context/cofee-group-fee-attendance-context.md) | [testcases](context/cofee-group-fee-attendance-testcases.md) (`group-fee-attendance-P0-01`) | `test_create_fixed_fee_group` |
| P0-02 | Attendance based fee, attendance marking, edit group, member deactivate/delete | Blocked — see Known blockers | [context](context/cofee-group-fee-attendance-context.md) | [testcases](context/cofee-group-fee-attendance-testcases.md) | — |

## Known blockers / test data

| Topic | Note |
|-------|------|
| Mobile + OTP login | Strategy: **Fixed OTP in dev**. `TEST_MOBILE` / `TEST_OTP` set in `.env.dev` (gitignored, never committed — see `.env.dev.example` for the variable names, not the values). Applies to **dev only** — stg/uat have no strategy set yet, tests requiring OTP login will fail fast (`TEST_MOBILE` missing) if collected against those envs. |
| Other login methods | Not confirmed. No login screen was included in the Figma set used for `get-mobile-context`, and only mobile+OTP credentials were provided — email/password and SSO (Google, etc.) support is unknown for this app. Revisit `get-mobile-auth` if another method turns out to exist. |
| Attendance based fee not in this build | Live-confirmed 2026-09-07 against `builds/cofee-dev.apk` (versionCode 116): "Add New" → Select members → Fixed-fee-only Create group form. No fee-type picker, no Attendance based fee, no "Enable attendance" toggle, on either create or an existing group's Edit Group screen. See `cofee-group-fee-attendance-context.md` → Known product quirks for full detail. P0-02/03/04/06, P1-01..08, P2-01/02 in the approved testcases file target functionality that does not exist yet — do not implement against this build. |
| Group name character limit | "Character limit exceeded" validation fires somewhere between 30–32 characters — confirmed live, exact cutoff not pinned down. Keep generated group names short (`dp_create_group.py` uses `"QA Auto " + 8 hex chars`, 16 chars). |
| Per-member amount field required (Fixed fee) | The member row in Create/Edit Group has its own ₹ amount field, separate from the top-level "Amount" field — leaving it blank makes Save silently no-op (stays on the same form, no error shown). Both must be filled. |
| Flutter text fields need an explicit tap to focus | `send_keys()` alone silently no-ops on this app's text fields (Flutter semantics-based `EditText`s) — always `.click()` before `clear()`/`send_keys()`. Fixed in `PageActions.type_text()` (`src/core/base_actions.py`) so every layer gets this for free; do not bypass it with raw `element.send_keys()`. |
| `NO_RESET` resumes the last screen, not Home | A fresh Appium session with only `noReset` re-attaches to whatever screen the app process was last on (not a cold launch to Home). `appium:forceAppLaunch` + `appium:shouldTerminateApp` (set in `src/core/driver_factory.py`) force a clean relaunch each session while still keeping the login session (local storage survives). |
| Save latency is variable | Group creation's backend round-trip has been observed anywhere from ~4s to 20s+. Don't tighten `assert_group_created`'s wait in `create_group_steps.py` without re-confirming live. |
| "Overview" semantics can merge with a promo banner | On some Home states the accessibility id for the Overview card merges with an adjacent "Instant payment links..." banner into one combined content-desc, breaking an exact match on `"Overview"`. `"Add New"` is the stable, always-standalone locator used instead (`home_po.py`, `login_po.py`). |
| Member row is inside a virtualized list | The per-member amount field isn't always attached to the accessibility tree even with a single member — confirmed live as an intermittent `NoSuchElementException`. `CreateGroupActions.enter_member_amount()` scrolls it into view first (`PageActions.scroll_until_visible`) rather than finding it directly. |

## New feature rule

1. `get-mobile-context` → `docs/context/cofee-<feature>-context.md`
2. `get-mobile-auth` (only if credentials/OTP strategy isn't set yet)
3. `mobile-test-design` → approve `docs/context/cofee-<feature>-testcases.md`
4. `mobile-test-automation` → confirm locators live, implement
5. Update **this** index row to Done + links
