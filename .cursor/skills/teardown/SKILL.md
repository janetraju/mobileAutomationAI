---
name: teardown
description: >-
  Resets device/session/app state after a run so the next run starts clean
  - respecting whichever OTP/credential strategy get-mobile-auth chose, so
  it never undoes an intentional session-reuse (bypass) setup. Use after
  mobile-test-report has triaged a run, or any time a device/emulator is
  left in a state that would make the next run unreliable. Non-coders:
  nothing to do here, this runs on its own.
---

# Teardown

Reset device, Appium session, and app state after a test run, so the next
run starts from a known-clean baseline instead of inheriting leftover state
from the last one.

Repository conventions (credential strategy, `NO_RESET` policy) are defined
in `AGENTS.md` → *Test data & credentials*. This skill implements that
policy at run-boundary time; it does not choose or change the strategy —
that's `get-mobile-auth`'s job.

## When to Use

Use this skill:

- After `mobile-test-report` has generated/triaged a run
- Before starting a new automation run if the last one ended abnormally
  (crashed test, killed Appium server, orphaned emulator process)
- Any time a run behaves as if it inherited state from a previous one
  (already logged in when a test expects a logged-out start, a stray
  dialog still on screen, a session that won't release)

## The one rule that governs everything below

**Check the app's chosen OTP/credential strategy (`docs/<app_slug>-flow.md`
→ Known blockers / Test data, set by `get-mobile-auth`) before resetting
anything.** If the strategy is **Bypass via `NO_RESET` + session reuse**,
the whole point of that setup is a persisted, already-authenticated app
state across runs — clearing app data or forcing a fresh install would
silently break that strategy, not "clean up" after it. Only **Fixed OTP**
and **Manual** strategies expect (and want) a fresh, logged-out state each
run.

## Output

- Device/emulator left in a clean, next-run-ready state appropriate to the
  app's chosen credential strategy
- No orphaned Appium session or driver process
- A short note of what was reset (and, if `NO_RESET` applied, what was
  deliberately left alone and why)

This skill never deletes test code, `docs/`, `data/`, or committed
artifacts — only transient device/session state.

---

# Workflow

## Step 1 — Read the App's Credential Strategy

Read `docs/<app_slug>-flow.md` → *Known blockers / Test data* for the
strategy `get-mobile-auth` recorded, and check `NO_RESET` in `.env`.

| Strategy | What teardown does |
|---|---|
| Fixed OTP in dev | Clear app data / reinstall so the next run hits the login screen fresh |
| Manual | Same as Fixed OTP — a manual step is expected each run regardless |
| Bypass (`NO_RESET` + session reuse) | **Do not clear app data or reinstall.** Only reset transient UI state (see Step 3) |

If the flow doc has no strategy recorded at all, stop and say so rather
than guessing — an unconfigured app means `get-mobile-auth` hasn't run yet.

## Step 2 — Close Out the Appium Session Cleanly

- Confirm the driver session from the last run actually quit
  (`driver.quit()` completed, not just the test process exiting)
- If an Appium server or session is still holding the device, stop it
  rather than starting a new session on top of it — two live sessions
  against one device is a common source of the "next run behaves weird"
  symptom this skill exists to fix

## Step 3 — Reset App/Device State Per the Strategy

- **Fixed OTP / Manual:** clear app data (or uninstall/reinstall from
  `APP_PATH`) so the app opens to its true first-launch/logged-out state
- **Bypass (`NO_RESET`):** leave app data and session alone; only dismiss
  any stray dialog/overlay and return to the app's home/entry screen, so
  the *next* test starts from a known screen without touching auth state
- Either way: close any app left in the background from the failing test,
  don't leave it half-open mid-flow

## Step 4 — Confirm the Device Is Actually Ready

Before declaring teardown done, confirm the device/emulator responds (not
mid-reboot, not showing an ANR/crash dialog from the last run) and the app
is either fully closed (Fixed OTP/Manual) or sitting at a stable screen
(Bypass).

## Step 5 — Report

State plainly: which strategy was detected, what was reset, and — for
Bypass — what was deliberately left untouched and why. This is the signal
a human uses to catch a misconfigured `NO_RESET` before it causes a
confusing failure two runs later, not just now.

---

## Rules

- Never clear app data or force a reinstall for a `NO_RESET`/Bypass app —
  that is not a bug in this skill, it's the point of that strategy.
- Never touch `docs/`, `data/`, test code, or committed artifacts — this
  skill only resets device/session/app runtime state.
- If the credential strategy can't be determined, stop and say so rather
  than defaulting to the destructive (Fixed OTP/Manual-style) reset path.
- This skill runs on its own after `mobile-test-report` — it does not need
  a human confirmation gate the way a real data-deleting teardown would,
  because nothing it touches is backend data; it's local device state only.

## Related Skills

- `get-mobile-auth` — chooses the strategy this skill reads
- `mobile-test-automation` — the next run this skill is preparing the
  device for
- `mobile-test-report` — runs immediately before this skill in the pipeline
