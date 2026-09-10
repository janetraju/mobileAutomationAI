---
name: create-mobile-framework-structure
description: >-
  Bootstraps a brand-new mobile app into an Appium-based, Page Object
  Model (POM) automation repo: analyzes the APK/IPA, registers the app in
  APP_REGISTRY, wires .env (including Appium capabilities), and scaffolds
  the four-layer POM folder skeleton. Use when onboarding a new app,
  setting up project structure for the first time, or before any feature
  context, auth setup, or test design work can begin for that app.
---

# Create Mobile Framework Structure

Bootstrap a new application into the **app-agnostic** framework so downstream
skills (`get-mobile-context`, `get-mobile-auth`, `mobile-test-design`,
`mobile-test-automation`) have a configured app to work against.

This framework is **Appium 2.x** based and follows a **four-layer Page
Object Model (POM)**: Page Objects (locators) → Page Actions (interactions)
→ Steps (orchestration) → Tests. Every app this skill onboards gets the same
Appium/POM skeleton — no other driver or architecture is supported.

Repository conventions (Page Objects, locators, waits, coding standards, etc.)
are defined in `AGENTS.md`. This skill only sets up the app registration and
folder skeleton — it does not gather feature context, define credentials, or
author any test logic.

**Platform coverage status:** the Android path below (APK analysis via
`aapt`, `ANDROID_HOME`/emulator setup) has been exercised end-to-end against
a real app and is proven. The iOS path (IPA analysis, `BUNDLE_ID`,
simulator setup) follows the same Appium/XCUITest conventions but has not
been run end-to-end on a real macOS host — say so plainly when bootstrapping
an iOS app rather than implying equal confidence. Run `mobile-env-doctor`
Step 4 first on any host that hasn't done iOS work before, since iOS
automation requires an actual macOS host — there's no simulator fallback.

## When to Use

Use this skill when an app is **not yet configured**, i.e. any of the
following is true:

- `APP_SLUG` is not present in `.env`
- The app is not registered in `APP_REGISTRY`
- The app's project folders don't exist under `src/`, `tests/`, `data/`, `docs/`

If the app is already configured, skip this skill entirely and go straight to
`get-mobile-context`.

## Output

- App registered in `APP_REGISTRY`
- `.env` populated with:
  - App identity: `APP_NAME`, `APP_SLUG`, `APP_TYPE`, `APP_PACKAGE`,
    `APP_ACTIVITY`, `APP_PATH`
  - Appium capabilities: `PLATFORM`, `APPIUM_HOST`, `APPIUM_PORT`,
    `DEVICE_NAME`
- Empty four-layer **POM** folder skeleton created (no locators, no logic):
  ```
  src/page_objects/<app_slug>/    # Page Object Model — Layer 1
  src/page_actions/<app_slug>/    # Layer 2
  src/steps/<app_slug>/           # Layer 3
  src/constants/<app_slug>/
  tests/test/<app_slug>/          # Layer 4
  data/<app_slug>/
  ```
- `docs/<app_slug>-flow.md` stub, marked **Unconfirmed**
- A host resource pre-flight check wired into `tests/conftest.py`
  (`pytest_sessionstart`) that fails a run fast with a clear message if
  available memory is too low for the emulator/simulator to behave
  reliably, instead of producing confusing intermittent UI failures. Gate
  on available memory, not swap-used percentage — see `mobile-env-doctor`
  Step 1 for why. This is scaffolded by default now, not added reactively
  after a bad session.

Commit these outputs. They are the prerequisite for every other skill in the
feature lifecycle.

---

# Workflow

## Step 1 — Confirm the App Isn't Already Configured

Check `.env`, `APP_REGISTRY`, and existing folders (see When to Use). If
already configured, stop and hand off to `get-mobile-context`.

## Step 2 — Obtain the Build Artifact

If a path is already provided or a file already sits under `builds/`, use
it. Otherwise, hand off to `mobile-build-fetch` rather than just asking
"upload the APK/IPA" — most teams don't have a build sitting locally by
default; it comes from CI, an internal distribution service, or a source
build. For iOS, confirm first (via `mobile-env-doctor` Step 4) that the
current host is actually macOS with Xcode's command-line tools — there is
no way to inspect or run an IPA otherwise.

## Step 3 — Analyze the Artifact

**Android:**
```bash
invoke app:analyze --apk=builds/<app>.apk
```
Uses `aapt dump badging` to extract package name, launch activity, and app
type (native / Flutter / React Native / hybrid — detected from
`libflutter.so` / `index.android.bundle` presence in the archive).

**iOS:**
```bash
invoke app:analyze --ipa=builds/<app>.ipa
```
An IPA is a zip archive — extract `Payload/*.app/Info.plist` and read
`CFBundleIdentifier` (→ `BUNDLE_ID`) and `CFBundleExecutable`. There is no
iOS equivalent of `APP_ACTIVITY`; XCUITest launches by bundle ID alone.
*(This task isn't proven against a real IPA the way the Android path is —
verify the extracted values look sane before trusting them.)*

## Step 4 — Register the App

Configure, in this order:

1. `APP_REGISTRY` — add the new app entry
2. `.env` — set app identity and Appium capabilities. Android:
   `APP_NAME`, `APP_SLUG`, `APP_TYPE`, `APP_PACKAGE`, `APP_ACTIVITY`,
   `APP_PATH`, `PLATFORM=android`, `APPIUM_HOST`, `APPIUM_PORT`,
   `DEVICE_NAME`. iOS: the same identity/Appium fields but `BUNDLE_ID`
   instead of `APP_PACKAGE`/`APP_ACTIVITY`, `PLATFORM=ios`, and
   `DEVICE_NAME` set to a simulator name from `xcrun simctl list devices`
   (or a UDID for a real device).
3. Project folders — create the empty four-layer **POM** skeleton listed in
   Output (identical structure for both platforms — the four-layer POM is
   platform-agnostic; only the driver capabilities differ)

Do **not** derive Page Objects, locators, or any business logic from the
APK/IPA analysis — that requires a live device dump via Appium, done later
by `mobile-test-automation`.

## Step 5 — Create the Flow Doc Stub

Create `docs/<app_slug>-flow.md` with a placeholder structure (sections for
flows, known blockers, test data) and mark its contents **Unconfirmed** until
`get-mobile-context` and `get-mobile-auth` fill them in.

## Step 6 — Scaffold the Host Resource Pre-Flight Check

Add a `pytest_sessionstart` hook to `tests/conftest.py` that fails a run
immediately with a clear message if available memory is below
`MIN_AVAILABLE_MEMORY_MB` (a new `.env` var, default `2048`), per
`mobile-env-doctor` Step 1 — gate on available memory, not swap-used
percentage. This turns a session of confusing intermittent failures into
one fast, actionable exit, for every app this skill bootstraps from here
on rather than only the ones where someone already got burned once.

## Step 7 — Hand Off

Once registration, `.env`, folders, the flow doc stub, and the pre-flight
check exist, hand off to:

- `mobile-env-doctor` to confirm the host/device stack is actually ready
  (especially before iOS work on a host that hasn't done it before)
- `get-mobile-context` for feature/PRD/Figma intake
- `get-mobile-auth` for credential/OTP strategy setup

Do not proceed into feature context, credentials, or automation from this
skill — that is out of scope.
