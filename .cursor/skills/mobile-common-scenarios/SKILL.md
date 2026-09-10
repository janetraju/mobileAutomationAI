---
name: mobile-common-scenarios
description: >-
  Reference patterns for automation scenarios that live outside the app's
  own screens — OS-level permission/system dialogs, deep links, push
  notifications, and background/foreground transitions — so
  mobile-test-automation doesn't rediscover each one ad hoc per app. Use
  when a test needs to handle a system dialog, launch via deep link,
  simulate a push notification, or verify behavior across
  backgrounding/resuming the app.
---

# Mobile Common Scenarios

A reference for interaction patterns that don't fit "find an element in the
app's own accessibility tree and tap it" — because the thing being
interacted with (a permission dialog, another app's picker, the OS
notification tray) isn't part of the app under test. Each category below is
marked **Confirmed** (hit and handled live this session) or **Standard
practice, unverified** (Appium/OS documented behavior, not yet exercised
against a real app here) — treat the two differently.

This skill is reference material, not a workflow with its own inputs/
outputs. `mobile-test-automation` implements the actual Page
Object/Action/Step code; this is where it looks up the pattern first
instead of guessing at a system-level interaction.

## System / Permission Dialogs — **Confirmed**

The single biggest source of "the locator was right but the tap did
nothing" today turned out to be a dialog from a *different* package sitting
on top of the app — not a bug in the app or the test.

- **Check the `package` attribute, not just content-desc, when a screen
  looks wrong.** A permission prompt runs as
  `com.android.permissioncontroller` (Android) or a system alert on iOS —
  not the app's own package. A dump showing unexpected content mixed with
  expected content is often two packages' trees appearing together, not
  app corruption.
- **`AUTO_GRANT_PERMISSIONS` doesn't cover everything.** It handles the
  standard Android runtime-permission grant dialog, but a Google
  account/phone-number picker (`com.google.android.gms`) is a *different*
  system surface that can still appear unpredictably (confirmed: it
  appeared both during onboarding and later, mid-flow, with no consistent
  trigger point identified) and needs its own explicit dismiss step —
  don't assume one capability flag suppresses every system-level popup.
- **Pattern:** before treating an unexpected screen as an app bug, check
  whether it's actually a different package's dialog; dismiss it via its
  own accessibility tree (a `Cancel`/`Allow`/`Deny` button in that
  package), then re-verify the app's own screen underneath.

## Background / Foreground Transitions — **Confirmed (adjacent)**

Not background/resume in the strict sense, but the same underlying
mechanism, used and confirmed working this session as the fix for
needing a known-clean starting screen per test:

```python
driver.terminate_app(settings.app_package)
driver.activate_app(settings.app_package)
```

For an actual background/resume test (does the app preserve state after
being backgrounded, not fully killed):

```python
driver.background_app(seconds)   # Android — standard Appium capability, not yet exercised here for this specific purpose
```

**Caveat, confirmed live:** `terminate_app` immediately followed by
`activate_app` can race the app engine's surface attach and land on a
blank/black screen before it's ready — a short settle wait (`sleep(2-3)`)
after `activate_app` was necessary in practice. Don't assume the app is
interactive the instant `activate_app` returns.

## Deep Links — Standard practice, unverified

Not exercised against a real app this session — the commands below are
Appium/OS documented behavior, treat as a starting point:

```bash
# Android
adb shell am start -a android.intent.action.VIEW -d "<scheme>://<path>"
```
```bash
# iOS
xcrun simctl openurl booted "<scheme>://<path>"
```

Confirm live before trusting: whether the app is already running or needs
a cold launch via the link, and whether the resulting screen matches what
the deep link's destination is supposed to be — don't assume the link
"worked" just because the command didn't error.

## Push Notifications — Standard practice, unverified, genuinely harder

Not exercised this session. Two different approaches exist, and which one
applies depends on what's actually being tested:

- **Testing the app's reaction to a notification tap** (not the delivery
  mechanism itself): Appium's `mobile: pushNotification` (Android
  emulator only) can inject a notification via a base64-encoded payload
  without needing a real backend round-trip.
- **Testing that a real backend event actually triggers a notification**:
  this needs a real notification to be sent, which means triggering the
  backend action that causes it — this is `mobile-test-data`'s territory
  (does the precondition exist to trigger one) combined with this skill's
  job (verifying receipt/tap behavior once it arrives), not a single
  self-contained step.

Decide which of these two a given test case actually needs before
automating either — they test different things and need different setup.

## Rules

- Never assume a system-level dialog is covered by an app-level capability
  flag just because it usually is — confirm the specific dialog's package
  and handle it explicitly if it isn't
- Mark any pattern used from this file as Confirmed for *this app* once
  it's actually been exercised — a pattern being Standard practice here
  doesn't mean it'll work unmodified on the next app
- Don't add elaborate retry/wait logic around a system dialog before
  confirming via the `package` attribute that it's actually what's showing
  — that diagnosis step is fast and prevents chasing the wrong cause

## Related Skills

- `mobile-test-automation` — implements the actual layer code using these
  patterns; owns locator priority/naming for the app's own screens
- `mobile-env-doctor` — a system dialog that never dismisses (vs. one that
  needs a documented step) can be a device/host responsiveness symptom
  instead — check there if a dialog seems permanently stuck
- `mobile-test-data` — push-notification-triggering preconditions are a
  test-data/backend concern, not just a UI interaction
