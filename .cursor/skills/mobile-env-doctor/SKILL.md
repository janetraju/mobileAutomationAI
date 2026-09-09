---
name: mobile-env-doctor
description: >-
  Diagnoses whether the local host, emulator/simulator, and Appium stack are
  actually fit to run mobile automation right now — host resource pressure,
  device/OS responsiveness (including a real Android ANR, not just "adb
  devices shows something"), Appium server/driver health, and known
  dependency version conflicts. Use before a big run, any time tests fail
  in ways that don't point to a locator or code issue, after a long
  session, or whenever a run "feels" flaky without a code-level cause.
---

# Mobile Env Doctor

Answer one question before anything else runs: **is this environment
actually capable of producing a trustworthy result right now?** Every other
skill assumes yes. This skill is the one that checks, and it does so with a
live round-trip test, not just process-existence checks — a device can
report as "online" while its own UI thread is hung.

This skill diagnoses and reports. It does not fix a locator, write a test,
or edit any layer file — a real code-level failure hands off to
`mobile-test-automation`; a stale device/session state hands off to
`teardown`.

## Why this exists

A full session was lost chasing what looked like flaky test failures —
tests that had passed cleanly multiple times started failing identically,
with no code change in between. Working backward through every layer
(Appium `.click()` → raw coordinate tap → raw `adb shell input tap`,
bypassing Appium entirely → a `HOME` keyevent, which worked → relaunching
the app, which didn't help → cold-booting the emulator without its saved
snapshot, which didn't help either) eventually surfaced Android's own
**"System UI isn't responding"** dialog on a brand-new, freshly booted
emulator, before any test code had even run. The device was never actually
capable of running the suite; every "failure" was the same root cause
wearing a different symptom. Two supporting environment issues from the
same session are folded in below: host memory pressure that read fine on
one metric (available RAM) while swap was saturated, and a
locator-adjacent-looking crash that was actually an `allure-pytest` /
`pytest` version incompatibility.

None of this is a hunt for a specific bug — it's a checklist so the *next*
person doesn't have to rediscover the diagnostic path from scratch.

## When to Use

- Before starting a large or long-running automation session
- Any time a previously-passing test fails with no related code change
- When a failure trace bottoms out in a generic timeout/`NoSuchElement`
  after basic navigation, with no obvious locator problem
- After the host has been running emulators/simulators + IDE + browser for
  an extended period
- When switching between iOS and Android work on the same host, or setting
  up iOS automation for the first time on a host that's only done Android
- Any time `mobile-test-report` triages a failure to "environment," per its
  own routing table

## Output

A plain status for each check below: **Healthy**, **Degraded** (usable but
explain the risk), or **Broken** (stop — fix this before running anything).
Never silently downgrade a Broken result to a warning to let a run proceed.

---

# Workflow

## Step 1 — Host Resource Pressure

Check available memory, not just "is the machine slow":

```bash
# Linux
awk '/MemAvailable/ {print $2/1024 " MB available"}' /proc/meminfo
free -h
```

```bash
# macOS
vm_stat
```

- **Broken** if available memory is critically low (a few hundred MB) —
  emulator/simulator input and rendering become unreliable well before the
  OS calls it "out of memory."
- Do **not** gate on swap-used percentage alone. Swap can read as ~100%
  used long after real pressure has passed — the OS doesn't proactively
  swap idle pages back in. `MemAvailable` (Linux) / page-out rate (macOS)
  is the signal that actually tracks current pressure; a project's
  `tests/conftest.py` pre-flight check (see `create-mobile-framework-structure`)
  should gate on the same thing.
- Also glance at load average vs. core count (`uptime`, `nproc`). A
  sustained emulator process pinned at 150%+ CPU on an otherwise-idle
  machine is a *different* problem than memory (see Step 3) — don't
  conflate the two just because both are "environment."

## Step 2 — Appium Server + Driver Health

```bash
curl -s http://$APPIUM_HOST:$APPIUM_PORT/status
appium driver list --installed
```

- **Broken** if `/status` doesn't respond — restart the server before
  anything else.
- Check installed driver versions against Appium's own compatibility
  notes (a version warning printed at Appium startup, e.g. "driver X may
  be incompatible with Appium vY," is a real signal — don't ignore it
  because the server still started).
- **Known dependency conflict, confirmed live:** `allure-pytest` versions
  before **2.16.0** raise `AttributeError: 'str' object has no attribute
  'iter_parents'` during `pytest_runtest_setup` on `pytest>=9` (a
  `FixtureManager` internal API change `allure-pytest` didn't yet handle).
  This looks nothing like an environment issue at first — it's a pytest
  hookwrapper exception, so check dependency versions before assuming a
  broken run is device-related. `pyproject.toml` should pin
  `allure-pytest>=2.16`.

## Step 3 — Device/Simulator Live Responsiveness

`adb devices` / `xcrun simctl list` showing a device is **necessary, not
sufficient**. Confirm the device's own UI thread actually responds:

**Android:**
```bash
adb shell input keyevent KEYCODE_HOME   # system input alive?
adb shell dumpsys window | grep mCurrentFocus  # correct app focused?
adb shell input tap <x> <y>             # does a real tap change anything?
adb shell uiautomator dump               # re-check the tree after the tap
```

If the keyevent works but a tap on a known, on-screen, correctly-bounded
element produces *zero* change in the UI tree — not a wrong screen, no
screen change at all — take a real screenshot (`adb shell screencap`) and
look for Android's **"System UI isn't responding"** ANR dialog before
assuming it's a locator problem. A frozen SystemUI can leave the
accessibility tree reporting stale-but-plausible content while nothing is
actually rendering or accepting input.

If this reproduces on a **freshly cold-booted** emulator
(`emulator -avd <name> -no-snapshot-load`, not the default snapshot boot)
before any test code runs, the emulator itself — not the app, not Appium,
not the test — is the problem. Restart it; if it recurs quickly, this is
Step 1's territory (host can't sustain it), not a device bug to keep
chasing.

**iOS:** *(procedure below is the Android-equivalent adapted from Apple's
own tooling — not yet exercised against a real failure the way the Android
path above was; treat it as a starting checklist, not a proven recipe)*
```bash
xcrun simctl list devices                 # simulator present and Booted?
xcrun simctl io booted screenshot out.png # does it actually render?
xcrun simctl spawn booted log stream --predicate 'eventMessage contains "hang"'
```
A booted-but-blank or stale screenshot, or a `hang`/`SpringBoard` entry in
the log stream, is the iOS-side equivalent of the Android ANR above:
something below the app is not responding, not a test-code problem.

## Step 4 — Platform-Specific Host Readiness

Before attempting iOS work on a host that's only done Android (or vice
versa), confirm the toolchain actually exists — don't assume parity:

**iOS requires a macOS host.** There is no iOS simulator or XCUITest
support on Linux or Windows:
```bash
xcode-select -p          # Xcode command-line tools installed?
xcrun simctl list        # any simulators available?
```
If this is being run from a non-macOS host, **stop here and say so** —
this is a hard platform requirement, not a configuration gap to work
around. `create-mobile-framework-structure` can still register an iOS app
in `APP_REGISTRY` conceptually, but no locator, screen, or flow can be
confirmed live per the "never invent locators" rule until this check
passes on an actual macOS host.

**Android** requires `ANDROID_HOME`/`ANDROID_SDK_ROOT` set and
`platform-tools`/`emulator` present — `invoke appium:doctor` already
covers this; re-run it if in doubt.

## Step 5 — Report

State each check's result plainly (Healthy / Degraded / Broken) and, for
anything not Healthy, the specific next action — not "try again." A
Degraded or Broken result blocks handing off to `mobile-test-automation`
or `mobile-test-report`; loop back to whichever step failed once addressed.

---

## Rules

- A device/simulator reporting "online" is not evidence it's responsive —
  always confirm with a real input round-trip (Step 3), not just presence.
- Never chase a "flaky" failure by adding retries or `time.sleep()` before
  running this skill once — if the environment is Broken, retries just
  burn time reproducing the same non-issue.
- Don't conflate memory pressure, CPU contention, and dependency version
  conflicts — they look similar (intermittent failures with no code cause)
  but need different fixes; diagnose which one it actually is before
  acting.
- iOS guidance here is written from Appium/Apple tooling conventions, not
  from a confirmed live run — say so plainly rather than presenting it with
  the same confidence as the Android path. Update this file once someone
  runs it for real on a macOS host.

## Related Skills

- `create-mobile-framework-structure` — should scaffold a resource
  pre-flight check (Step 1's pattern) into every new app's
  `tests/conftest.py` by default, not add it reactively after a bad session
- `mobile-test-automation` — hands off here when a failure doesn't trace to
  a locator/layer/wait issue
- `mobile-test-report` — routes "environment" failures here per its own
  triage table
- `teardown` — resets device/session/app *state*; this skill checks whether
  the device/host can run anything at all, a different and earlier concern
